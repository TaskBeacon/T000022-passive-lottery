from contextlib import nullcontext
from functools import partial
from pathlib import Path

import pandas as pd
from psychopy import core

from psyflow import (
    BlockUnit,
    StimBank,
    StimUnit,
    SubInfo,
    TaskRunOptions,
    TaskSettings,
    context_from_config,
    count_down,
    initialize_exp,
    initialize_triggers,
    load_config,
    parse_task_run_options,
    runtime_context,
)

from src import ScoreTracker, generate_passive_lottery_conditions, run_trial

MODES = ("human", "qa", "sim")
DEFAULT_CONFIG_BY_MODE = {
    "human": "config/config.yaml",
    "qa": "config/config_qa.yaml",
    "sim": "config/config_scripted_sim.yaml",
}


def run(options: TaskRunOptions):
    """Run Passive Lottery Task in human/qa/sim mode with one auditable flow."""
    task_root = Path(__file__).resolve().parent
    cfg = load_config(str(options.config_path), extra_keys=["condition_generation"])
    
    output_dir: Path | None = None
    runtime_scope = nullcontext()
    runtime_ctx = None
    if options.mode in ("qa", "sim"):
        runtime_ctx = context_from_config(task_dir=task_root, config=cfg, mode=options.mode)
        output_dir = runtime_ctx.output_dir
        runtime_scope = runtime_context(runtime_ctx)

    with runtime_scope:
        # 2. Collect subject info
        if options.mode == "qa":
            subject_data = {"subject_id": "qa"}
        elif options.mode == "sim":
            participant_id = "sim"
            if runtime_ctx is not None and runtime_ctx.session is not None:
                participant_id = str(runtime_ctx.session.participant_id or "sim")
            subject_data = {"subject_id": participant_id}
        else:
            subform = SubInfo(cfg["subform_config"])
            subject_data = subform.collect()

        # 3. Load task settings
        settings = TaskSettings.from_dict(cfg["task_config"])
        if options.mode in ("qa", "sim") and output_dir is not None:
            settings.save_path = str(output_dir)
        settings.add_subinfo(subject_data)

        # In QA mode, force deterministic artifact locations.
        if options.mode == "qa" and output_dir is not None:
            output_dir.mkdir(parents=True, exist_ok=True)
            settings.res_file = str(output_dir / "qa_trace.csv")
            settings.log_file = str(output_dir / "qa_psychopy.log")
            settings.json_file = str(output_dir / "qa_settings.json")

        # 4. Task-specific condition generation settings (no task controller object)
        condition_generation = cfg.get("condition_generation_config", {})

        # 5. Setup triggers
        settings.triggers = cfg["trigger_config"]
        trigger_runtime = initialize_triggers(mock=True) if options.mode in ("qa", "sim") else initialize_triggers(cfg)

        # 6. Set up window & input
        win, kb = initialize_exp(settings)

        # 7. Setup stimulus bank
        stim_bank = StimBank(win, cfg["stim_config"])
        if options.mode not in ("qa", "sim"):
            stim_bank = stim_bank.convert_to_voice("instruction_text")
        stim_bank = stim_bank.preload_all()

        # 8. Setup score tracker
        score_tracker = ScoreTracker(initial_score=int(getattr(settings, "initial_score", 0)))

        trigger_runtime.send(settings.triggers.get("exp_onset"))

        # Instruction
        instr = StimUnit("instruction_text", win, kb, runtime=trigger_runtime).add_stim(
            stim_bank.get("instruction_text")
        )
        if options.mode not in ("qa", "sim"):
            instr.add_stim(stim_bank.get("instruction_text_voice"))
        instr.wait_and_continue()

        all_data = []
        for block_i in range(settings.total_blocks):
            if options.mode not in ("qa", "sim"):
                count_down(win, 3, color="black")

            block = (
                BlockUnit(
                    block_id=f"block_{block_i}",
                    block_idx=block_i,
                    settings=settings,
                    window=win,
                    keyboard=kb,
                )
                .generate_conditions(
                    func=generate_passive_lottery_conditions,
                    n_trials=int(settings.trials_per_block),
                    condition_labels=list(getattr(settings, "conditions", [])),
                    seed=int(settings.block_seed[block_i]),
                    seed_offset=int(condition_generation.get("seed", 2026)) + int(block_i) * 1009,
                    lottery_profiles=dict(condition_generation.get("lottery_profiles", {})),
                    enable_logging=bool(condition_generation.get("enable_logging", True)),
                )
                .on_start(lambda b: trigger_runtime.send(settings.triggers.get("block_onset")))
                .on_end(lambda b: trigger_runtime.send(settings.triggers.get("block_end")))
                .run_trial(
                    partial(
                        run_trial,
                        stim_bank=stim_bank,
                        score_tracker=score_tracker,
                        trigger_runtime=trigger_runtime,
                        block_id=f"block_{block_i}",
                        block_idx=block_i,
                    )
                )
                .to_dict(all_data)
            )

            block_trials = block.get_all_data()
            block_score = sum(int(trial.get("outcome_value", 0)) for trial in block_trials)
            win_rate = (
                sum(1 for trial in block_trials if str(trial.get("outcome_kind", "")) == "win") / len(block_trials)
                if block_trials
                else 0.0
            )
            
            StimUnit("block", win, kb, runtime=trigger_runtime).add_stim(
                stim_bank.get_and_format(
                    "block_break",
                    block_num=block_i + 1,
                    total_blocks=settings.total_blocks,
                    win_rate=win_rate,
                    block_score=block_score,
                    total_score=score_tracker.total_score,
                )
            ).wait_and_continue()

        final_score = int(score_tracker.total_score)
        StimUnit("goodbye", win, kb, runtime=trigger_runtime).add_stim(
            stim_bank.get_and_format("good_bye", total_score=final_score)
        ).wait_and_continue(terminate=True)

        trigger_runtime.send(settings.triggers.get("exp_end"))

        df = pd.DataFrame(all_data)
        df.to_csv(settings.res_file, index=False)

        trigger_runtime.close()
        core.quit()


def main() -> None:
    task_root = Path(__file__).resolve().parent
    options = parse_task_run_options(
        task_root=task_root,
        description="Run Passive Lottery Task in human/qa/sim mode.",
        default_config_by_mode=DEFAULT_CONFIG_BY_MODE,
        modes=MODES,
    )
    run(options)


if __name__ == "__main__":
    main()
