# Stimulus Mapping

Task: `Passive Lottery Task`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `gain` | `condition_cue`, `fixation`, `lottery_offer`, `outcome_win`, `outcome_neutral` | `W2140531843` | Methods describe condition-specific cue, anticipation interval, and valence-dependent outcome feedback in reward/punishment prediction-error trials. | `psychopy_builtin` | Gain profile is rendered via controller profile values (`prob_a=0.75`, outcomes `+10/0`); exact numeric values are marked `inferred` in parameter mapping. |
| `loss` | `condition_cue`, `fixation`, `lottery_offer`, `outcome_loss`, `outcome_neutral` | `W2140531843` | Same cue-to-outcome state structure is used for punishment-context trials with negative or neutral outcomes. | `psychopy_builtin` | Loss profile uses `prob_a=0.75`, outcomes `-10/0`; cue label is participant-facing text from controller config. |
| `mixed` | `condition_cue`, `fixation`, `lottery_offer`, `outcome_win`, `outcome_loss` | `W2140531843` | Mixed-valence prediction context follows the same anticipatory and feedback timeline while sampling positive vs negative outcomes. | `psychopy_builtin` | Mixed profile uses `prob_a=0.5`, outcomes `+10/-10`; no raw internal condition tokens are shown to participants. |
| `all_conditions` | `instruction_text`, `block_break`, `good_bye` | `W2002597000` | Passive-viewing paradigms support non-choice framing and instruction-driven observation without trial-level motor response. | `psychopy_builtin` | Continue-key pages are outside trial scoring and are shared across all conditions. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives in config.
- `generated_reference_asset`: task-specific synthetic assets generated from reference-described stimulus rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
