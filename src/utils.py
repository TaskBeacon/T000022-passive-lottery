from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Any

from psychopy import logging


@dataclass(frozen=True)
class LotteryProfile:
    label: str
    prob_a: float
    outcome_a: int
    outcome_b: int


class Controller:
    """Passive-lottery scheduler and score tracker."""

    def __init__(
        self,
        *,
        lottery_profiles: dict[str, dict[str, Any]],
        seed: int = 2026,
        enable_logging: bool = True,
    ) -> None:
        self.enable_logging = bool(enable_logging)
        self.seed = int(seed)
        self._rng = random.Random(self.seed)
        self._profiles = self._build_profiles(lottery_profiles)
        self._history: list[dict[str, Any]] = []
        self._total_score = 0

    @classmethod
    def from_dict(cls, config: dict[str, Any]) -> "Controller":
        profiles = config.get("lottery_profiles", {})
        if not isinstance(profiles, dict) or not profiles:
            raise ValueError("controller.lottery_profiles must be a non-empty mapping")
        return cls(
            lottery_profiles=profiles,
            seed=int(config.get("seed", 2026)),
            enable_logging=bool(config.get("enable_logging", True)),
        )

    def _build_profiles(self, raw: dict[str, dict[str, Any]]) -> dict[str, LotteryProfile]:
        out: dict[str, LotteryProfile] = {}
        for key, spec in raw.items():
            prob_a = float(spec.get("prob_a", 0.5))
            if prob_a < 0.0 or prob_a > 1.0:
                raise ValueError(f"controller.lottery_profiles.{key}.prob_a must be in [0, 1]")
            out[str(key)] = LotteryProfile(
                label=str(spec.get("label", key)),
                prob_a=prob_a,
                outcome_a=int(spec.get("outcome_a", 0)),
                outcome_b=int(spec.get("outcome_b", 0)),
            )
        return out

    @property
    def total_score(self) -> int:
        return int(self._total_score)

    @property
    def histories(self) -> dict[str, list[dict[str, Any]]]:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for item in self._history:
            grouped.setdefault(str(item["condition"]), []).append(item)
        return grouped

    def get_profile(self, condition: str) -> LotteryProfile:
        condition = str(condition)
        if condition not in self._profiles:
            raise KeyError(f"Unknown condition: {condition!r}")
        return self._profiles[condition]

    def prepare_block(self, *, block_idx: int, n_trials: int, conditions: list[str]) -> list[tuple[Any, ...]]:
        if n_trials <= 0:
            return []
        normalized_conditions = [str(c) for c in conditions if str(c) in self._profiles]
        if not normalized_conditions:
            raise ValueError("No valid condition available for passive lottery block")

        # Balanced condition list, then shuffled per block.
        scheduled: list[str] = [normalized_conditions[i % len(normalized_conditions)] for i in range(n_trials)]
        self._rng.shuffle(scheduled)

        planned: list[tuple[Any, ...]] = []
        for trial_index, cond in enumerate(scheduled, start=1):
            profile = self.get_profile(cond)
            draw_a = bool(self._rng.random() < profile.prob_a)
            outcome_value = profile.outcome_a if draw_a else profile.outcome_b
            outcome_kind = self._value_to_kind(outcome_value)
            condition_id = f"{cond}_p{int(round(profile.prob_a * 100))}_t{trial_index:03d}"
            planned.append(
                (
                    cond,
                    profile.label,
                    float(profile.prob_a),
                    int(profile.outcome_a),
                    int(profile.outcome_b),
                    int(outcome_value),
                    outcome_kind,
                    condition_id,
                    int(trial_index),
                )
            )

        if self.enable_logging:
            logging.data(
                "[PassiveLotteryController] "
                f"block={block_idx} n_trials={n_trials} seed={self.seed} "
                f"conditions={normalized_conditions}"
            )
        return planned

    def register_outcome(
        self,
        *,
        condition: str,
        block_idx: int,
        trial_index: int,
        outcome_value: int,
        outcome_kind: str,
    ) -> int:
        self._total_score += int(outcome_value)
        item = {
            "condition": str(condition),
            "block_idx": int(block_idx),
            "trial_index": int(trial_index),
            "outcome_value": int(outcome_value),
            "outcome_kind": str(outcome_kind),
            "total_score": int(self._total_score),
        }
        self._history.append(item)
        if self.enable_logging:
            logging.data(
                "[PassiveLotteryController] "
                f"trial={trial_index} block={block_idx} condition={condition} "
                f"outcome={outcome_value:+d} kind={outcome_kind} total={self._total_score}"
            )
        return int(self._total_score)

    @staticmethod
    def _value_to_kind(value: int) -> str:
        if value > 0:
            return "win"
        if value < 0:
            return "loss"
        return "neutral"
