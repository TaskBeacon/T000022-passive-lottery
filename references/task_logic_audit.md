# Task Logic Audit: Passive Lottery Task

## 1. Paradigm Intent

- Task: `passive_lottery`
- Primary construct: expectancy and valence-sensitive outcome processing under passive observation.
- Manipulated factors: lottery profile valence (`gain`, `loss`, `mixed`) and sampled trial outcome (`win`, `neutral`, `loss`).
- Dependent measures: trial-wise `outcome_kind`, `outcome_value`, cumulative score, and phase-aligned trigger timing.
- Key citations:
  - `W2140531843` (reward/punishment prediction error framing and cue-anticipation-outcome structure)
  - `W2035219495` (prediction-error model constraints for outcome interpretation)
  - `W2002597000` (passive viewing framing for non-choice valuation paradigms)
  - `W2024690164` (uncertainty representation context; supports ambiguity framing rationale)

## 2. Block/Trial Workflow

### Block Structure

- Human profile: `task.total_blocks=3`, `task.trial_per_block=24`, `task.total_trials=72`.
- QA and sim profiles: shortened to `1 x 9` for gate-speed execution.
- Condition scheduling: custom condition generation builds a balanced condition list, shuffles with seeded RNG, and pre-samples outcomes from each condition profile.

### Trial State Machine

1. `condition_cue`
   - Onset trigger: `{condition}_condition_cue_onset` (`20/21/22`).
   - Stimulus shown: `condition_cue` text with condition-specific label.
   - Valid keys: none.
   - Timeout behavior: fixed `timing.condition_cue_duration`, then auto-advance.
   - Next state: `pre_lottery_fixation`.
2. `pre_lottery_fixation`
   - Onset trigger: `{condition}_pre_lottery_fixation_onset` (`30/31/32`).
   - Stimulus shown: `fixation` (`+`).
   - Valid keys: none.
   - Timeout behavior: fixed `timing.pre_lottery_fixation_duration`, then auto-advance.
   - Next state: `lottery_reveal`.
3. `lottery_reveal`
   - Onset trigger: `{condition}_lottery_reveal_onset` (`40/41/42`).
   - Stimulus shown: `lottery_offer` with probability and two outcomes.
   - Valid keys: none.
   - Timeout behavior: fixed `timing.lottery_reveal_duration`, then auto-advance.
   - Next state: `outcome_feedback`.
4. `outcome_feedback`
   - Onset trigger: `{condition}_{outcome_kind}_outcome_feedback_onset` (`50-58`).
   - Stimulus shown: `outcome_win` or `outcome_neutral` or `outcome_loss`.
   - Valid keys: none.
   - Timeout behavior: fixed `timing.outcome_feedback_duration`, then auto-advance.
   - Next state: `iti`.
5. `iti`
   - Onset trigger: `iti_onset` (`60`).
   - Stimulus shown: `fixation`.
   - Valid keys: none.
   - Timeout behavior: fixed `timing.iti_duration`, then next trial.

Block wrappers:
- Block start trigger: `block_onset` (`10`).
- Block end trigger: `block_end` (`11`).
- Post-block summary page uses `block_break` and waits for continue key.

Session wrappers:
- Experiment start trigger: `exp_onset` (`1`).
- Experiment end trigger: `exp_end` (`2`).
- Final page uses `good_bye` and waits for continue key.

## 3. Condition Semantics

- Condition ID: `gain`
  - Participant-facing meaning: high-probability non-negative lottery (positive or zero points).
  - Concrete realization: cue label from `condition_generation.lottery_profiles.gain.label`, then offer text with `prob_a=0.75`, outcomes `+10` and `0`.
  - Outcome rules: sampled by RNG; outcome kind is `win` for `+10`, `neutral` for `0`.
- Condition ID: `loss`
  - Participant-facing meaning: high-probability negative lottery (negative or zero points).
  - Concrete realization: cue label from `condition_generation.lottery_profiles.loss.label`, then offer text with `prob_a=0.75`, outcomes `-10` and `0`.
  - Outcome rules: outcome kind is `loss` for `-10`, `neutral` for `0`.
- Condition ID: `mixed`
  - Participant-facing meaning: balanced mixed-valence lottery.
  - Concrete realization: cue label from `condition_generation.lottery_profiles.mixed.label`, then offer text with `prob_a=0.5`, outcomes `+10` and `-10`.
  - Outcome rules: outcome kind is `win` for `+10`, `loss` for `-10`.

## 4. Response and Scoring Rules

- Response mapping:
  - Trial phases are passive; no response is collected during cue/anticipation/lottery/feedback/ITI.
  - Continue key (`space`) is used only on instruction, block break, and goodbye pages.
