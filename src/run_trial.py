from __future__ import annotations

from functools import partial
from typing import Any

from psyflow import StimUnit, next_trial_id, set_trial_context


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
    raise ValueError(f"Unsupported passive-lottery condition format: {condition!r}")


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    score_tracker,
    trigger_runtime,
    block_id=None,
    block_idx=None,
):
    """Run a single passive-lottery trial (no in-trial participant response)."""
    parsed = _parse_condition(condition)
    trial_id = next_trial_id()
    block_idx_val = int(block_idx) if block_idx is not None else 0
    trial_index = int(parsed["trial_index"]) if int(parsed["trial_index"]) > 0 else int(trial_id)
    block_id_val = str(block_id) if block_id is not None else "block_0"

    trial_data = {
        "trial_id": trial_index,
        "block_id": block_id_val,
        "block_idx": block_idx_val,
        "condition": parsed["condition"],
        "condition_id": parsed["condition_id"],
        "condition_label": parsed["condition_label"],
        "prob_a": parsed["prob_a"],
        "outcome_a": parsed["outcome_a"],
        "outcome_b": parsed["outcome_b"],
    }
    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    condition_cue_duration = float(getattr(settings, "condition_cue_duration", 0.5))
    condition_cue = make_unit(unit_label="condition_cue").add_stim(
        stim_bank.get_and_format(
            "condition_cue",
            condition_label=parsed["condition_label"],
            condition_code=parsed["condition"],
        )
    )
    set_trial_context(
        condition_cue,
        trial_id=trial_index,
        phase="condition_cue",
        deadline_s=condition_cue_duration,
        valid_keys=[],
        block_id=block_id_val,
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "condition_cue",
            "condition": parsed["condition"],
            "condition_label": parsed["condition_label"],
            "block_idx": block_idx_val,
        },
        stim_id="condition_cue",
    )
    condition_cue.show(
        duration=condition_cue_duration,
        onset_trigger=settings.triggers.get(f"{parsed['condition']}_condition_cue_onset"),
    ).to_dict(trial_data)

    pre_lottery_fixation_duration = float(getattr(settings, "pre_lottery_fixation_duration", 0.5))
    pre_lottery_fixation = make_unit(unit_label="pre_lottery_fixation").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        pre_lottery_fixation,
        trial_id=trial_index,
        phase="pre_lottery_fixation",
        deadline_s=pre_lottery_fixation_duration,
        valid_keys=[],
        block_id=block_id_val,
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "pre_lottery_fixation",
            "condition": parsed["condition"],
            "block_idx": block_idx_val,
        },
        stim_id="fixation",
    )
    pre_lottery_fixation.show(
        duration=pre_lottery_fixation_duration,
        onset_trigger=settings.triggers.get(f"{parsed['condition']}_pre_lottery_fixation_onset"),
    ).to_dict(trial_data)

    lottery_reveal_duration = float(getattr(settings, "lottery_reveal_duration", 0.5))
    lottery_reveal = make_unit(unit_label="lottery_reveal").add_stim(
        stim_bank.get_and_format(
            "lottery_offer",
            prob_a=int(round(parsed["prob_a"] * 100.0)),
            rest_prob=int(round((1.0 - parsed["prob_a"]) * 100.0)),
            outcome_a=parsed["outcome_a"],
            outcome_b=parsed["outcome_b"],
        )
    )
    set_trial_context(
        lottery_reveal,
        trial_id=trial_index,
        phase="lottery_reveal",
        deadline_s=lottery_reveal_duration,
        valid_keys=[],
        block_id=block_id_val,
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
    lottery_reveal.capture_response(
        keys=[],
        duration=lottery_reveal_duration,
        onset_trigger=settings.triggers.get(f"{parsed['condition']}_lottery_reveal_onset"),
        terminate_on_response=False,
    )
    lottery_reveal.to_dict(trial_data)

    outcome_value = int(parsed["outcome_value"])
    outcome_kind = str(parsed["outcome_kind"])
    total_score = score_tracker.update(outcome_value)

    outcome_feedback_duration = float(getattr(settings, "outcome_feedback_duration", 0.5))
    outcome_stim_id = f"outcome_{outcome_kind}"
    outcome_feedback = make_unit(unit_label="outcome_feedback").add_stim(
        stim_bank.get_and_format(
            outcome_stim_id,
            outcome_value=outcome_value,
            total_score=total_score,
        )
    )
    set_trial_context(
        outcome_feedback,
        trial_id=trial_index,
        phase="outcome_feedback",
        deadline_s=outcome_feedback_duration,
        valid_keys=[],
        block_id=block_id_val,
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "outcome_feedback",
            "condition": parsed["condition"],
            "outcome_value": outcome_value,
            "outcome_kind": outcome_kind,
            "total_score": total_score,
            "block_idx": block_idx_val,
        },
        stim_id=outcome_stim_id,
    )
    outcome_feedback.show(
        duration=outcome_feedback_duration,
        onset_trigger=settings.triggers.get(f"{parsed['condition']}_{outcome_kind}_outcome_feedback_onset"),
    ).to_dict(trial_data)

    iti_duration = float(getattr(settings, "iti_duration", 0.6))
    iti = make_unit(unit_label="iti").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        iti,
        trial_id=trial_index,
        phase="iti",
        deadline_s=iti_duration,
        valid_keys=[],
        block_id=block_id_val,
        condition_id=parsed["condition_id"],
        task_factors={"stage": "iti", "block_idx": block_idx_val},
        stim_id="fixation",
    )
    iti.show(
        duration=iti_duration,
        onset_trigger=settings.triggers.get("iti_onset"),
    ).to_dict(trial_data)

    trial_data["outcome_kind"] = outcome_kind
    trial_data["outcome_value"] = outcome_value
    trial_data["feedback_delta"] = outcome_value
    trial_data["total_score"] = total_score
    return trial_data
