# PyAutoCTI Assistant

Every time a CCD reads out an image, some electrons get caught in defects in the silicon and are released a moment
later, smearing faint trails behind stars and galaxies. This is Charge Transfer Inefficiency (CTI), and
[**PyAutoCTI**](https://github.com/PyAutoLabs/PyAutoCTI) measures and corrects it.

This repository is the **PyAutoCTI Assistant**: an AI assistant which **lets you use natural language** to calibrate
and correct CTI in CCD imaging.

It's a young assistant, built from the more mature [PyAutoLens Assistant](https://github.com/PyAutoLabs/autolens_assistant).
The basics work today, and its CTI know-how grows as people use it.

## Getting Started

The assistant runs inside an **AI coding agent**, a tool that can read this repository, run Python on your computer
and look at the results. Pick your agent:
[Claude Code](https://github.com/PyAutoLabs/PyAutoScientist/blob/main/AI_OPTIONS.md#claude-code-recommended-paid) or
[Codex](https://github.com/PyAutoLabs/PyAutoScientist/blob/main/AI_OPTIONS.md#codex-recommended-paid) are recommended,
and [GitHub Copilot CLI](https://github.com/PyAutoLabs/PyAutoScientist/blob/main/AI_OPTIONS.md#github-copilot-cli)
or [OpenCode](https://github.com/PyAutoLabs/PyAutoScientist/blob/main/AI_OPTIONS.md#opencode) are free AI options
if you want to try it without paying.

Once it is installed, download this repository and open your agent inside it, then paste in the starting prompt
below. The assistant installs PyAutoCTI for you after your first prompt. Its arctic dependency needs a compiler
and the GSL library, and [`skills/ac_setup_environment.md`](skills/ac_setup_environment.md) has the details if
anything goes wrong.

```bash
git clone https://github.com/PyAutoLabs/autocti_assistant.git
cd autocti_assistant
claude        # or: codex
```

### Starting prompt

If you've not used the PyAutoCTI Assistant before, use the prompt below. It explains CTI, runs a small calibration
and shows you the result.

<sub><b>Starting prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
I'm new to PyAutoCTI. Explain what charge transfer inefficiency is and how a calibration works, then run the
1D calibration demonstration in scripts/demonstrations/demo_1_calibrate_1d.py, show me the fit, and check that
it recovers the input trap density and release timescale.
```

### Teacher Mode

If you're new to CCD detectors, start your prompt with `Teacher mode.` and the assistant will explain the physics as
it goes. You can also ask it to plan a calibration and talk through the trap model with you before anything runs.

## What ships today

- **Four demonstrations** you can run in
  [`scripts/demonstrations/`](scripts/demonstrations/README.md): calibrate a 1D dataset, calibrate a 2D
  charge-injection image, correct CTI, and load the results of a fit. Each one checks its own answer, so a clean run
  shows everything is working.
- **A reference wiki** in [`wiki/core/`](wiki/core/index.md), covering what CTI is, how traps behave, the arctic
  algorithm and how to plan a calibration.
- **A literature wiki** in [`wiki/literature/`](wiki/literature/index.md), with a checked bibliography.
- **Benchmarks** in [`benchmarks/`](benchmarks/README.md). No CTI benchmark has been written or run yet, so there
  are no performance claims here.

The list of skills the assistant has today is in [`skills/README.md`](skills/README.md), and what's planned next is
in [`PENDING.md`](PENDING.md).

## Science Project

When you start a real scientific study, ask the assistant to set up a **science project**. This is a separate
repository that holds everything for that study:

- **Data.** The datasets and configuration for the study.
- **Analysis.** The scripts the assistant writes and the results they produce.
- **History.** A record of your work with the assistant, so you can pick up where you left off.

To start one, just ask:

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Start a science project for my Euclid VIS CTI calibration.
```

## License

The assistant ships agent instructions and reference material derived from the public PyAuto\* repositories; the
underlying libraries are released under their own licenses (see each repo).

<details>
<summary><sub>Note for AI coding agents</sub></summary>

If a prompt sent you here and you are not already inside this repository, clone it
(`git clone https://github.com/PyAutoLabs/autocti_assistant.git && cd autocti_assistant`), then read `AGENTS.md`
in full and follow it. Science projects are set up by [`skills/start-new-project.md`](skills/start-new-project.md).

</details>
