# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| `P001` | `task.conditions` | `['gain', 'loss', 'mixed']` | `W2140531843` | Methods: reward, punishment, and mixed valence contexts are modeled with cue-conditioned outcomes. | inferred | Condition labels are implementation tokens; participant labels come from config profiles. |
| `P002` | `task.total_blocks` | `3` | `W2140531843` | Blocked cue-outcome structure is used in protocol framing. | inferred | Human profile; QA/sim profiles are shortened for gating speed. |
| `P003` | `task.trial_per_block` | `24` | `W2140531843` | Repeated trial sampling per condition family is required to estimate valence effects. | inferred | With 3 blocks gives 72 trials total. |
| `P004` | `task.total_trials` | `72` | `W2140531843` | Trial repetition for PE contrast estimation is required by paradigm intent. | inferred | Derived from blocks x trials-per-block. |
| `P005` | `task.key_list` | `['space']` | `W2002597000` | Passive-viewing framing does not require trial-level choice response. | cited | Continue key is only for page transitions. |
| `P006` | `timing.condition_cue_duration` | `0.6` | `W2140531843` | Cue phase precedes anticipation and outcome in fixed sequence. | inferred | Duration value is implementation-level and documented as inferred. |
| `P007` | `timing.pre_lottery_fixation_duration` | `1.2` | `W2140531843` | Anticipation period separates cue from reveal/outcome. | inferred | Fixed-duration fixation. |
| `P008` | `timing.lottery_reveal_duration` | `1.5` | `W2140531843` | Lottery information is displayed before outcome feedback. | inferred | Reveals probability and outcome pair. |
| `P009` | `timing.outcome_feedback_duration` | `1.0` | `W2140531843` | Outcome phase is explicit and valence-sensitive in PE design. | inferred | Uses `outcome_win`, `outcome_neutral`, `outcome_loss` screens. |
| `P010` | `timing.iti_duration` | `0.8` | `W2035219495` | Trials are segmented by ITI for event-level modelability. | inferred | Fixed ITI for simpler event timing. |
| `P011` | `condition_generation.lottery_profiles.gain` | `prob_a=0.75; outcomes=[10,0]` | `W2140531843` | Reward-context trials contain positive/neutral outcomes. | inferred | Concrete numeric constants are implementation-level inferences. |
| `P012` | `condition_generation.lottery_profiles.loss` | `prob_a=0.75; outcomes=[-10,0]` | `W2140531843` | Punishment-context trials contain negative/neutral outcomes. | inferred | Mirrors gain profile probability with opposite valence. |
| `P013` | `condition_generation.lottery_profiles.mixed` | `prob_a=0.5; outcomes=[10,-10]` | `W2140531843` | Mixed context contrasts positive and negative outcomes. | inferred | Balanced mixed profile. |
| `P014` | `triggers.map.exp_onset` / `triggers.map.exp_end` | `1` / `2` | `W2140531843` | Session boundary markers support event auditability. | implementation | Contract-level trigger namespace. |
| `P015` | `triggers.map.block_onset` / `triggers.map.block_end` | `10` / `11` | `W2140531843` | Block boundary markers are needed for segmented runs. | implementation | Shared across conditions. |
| `P016` | `triggers.map.gain_condition_cue_onset` / `loss` / `mixed` | `20` / `21` / `22` | `W2140531843` | Cue phase is condition-indexed. | implementation | Condition-specific cue markers. |
| `P017` | `triggers.map.gain_pre_lottery_fixation_onset` / `loss` / `mixed` | `30` / `31` / `32` | `W2140531843` | Anticipation phase is condition-indexed. | implementation | Mirrors cue mapping family. |
| `P018` | `triggers.map.gain_lottery_reveal_onset` / `loss` / `mixed` | `40` / `41` / `42` | `W2140531843` | Lottery reveal phase is condition-indexed. | implementation | One code per condition. |
| `P019` | `triggers.map.*_outcome_feedback_onset` | `50-58` | `W2140531843` | Outcome phase must distinguish both condition and valence. | implementation | Encodes gain/loss/mixed x win/neutral/loss. |
| `P020` | `triggers.map.iti_onset` | `60` | `W2140531843` | ITI onset is a standalone event in the trial model. | implementation | Common ITI trigger for all trials. |
