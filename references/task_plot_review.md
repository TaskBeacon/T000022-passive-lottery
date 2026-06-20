# Task Plot Review

## Evidence Match

- Pass: title and construct match the passive lottery-viewing task.
- Pass: rows match configured gain, loss, and mixed lottery profiles.
- Pass: phase order matches README and `src/run_trial.py`: Cue -> Fixation -> Lottery reveal -> Outcome feedback -> ITI.
- Pass: timing labels match config: 600 ms cue, 1200 ms fixation, 1500 ms reveal, 1000 ms feedback, 800 ms ITI.
- Pass: no trial-level response key is shown, matching the passive task design.
- Pass: outcome feedback shows realized result and cumulative score.

## Visual Quality

- Pass: labels and timings are readable.
- Pass: generated timeline content stays below the header band.
- Pass: fixed title and Construct subtitle are centered.
- Pass: top-right TaskBeacon logo lockup is borderless and non-overlapping.
- Pass: no generated title, logo, watermark, people, devices, or decorative scene is present.

## README Embed

- Pass: `README.md` contains `## 2. Task Flow`.
- Pass: the section embeds `![Task Flow](task_flow.png)`.
- Pass: final image is saved as `task_flow.png`; raw timeline is saved as `references/task_plot_timeline_raw.png`.
