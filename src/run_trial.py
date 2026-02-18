from __future__ import annotations

from functools import partial
from typing import Any

from psyflow import StimUnit, set_trial_context


def _deadline_s(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, (list, tuple)) and value:
        try:
            return float(max(value))
        except Exception:
            return None
    return None


def _parse_condition(condition: Any) -> dict[str, Any]:
    if isinstance(condition, tuple) and len(condition) >= 9:
        (
            condition_name,
            condition_label,
            prob_a,
            outcome_a,
            outcome_b,
            outcome_value,
            outcome_kind,
            condition_id,
            trial_index,
            *_,
        ) = condition
        return {
            "condition": str(condition_name),
            "condition_label": str(condition_label),
            "prob_a": float(prob_a),
            "outcome_a": int(outcome_a),
            "outcome_b": int(outcome_b),
            "outcome_value": int(outcome_value),
            "outcome_kind": str(outcome_kind),
            "condition_id": str(condition_id),
            "trial_index": int(trial_index),
        }
    if isinstance(condition, dict):
        return {
            "condition": str(condition.get("condition", "gain")),
            "condition_label": str(condition.get("condition_label", condition.get("condition", "gain"))),
            "prob_a": float(condition.get("prob_a", 0.5)),
            "outcome_a": int(condition.get("outcome_a", 0)),
            "outcome_b": int(condition.get("outcome_b", 0)),
            "outcome_value": int(condition.get("outcome_value", 0)),
            "outcome_kind": str(condition.get("outcome_kind", "neutral")),
            "condition_id": str(condition.get("condition_id", "unknown")),
            "trial_index": int(condition.get("trial_index", 0)),
        }
    return {
        "condition": str(condition),
        "condition_label": str(condition),
        "prob_a": 0.5,
        "outcome_a": 0,
        "outcome_b": 0,
        "outcome_value": 0,
        "outcome_kind": "neutral",
        "condition_id": str(condition),
        "trial_index": 0,
    }


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    controller,
    trigger_runtime,
    block_id=None,
    block_idx=None,
):
    """Run a single passive lottery trial (no in-trial key press required)."""
    parsed = _parse_condition(condition)
    block_idx_val = int(block_idx) if block_idx is not None else 0
    trial_id = int(len(controller.histories.get(parsed["condition"], [])) + 1)

    trial_data = {
        "trial_id": int(parsed["trial_index"]) if parsed["trial_index"] > 0 else int(trial_id),
        "block_id": str(block_id) if block_id is not None else "block_0",
        "block_idx": block_idx_val,
        "condition": parsed["condition"],
        "condition_id": parsed["condition_id"],
        "condition_label": parsed["condition_label"],
        "prob_a": parsed["prob_a"],
        "outcome_a": parsed["outcome_a"],
        "outcome_b": parsed["outcome_b"],
    }
    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    cue = make_unit(unit_label="cue").add_stim(
        stim_bank.get_and_format(
            "condition_cue",
            condition_label=parsed["condition_label"],
            condition_code=parsed["condition"],
        )
    )
    set_trial_context(
        cue,
        trial_id=trial_data["trial_id"],
        phase="offer_cue",
        deadline_s=_deadline_s(settings.cue_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "offer_cue",
            "condition": parsed["condition"],
            "condition_label": parsed["condition_label"],
            "block_idx": block_idx_val,
        },
        stim_id="condition_cue",
    )
    cue.show(
        duration=settings.cue_duration,
        onset_trigger=settings.triggers.get(f"{parsed['condition']}_cue_onset"),
    ).to_dict(trial_data)

    anticipation = make_unit(unit_label="anticipation").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        anticipation,
        trial_id=trial_data["trial_id"],
        phase="pre_lottery_fixation",
        deadline_s=_deadline_s(settings.anticipation_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "pre_lottery_fixation",
            "condition": parsed["condition"],
            "block_idx": block_idx_val,
        },
        stim_id="fixation",
    )
    anticipation.show(
        duration=settings.anticipation_duration,
        onset_trigger=settings.triggers.get(f"{parsed['condition']}_anticipation_onset"),
    ).to_dict(trial_data)

    target = make_unit(unit_label="target").add_stim(
        stim_bank.get_and_format(
            "lottery_offer",
            prob_a=int(round(parsed["prob_a"] * 100.0)),
            rest_prob=int(round((1.0 - parsed["prob_a"]) * 100.0)),
            outcome_a=parsed["outcome_a"],
            outcome_b=parsed["outcome_b"],
        )
    )
    set_trial_context(
        target,
        trial_id=trial_data["trial_id"],
        phase="lottery_reveal",
        deadline_s=_deadline_s(settings.lottery_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "lottery_reveal",
            "condition": parsed["condition"],
            "prob_a": parsed["prob_a"],
            "outcome_a": parsed["outcome_a"],
            "outcome_b": parsed["outcome_b"],
            "block_idx": block_idx_val,
        },
        stim_id="lottery_offer",
    )
    target.capture_response(
        keys=[],
        duration=settings.lottery_duration,
        onset_trigger=settings.triggers.get(f"{parsed['condition']}_lottery_onset"),
        terminate_on_response=False,
    )
    target.to_dict(trial_data)

    outcome_value = int(parsed["outcome_value"])
    outcome_kind = str(parsed["outcome_kind"])
    cumulative_score = controller.register_outcome(
        condition=parsed["condition"],
        block_idx=block_idx_val,
        trial_index=int(trial_data["trial_id"]),
        outcome_value=outcome_value,
        outcome_kind=outcome_kind,
    )

    outcome_unit_name = f"outcome_{outcome_kind}"
    feedback = make_unit(unit_label="feedback").add_stim(
        stim_bank.get_and_format(
            outcome_unit_name,
            outcome_value=outcome_value,
            total_score=cumulative_score,
        )
    )
    set_trial_context(
        feedback,
        trial_id=trial_data["trial_id"],
        phase="outcome_feedback",
        deadline_s=_deadline_s(settings.feedback_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "outcome_feedback",
            "condition": parsed["condition"],
            "outcome_value": outcome_value,
            "outcome_kind": outcome_kind,
            "total_score": cumulative_score,
            "block_idx": block_idx_val,
        },
        stim_id=outcome_unit_name,
    )
    feedback.show(
        duration=settings.feedback_duration,
        onset_trigger=settings.triggers.get(f"{parsed['condition']}_{outcome_kind}_outcome_onset"),
    ).to_dict(trial_data)

    iti = make_unit(unit_label="iti").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        iti,
        trial_id=trial_data["trial_id"],
        phase="inter_trial_interval",
        deadline_s=_deadline_s(settings.iti_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={"stage": "inter_trial_interval", "block_idx": block_idx_val},
        stim_id="fixation",
    )
    iti.show(duration=settings.iti_duration, onset_trigger=settings.triggers.get("iti_onset")).to_dict(trial_data)

    trial_data["outcome_kind"] = outcome_kind
    trial_data["outcome_value"] = outcome_value
    trial_data["feedback_delta"] = outcome_value
    trial_data["total_score"] = cumulative_score

    return trial_data
