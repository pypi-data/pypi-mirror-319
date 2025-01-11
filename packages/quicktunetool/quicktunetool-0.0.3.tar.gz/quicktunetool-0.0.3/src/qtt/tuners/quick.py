import json
import pickle
import logging
import os
import time
from typing import Callable, Any

import numpy as np
import pandas as pd

from ..optimizers import Optimizer
from ..utils import (
    add_log_to_file,
    config_to_serializible_dict,
    set_logger_verbosity,
    setup_outputdir,
)

logger = logging.getLogger(__name__)


class QuickTuner:
    """
    QuickTuner is a simple tuner that can be used to optimize a given function
    using a given optimizer.

    Args:
        optimizer (Optimizer): An instance of an Optimizer class.
        f (Callable): A function that takes a configuration and returns a score.
        path (str, optional): Directory location to store all outputs. Defaults to None.
            If None, a new unique time-stamped directory is chosen.
        save_freq (str, optional): Frequency of saving the state of the tuner. Defaults to "step".
            - "step": save after each evaluation.
            - "incumbent": save only when the incumbent changes.
            - None: do not save.
        verbosity (int, optional): Verbosity level of the logger. Defaults to 2.
        resume (bool, optional): Whether to resume the tuner from a previous state. Defaults to False.
    """

    log_to_file: bool = True
    log_file_name: str = "quicktuner.log"
    log_file_path: str = "auto"
    path_suffix: str = "tuner"

    def __init__(
        self,
        optimizer: Optimizer,
        f: Callable,
        path: str | None = None,
        save_freq: str | None = "step",
        verbosity: int = 2,
        resume: bool = False,
        **kwargs,
    ):
        if resume and path is None:
            raise ValueError("Cannot resume without specifying a path.")
        self._validate_kwargs(kwargs)

        self.verbosity = verbosity
        set_logger_verbosity(verbosity, logger)

        self.output_dir = setup_outputdir(path, path_suffix=self.path_suffix)
        self._setup_log_to_file(self.log_to_file, self.log_file_path)

        if save_freq not in ["step", "incumbent"] and save_freq is not None:
            raise ValueError("Invalid value for 'save_freq'.")
        self.save_freq = save_freq

        self.optimizer = optimizer
        self.optimizer.reset_path(self.output_dir)
        self.f = f

        # trackers
        self.inc_score: float = 0.0
        self.inc_fidelity: int = -1
        self.inc_config: dict = {}
        self.inc_cost: float = 0.0
        self.inc_info: object = None
        self.inc_id: int = -1
        self.traj: list[object] = []
        self.history: list[object] = []
        self.runtime: list[object] = []

        self._remaining_fevals = None
        self._remaining_time = None

        if resume:
            self.load(os.path.join(self.output_dir, "qt.json"))

    def _setup_log_to_file(self, log_to_file: bool, log_file_path: str) -> None:
        if not log_to_file:
            return
        if log_file_path == "auto":
            log_file_path = os.path.join(self.output_dir, "logs", self.log_file_name)
        log_file_path = os.path.abspath(os.path.normpath(log_file_path))
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        add_log_to_file(log_file_path, logger)

    def _is_budget_exhausted(self, fevals=None, time_budget=None):
        """Checks if the run should be terminated or continued."""
        if fevals is not None:
            evals_left = fevals - len(self.traj)
            if evals_left <= 0:
                return True
            logger.info(f"Evaluations left: {evals_left}")
        if time_budget is not None:
            time_left = time_budget - (time.time() - self.start)
            if time_left <= 0:
                return True
            logger.info(f"Time left: {time_left:.2f}s")
        return False

    def _save_incumbent(self, save: bool = True):
        if not self.inc_config or not save:
            return
        try:
            out: dict[str, Any] = {}
            out["config"] = self.inc_config
            out["score"] = self.inc_score
            out["cost"] = self.inc_cost
            out["info"] = self.inc_info
            with open(os.path.join(self.output_dir, "incumbent.json"), "w") as f:
                json.dump(out, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save incumbent: {e}")

    def _save_history(self, save: bool = True):
        if not self.history or not save:
            return
        try:
            history_path = os.path.join(self.output_dir, "history.csv")
            history_df = pd.DataFrame(self.history)
            history_df.to_csv(history_path)
        except Exception as e:
            logger.warning(f"History not saved: {e!r}")
        finally:
            logger.info("Saved history.")

    def _log_job_submission(self, trial_info: dict):
        fidelity = trial_info["fidelity"]
        config_id = trial_info["config-id"]
        logger.info(
            f"INCUMBENT: {self.inc_id}  "
            f"SCORE: {self.inc_score}  "
            f"FIDELITY: {self.inc_fidelity}",
        )
        logger.info(f"Evaluating configuration {config_id} with fidelity {fidelity}")

    def _get_state(self):
        state = self.__dict__.copy()
        state.pop("optimizer")
        state.pop("f")
        return state

    def _save_state(self, save: bool = True):
        if not save:
            return
        # Get state
        state = self._get_state()
        # Write state to disk
        try:
            state_path = os.path.join(self.output_dir, "qt.json")
            with open(state_path, "wb") as f:
                pickle.dump(state, f, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            logger.warning(f"State not saved: {e!r}")
        finally:
            logger.info("State saved to disk.")
        try:
            opt_path = os.path.join(self.output_dir, "optimizer")
            self.optimizer.save(opt_path)
        except Exception as e:
            logger.warning(f"Optimizer state not saved: {e!r}")

    def save(self, incumbent: bool = True, history: bool = True, state: bool = True):
        logger.info("Saving current state to disk...")
        self._save_incumbent(incumbent)
        self._save_history(history)
        self._save_state(state)

    def load(self, path: str):
        logger.info(f"Loading state from {path}")
        with open(path, "rb") as f:
            state = pickle.load(f)
        self.__dict__.update(state)
        self.optimizer = Optimizer.load(os.path.join(self.output_dir, "optimizer"))

    def run(
        self,
        fevals: int | None = None,
        time_budget: float | None = None,
        trial_info: dict | None = None,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Run the tuner.

        Args:
            fevals (int, optional): Number of function evaluations to run. Defaults to None.
            time_budget (float, optional): Time budget in seconds. Defaults to None.
            trial_info (dict, optional): Additional information to pass to the objective function. Defaults to None.

        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray]:
                - trajectory (np.ndarray): Trajectory of the incumbent scores.
                - runtime (np.ndarray): Runtime of the incumbent evaluations.
                - history (np.ndarray): History of all evaluations.
        """
        logger.info("Starting QuickTuner Run...")
        logger.info(f"QuickTuneTool will save results to {self.output_dir}")

        self.start = time.time()
        while True:
            self.optimizer.ante()

            # ask for a new configuration
            trial = self.optimizer.ask()
            if trial is None:
                break
            _trial_info = self._add_trial_info(trial_info)

            self._log_job_submission(trial)
            result = self.f(trial, trial_info=_trial_info)

            self._log_report(result)
            self.optimizer.tell(result)

            self.optimizer.post()
            if self._is_budget_exhausted(fevals, time_budget):
                logger.info("Budget exhausted. Stopping run...")
                break

        self._log_end()
        self.save()

        return (
            np.array(self.traj),
            np.array(self.runtime),
            np.array(self.history, dtype=object),
        )

    def _update_trackers(self, traj, runtime, history):
        self.traj.append(traj)
        self.runtime.append(runtime)
        self.history.append(history)

    def _log_report(self, reports):
        if isinstance(reports, dict):
            reports = [reports]

        inc_changed = False
        for report in reports:
            config_id = report["config-id"]
            score = report["score"]
            cost = report["cost"]
            fidelity = report["fidelity"]
            config = config_to_serializible_dict(report["config"])

            separator = "-" * 60
            logger.info(separator)
            logger.info(f"CONFIG ID : {config_id}")
            logger.info(f"FIDELITY  : {fidelity}")
            logger.info(f"SCORE     : {score:.3f}")
            logger.info(f"TIME      : {cost:.3f}")
            logger.info(separator)

            if self.inc_score < score:
                self.inc_score = score
                self.inc_cost = cost
                self.inc_fidelity = fidelity
                self.inc_id = config_id
                self.inc_config = config
                self.inc_info = report.get("info")
                inc_changed = True

            report["config"] = config
            self._update_trackers(
                self.inc_score,
                time.time() - self.start,
                report,
            )

        if self.save_freq == "step" or (self.save_freq == "incumbent" and inc_changed):
            self.save()

    def _log_end(self):
        separator = "=" * 60
        logger.info(separator)
        logger.info("RUN COMPLETE - SUMMARY REPORT")
        logger.info(separator)
        logger.info(f"Best Score        : {self.inc_score:.3f}")
        logger.info(f"Best Cost         : {self.inc_cost:.3f} seconds")
        logger.info(f"Best Config ID    : {self.inc_id}")
        logger.info(f"Best Configuration: {self.inc_config}")
        logger.info(separator)

    def _validate_kwargs(self, kwargs: dict) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                logger.warning(f"Unknown argument: {key}")

    def _add_trial_info(self, task_info: dict | None) -> dict:
        out = {} if task_info is None else task_info.copy()
        out["output-dir"] = self.output_dir
        out["remaining-fevals"] = self._remaining_fevals
        out["remaining-time"] = self._remaining_time
        return out

    def get_incumbent(self):
        return (
            self.inc_id,
            self.inc_config,
            self.inc_score,
            self.inc_fidelity,
            self.inc_cost,
            self.inc_info,
        )
