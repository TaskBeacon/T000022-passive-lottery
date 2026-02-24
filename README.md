# Passive Lottery Task

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field | Value |
|---|---|
| Name | Passive Lottery Task |
| Version | v0.2.3-dev |
| URL / Repository | https://github.com/TaskBeacon/T000022-passive-lottery |
| Short Description | Passive observation task for gain/loss/mixed lottery outcomes with deterministic profile-driven sampling. |
| Created By | TaskBeacon |
| Date Updated | 2026-02-24 |
| PsyFlow Version | 0.1.9 |
| PsychoPy Version | 2025.1.1 |
| Modality | Behavior |
| Language | Chinese |
| Voice Name | zh-CN-YunyangNeural (voice disabled by default) |

## 1. Task Overview

In this task, participants passively observe lottery cues, offer displays, and outcome feedback without making trial-level responses. The paradigm includes gain, loss, and mixed lotteries and is suitable for studying expectancy and outcome processing without action-selection confounds.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|---|---|
| 1. Prepare block schedule | Custom condition generation builds balanced, randomized trial sequences and pre-sampled outcomes. |
| 2. Execute trials | `BlockUnit(...).run_trial(...)` executes each planned trial. |
| 3. Block summary | Block hit rate, block score, and cumulative score are displayed. |

### Trial-Level Flow

| Step | Description |
|---|---|
| Condition cue | Condition cue (gain/loss/mixed) is displayed. |
| Pre-lottery fixation | Central fixation stage. |
| Lottery reveal | Trial-specific probability and outcomes are shown. |
| Outcome feedback | Realized outcome and cumulative score are shown. |
| Inter-trial interval | Fixed fixation interval before next trial. |

### Controller Logic

| Component | Description |
|---|---|
| Architecture note | No task controller object is used; `condition_generation` defines lottery profiles/sampling and a `ScoreTracker` accumulates score. |
| Condition balancing | Gain/loss/mixed conditions are balanced across trials. |
| Outcome sampling | Trial outcome is sampled from profile probabilities. |
| Score accumulation | Trial deltas and cumulative score are tracked. |

### Runtime Context Phases

| Phase Label | Meaning |
|---|---|
| `condition_cue` | Condition cue stage. |
| `pre_lottery_fixation` | Pre-offer fixation stage. |
| `lottery_reveal` | Lottery information display stage. |
| `outcome_feedback` | Outcome feedback stage. |
| `iti` | ITI stage. |

## 3. Configuration Summary

### a. Subject Info

| Field | Meaning |
|---|---|
| `subject_id` | Participant identifier. |

### b. Window Settings

| Parameter | Value |
|---|---|
| `size` | `[1280, 720]` |
| `units` | `pix` |
| `screen` | `0` |
| `bg_color` | `gray` |
| `fullscreen` | `false` |
| `monitor_width_cm` | `35.5` |
| `monitor_distance_cm` | `60` |

### c. Stimuli

| Name | Type | Description |
|---|---|---|
| `condition_cue` | text | Condition-specific cue label from `condition_generation.lottery_profiles`. |
| `lottery_offer` | text | Lottery probability-outcome display with two possible outcomes. |
| `outcome_win` / `outcome_neutral` / `outcome_loss` | text | Valence-specific outcome feedback screens with cumulative score. |
| `fixation` | text | Central fixation marker. |
| `block_break` / `good_bye` | text | Block and final summary pages. |

### d. Timing

| Phase | Duration |
|---|---|
| condition_cue | 0.6 s |
| pre_lottery_fixation | 1.2 s |
| lottery_reveal | 1.5 s |
| outcome_feedback | 1.0 s |
| iti | 0.8 s |

### e. Triggers

| Group | Trigger Codes |
|---|---|
| Experiment | `exp_onset=1`, `exp_end=2` |
| Block | `block_onset=10`, `block_end=11` |
| Condition cue by condition | `gain/loss/mixed: 20/21/22` |
| Pre-lottery fixation by condition | `gain/loss/mixed: 30/31/32` |
| Lottery reveal by condition | `gain/loss/mixed: 40/41/42` |
| Outcome feedback by condition x valence | `50-58` |
| Inter-trial interval | `iti_onset=60` |

### f. Lottery Profiles (`condition_generation`)

| Profile | Probability of Outcome A | Outcome A | Outcome B |
|---|---:|---:|---:|
| `gain` | 0.75 | +10 | 0 |
| `loss` | 0.75 | -10 | 0 |
| `mixed` | 0.50 | +10 | -10 |

## 4. Methods (for academic publication)

Participants completed a passive lottery-viewing task in which each trial presented condition cue, fixation, lottery information, and outcome feedback. No decision response was required, allowing isolation of expectancy and outcome-related processing.

Lottery profiles covered gain, loss, and mixed valence conditions with distinct probability-outcome mappings. Trial logs included condition, realized outcome type, outcome value, and cumulative score, supporting behavioral and neurocognitive analyses of value and valence processing.

The task supports aligned `human`, `qa`, and `sim` execution with standardized trial context instrumentation.
