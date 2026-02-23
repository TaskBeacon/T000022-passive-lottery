# CHANGELOG

## [Unreleased]

### Changed
- Refactored `src/run_trial.py` to eliminate local duration scaling and trial ID boilerplate, using `psyflow` native `next_trial_id()`.
- Standardized ITI phase naming to `iti` instead of `inter_trial_interval`.

## [0.2.2-dev] - 2026-02-19

### Changed
- Refactored trial runtime contract in `src/run_trial.py` to passive-lottery semantic units/phases:
  - `cue/anticipation/target/feedback/inter_trial_interval` -> `condition_cue/pre_lottery_fixation/lottery_reveal/outcome_feedback/iti`.
- Added backward-compatible timing/trigger fallback logic in runtime while promoting semantic keys.
- Renamed timing keys across all configs:
  - `condition_cue_duration`, `pre_lottery_fixation_duration`, `lottery_reveal_duration`, `outcome_feedback_duration`.
- Renamed trigger keys across all configs:
  - `{condition}_condition_cue_onset`, `{condition}_pre_lottery_fixation_onset`, `{condition}_lottery_reveal_onset`, `{condition}_{outcome_kind}_outcome_feedback_onset`.
- Synchronized evidence/docs (`references/task_logic_audit.md`, `references/parameter_mapping.md`, `README.md`) with the repaired runtime contract.

## [0.2.1-dev] - 2026-02-18

### Changed
- Rebuilt `references/task_logic_audit.md` with a complete, non-placeholder state machine, explicit trigger mapping, layout plan, and inference log.
- Curated literature selection to a task-relevant subset and regenerated `references/references.yaml` plus `references/references.md`.
- Updated `references/stimulus_mapping.md` to map implemented stimulus IDs (`condition_cue`, `lottery_offer`, `outcome_*`, `fixation`) instead of abstract cue/target placeholders.
- Aligned `README.md` metadata and configuration summary with the implemented Chinese profile, trigger schema, and lottery controller parameters.

## [0.2.0-dev] - 2026-02-18

### Added
- Passive lottery scheduler in `src/utils.py` with condition-balanced trial planning and deterministic outcome sampling.

### Changed
- Rebuilt `src/run_trial.py` from MID placeholder flow to passive lottery flow: `cue -> anticipation -> target(lottery) -> feedback -> iti`.
- Updated `main.py` block execution to use `Controller.prepare_block(...)` and outcome-based block summaries.
- Replaced all task configs with Chinese, audit-friendly lottery parameters and split mode profiles.
- Updated `responders/task_sampler.py` to passive-mode behavior (continue-page response only).
- Updated `README.md` to document true task logic and runtime modes.

### Fixed
- Removed incorrect adaptive RT logic and target-hit scoring from the passive lottery task.
