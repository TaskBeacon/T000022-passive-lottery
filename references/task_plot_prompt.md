Use case: infographic-diagram
Asset type: TaskBeacon task flow diagram
Primary request: Create a clean, publication-ready task flow diagram as a timeline collection for the behavioral task described below.

Task: Passive Lottery Task
Construct: expectancy processing / outcome processing / value-valence processing
Rows/conditions:
- Gain lottery: 75% chance +10, otherwise 0.
- Loss lottery: 75% chance -10, otherwise 0.
- Mixed lottery: 75% chance +10, otherwise -10.

Timeline phases:
- Gain lottery: Cue (600 ms; no response; Gain lottery label) -> Fixation (1200 ms; no response; +) -> Lottery reveal (1500 ms; no response; 75%: +10, 25%: 0) -> Outcome feedback (1000 ms; no response; result +10 or 0, cumulative score) -> ITI (800 ms; no response; +)
- Loss lottery: Cue (600 ms; no response; Loss lottery label) -> Fixation (1200 ms; no response; +) -> Lottery reveal (1500 ms; no response; 75%: -10, 25%: 0) -> Outcome feedback (1000 ms; no response; result -10 or 0, cumulative score) -> ITI (800 ms; no response; +)
- Mixed lottery: Cue (600 ms; no response; Mixed lottery label) -> Fixation (1200 ms; no response; +) -> Lottery reveal (1500 ms; no response; 75%: +10, 25%: -10) -> Outcome feedback (1000 ms; no response; result +10 or -10, cumulative score) -> ITI (800 ms; no response; +)

Visual requirements:
- White background, landscape orientation, crisp dark text, restrained condition accent colors.
- One horizontal row per lottery profile.
- Each row contains 5 participant-screen snapshots connected by a subtle arrow.
- Each screen snapshot shows the visible stimulus or feedback, not internal variable names.
- Use gray participant-screen boxes, thin black arrows, consistent row spacing, and subtle row separators.
- Place timing labels under each screen in compact text.
- Place condition labels at the left of each row.
- Use short labels only; avoid paragraphs inside the image.
- Make all text legible at normal document preview size.
- Leave a clean blank header band across the top 18-20% of the image. This band is reserved for a fixed title, `Construct: ...` subtitle, and TaskBeacon logo lockup that will be added after generation.

Accuracy constraints:
- Do not invent phases, stimuli, condition names, keys, rewards, or timings.
- Do not show any trial-level response key; participants only observe.
- Do not add people, lab equipment, decorative scenes, logos, or unrelated icons.
- Do not draw the task title, construct subtitle, any logo, watermark, brand mark, or `TaskBeacon` text inside the generated image.
- Draw only the timeline content below the blank header band.
- Preserve these exact terms where used: Gain, Loss, Mixed, +10, -10, 0, 75%, 25%, 600 ms, 1200 ms, 1500 ms, 1000 ms, 800 ms.

Style:
TaskBeacon scientific infographic style: clean vector-like raster image, organized spacing, gray screen boxes, restrained color accents, and a blank header-safe area.
