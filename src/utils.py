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


class ScoreTracker:
    """Track cumulative passive-lottery score."""

    def __init__(self, initial_score: int = 0) -> None:
        self.total_score = int(initial_score)

    def update(self, outcome_value: int) -> int:
        self.total_score += int(outcome_value)
        return int(self.total_score)


def _value_to_kind(value: int) -> str:
    if int(value) > 0:
        return "win"
    if int(value) < 0:
        return "loss"
    return "neutral"


def build_lottery_profiles(lottery_profiles: dict[str, dict[str, Any]]) -> dict[str, LotteryProfile]:
    if not isinstance(lottery_profiles, dict) or not lottery_profiles:
        raise ValueError("condition_generation.lottery_profiles must be a non-empty mapping")

    out: dict[str, LotteryProfile] = {}
    for key, spec in lottery_profiles.items():
        prob_a = float(spec.get("prob_a", 0.5))
        if prob_a < 0.0 or prob_a > 1.0:
            raise ValueError(f"condition_generation.lottery_profiles.{key}.prob_a must be in [0, 1]")
        out[str(key)] = LotteryProfile(
            label=str(spec.get("label", key)),
            prob_a=prob_a,
            outcome_a=int(spec.get("outcome_a", 0)),
            outcome_b=int(spec.get("outcome_b", 0)),
        )
    return out


def generate_passive_lottery_conditions(
    n_trials: int,
    condition_labels: list[Any] | None,
    *,
    seed: int,
    lottery_profiles: dict[str, dict[str, Any]],
    seed_offset: int = 0,
    enable_logging: bool = True,
    **kwargs,
) -> list[tuple[Any, ...]]:
    """
    Generate balanced, shuffled passive-lottery trials with preplanned outcomes.

    Returns tuples:
    (condition, label, prob_a, outcome_a, outcome_b, outcome_value, outcome_kind, condition_id, trial_index)
    """
    del kwargs

    profiles = build_lottery_profiles(lottery_profiles)
    labels = [str(c) for c in (condition_labels or []) if str(c) in profiles]
    if not labels:
        raise ValueError("No valid task.conditions entries matched condition_generation.lottery_profiles")

    n = int(n_trials)
    if n <= 0:
        return []

    rng = random.Random(int(seed) + int(seed_offset))

    # Balanced schedule, then randomized within block.
    scheduled = [labels[i % len(labels)] for i in range(n)]
    rng.shuffle(scheduled)

    planned: list[tuple[Any, ...]] = []
    for trial_index, cond in enumerate(scheduled, start=1):
        profile = profiles[cond]
        draw_a = bool(rng.random() < profile.prob_a)
        outcome_value = profile.outcome_a if draw_a else profile.outcome_b
        outcome_kind = _value_to_kind(outcome_value)
        condition_id = f"{cond}_p{int(round(profile.prob_a * 100))}_t{trial_index:03d}"
        planned.append(
            (
                cond,
                profile.label,
                float(profile.prob_a),
                int(profile.outcome_a),
                int(profile.outcome_b),
                int(outcome_value),
                str(outcome_kind),
                str(condition_id),
                int(trial_index),
            )
        )

    if bool(enable_logging):
        logging.data(
            "[PassiveLottery] "
            f"n_trials={n} seed={int(seed) + int(seed_offset)} "
            f"labels={labels}"
        )
    return planned
