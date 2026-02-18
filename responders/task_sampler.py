from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from psyflow.sim.contracts import Action, Feedback, Observation, SessionInfo


@dataclass
class TaskSamplerResponder:
    """Sampler responder for passive lottery.

    This task has no in-trial response. The responder only advances
    instruction / break / goodbye pages by pressing `continue_key`.
    """

    continue_key: str = "space"
    continue_rt_s: float = 0.25

    def __post_init__(self) -> None:
        self.continue_rt_s = max(0.0, float(self.continue_rt_s))
        self._rng: Any = None

    def start_session(self, session: SessionInfo, rng: Any) -> None:
        self._rng = rng

    def on_feedback(self, fb: Feedback) -> None:
        return None

    def end_session(self) -> None:
        self._rng = None

    def act(self, obs: Observation) -> Action:
        valid_keys = list(obs.valid_keys or [])
        if not valid_keys:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "no_valid_keys"})
        if self.continue_key in valid_keys:
            return Action(
                key=self.continue_key,
                rt_s=self.continue_rt_s,
                meta={"source": "task_sampler", "policy": "continue"},
            )
        return Action(key=valid_keys[0], rt_s=self.continue_rt_s, meta={"source": "task_sampler", "policy": "fallback"})