- Missing-response policy:
  - Not applicable for trial phases (no valid trial keys).
  - For continue pages, task waits until a valid continue press.
- Correctness logic:
  - No correct/incorrect classification; passive observation only.
- Reward/penalty update:
  - `ScoreTracker.update(...)` adds `outcome_value` to running `total_score` each trial.
- Running metrics:
  - Trial-level: condition, sampled outcomes, trigger-aligned timestamps, cumulative score.
  - Block-level: block score and win-rate summary on `block_break`.

## 5. Stimulus Layout Plan

- Screen: `instruction_text`, `block_break`, `good_bye`
  - Stimulus IDs shown together: text only (plus optional audio in human instruction page).
  - Layout anchors (`pos`): default centered anchor from PsychoPy text object.
  - Size/spacing: `height` in range `26-30`, `wrapWidth=980`, `font=SimHei`.
  - Readability checks: multiline text remains within 1280x720 bounds in QA.
  - Rationale: centered large text supports unattended passive phases and low motor demand.
- Screen: `condition_cue`
  - Stimulus IDs shown together: `condition_cue` text only.
  - Layout anchors (`pos`): centered.
  - Size/spacing: `height=36`, `wrapWidth=980`, no additional overlays.
  - Readability checks: condition label remains legible with no overlap.
  - Rationale: single-channel cue avoids pre-outcome clutter.
- Screen: `lottery_offer`
  - Stimulus IDs shown together: `lottery_offer` text only.
  - Layout anchors (`pos`): centered.
  - Size/spacing: `height=34`, `wrapWidth=980`, explicit line breaks for probability/outcome rows.
  - Readability checks: both rows visible simultaneously; no truncation in QA.
  - Rationale: deterministic text layout replaces template tokens with concrete lottery values.
- Screen: `outcome_feedback`
  - Stimulus IDs shown together: one of `outcome_win`, `outcome_neutral`, `outcome_loss`.
  - Layout anchors (`pos`): centered.
  - Size/spacing: `height=40`, `wrapWidth=980`, color-coding by valence.
  - Readability checks: value and cumulative score remain separated by line breaks.
  - Rationale: valence-coded feedback supports prediction-error interpretation.

There are no screens with multiple simultaneous choice options in this passive design.

## 6. Trigger Plan

| Trigger | Code | Semantics |
|---|---:|---|
| `exp_onset` | 1 | Experiment start |
| `exp_end` | 2 | Experiment end |
| `block_onset` | 10 | Block start |
| `block_end` | 11 | Block end |
| `gain_condition_cue_onset` / `loss_condition_cue_onset` / `mixed_condition_cue_onset` | 20/21/22 | Cue onset by condition |
| `gain_pre_lottery_fixation_onset` / `loss_pre_lottery_fixation_onset` / `mixed_pre_lottery_fixation_onset` | 30/31/32 | Anticipation fixation onset by condition |
| `gain_lottery_reveal_onset` / `loss_lottery_reveal_onset` / `mixed_lottery_reveal_onset` | 40/41/42 | Lottery reveal onset by condition |
| `gain_win_outcome_feedback_onset` ... `mixed_loss_outcome_feedback_onset` | 50-58 | Outcome feedback onset by condition and valence |
| `iti_onset` | 60 | ITI fixation onset |

## 7. Inference Log

- Decision: use passive no-response trial flow with only continue-key pages.
  - Why inference was required: selected sources describe reward/uncertainty processing but do not provide a single canonical buttonless implementation spec for this exact task package.
  - Citation-supported rationale: passive valuation framing is consistent with `W2002597000`, while cue-anticipation-outcome sequencing is aligned to `W2140531843`.
- Decision: use three lottery profiles (`gain/loss/mixed`) with deterministic profile parameters in `condition_generation` config.
  - Why inference was required: exact probability/outcome constants are not directly specified as a reusable software standard in selected papers.
  - Citation-supported rationale: profile structure operationalizes reward, punishment, and mixed expectancy contrasts from prediction-error literature (`W2140531843`, `W2035219495`).
- Decision: keep participant-facing language as Chinese with `SimHei`.
  - Why inference was required: publication protocols are language-agnostic, but deployment target requires localized instructions.
  - Citation-supported rationale: localization preserves task structure without changing trial logic or valence mapping.
- Decision: runtime unit labels and exported columns use passive-lottery phase names (`condition_cue_*`, `pre_lottery_fixation_*`, `lottery_reveal_*`, `outcome_feedback_*`, `iti_*`) instead of template residue (`cue_*`, `anticipation_*`, `target_*`, `feedback_*`).
  - Why inference was required: this is an implementation contract decision, not a paradigm manipulation.
  - Citation-supported rationale: improves traceability from literature-defined phases to runtime artifacts without changing paradigm logic.
