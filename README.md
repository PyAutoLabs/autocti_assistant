# PyAutoCTI Assistant

This repository is the **PyAutoCTI Assistant**: an AI assistant which **lets you use natural language** to calibrate
and correct Charge Transfer Inefficiency (CTI) in CCD imaging with
[PyAutoCTI](https://github.com/PyAutoLabs/PyAutoCTI) — trap models clocked through the arctic algorithm, charge-injection
and 1D datasets, FPR/EPER extraction, and Bayesian calibration of trap densities and release timescales.

It was born as a **lightweight seed** of the mature sibling [autolens_assistant](https://github.com/PyAutoLabs/autolens_assistant):
the agent instructions, skills framework, reference wiki and benchmark machinery are in place, and the CTI-specific
skills grow in use — [`PENDING.md`](PENDING.md) is the growth queue and [`skills/README.md`](skills/README.md) the
index of what exists today.

## Getting Started

The assistant runs inside an **AI coding agent** — a tool that reads this repository, executes Python on your computer
and inspects the results. That is what lets it install PyAutoCTI and its arctic dependency, run calibrations and look at
the trails they produce. You do not have to run anything to use it: asking what CTI is, planning a calibration or
learning in Teacher Mode all happen inside the same agent.

1. **Choose Claude Code or Codex.** These are the two recommended agents and the ones the assistant is developed and
   tested against. Their setup pages live in the sibling assistant and apply here with this repository's URL:
   [Claude Code](https://github.com/PyAutoLabs/autolens_assistant/blob/main/docs/setup/claude_code.md) ·
   [Codex](https://github.com/PyAutoLabs/autolens_assistant/blob/main/docs/setup/codex_cli.md). For sustained
   scientific work expect to pay for one of them, but how depends on your situation: a personal subscription, access
   through your institution or team, or usage-based API billing. Check the provider's current plans rather than
   assuming a subscription is the only route. Desktop and IDE versions of either agent are fine, provided they can read
   this repository and execute code.
2. **Open the assistant workspace.** Clone this repository and start the agent inside it — the instructions load
   automatically, and the assistant sets up the PyAutoCTI stack (including arcticpy, which needs a compiler and GSL
   headers — see [`skills/ac_setup_environment.md`](skills/ac_setup_environment.md)) after your first prompt:

   ```bash
   git clone https://github.com/PyAutoLabs/autocti_assistant.git
   cd autocti_assistant
   claude        # or: codex
   ```

3. **Submit the starting prompt:**

   ```
   I'm new to PyAutoCTI. Explain what charge transfer inefficiency is and how a calibration works, then run the
   1D calibration demonstration in scripts/demonstrations/demo_1_calibrate_1d.py, show me the fit, and check that
   it recovers the input trap density and release timescale.
   ```

Start the prompt with `Teacher mode.` if you want the detector physics explained as you go, or ask it to plan a
calibration and discuss the trap model before anything runs.

## Experimental alternatives

**OpenCode** is an open-source coding agent whose *client* is free. Model access is separate: you connect it to a
provider, and the cost, capability and availability of the model are the provider's, not OpenCode's; free models are
often limited-time offerings, and not every model can drive the assistant (it must handle multi-step tool use and be
able to look at figures). **No free provider/model configuration has yet been validated against any PyAuto assistant**,
so treat OpenCode as compatible rather than tested. Setup and caveats are on the sibling assistant's
[OpenCode page](https://github.com/PyAutoLabs/autolens_assistant/blob/main/docs/setup/opencode_cli.md); use this
repository's URL.

Browser chats with a GitHub connector are **not supported**. Maintainer-facing notes on evaluating further agents are
in the sibling assistant's
[`docs/evaluation/agent_evaluation.md`](https://github.com/PyAutoLabs/autolens_assistant/blob/main/docs/evaluation/agent_evaluation.md).

## What ships today

- **Four runnable demonstrations** under [`scripts/demonstrations/`](scripts/demonstrations/README.md): calibrate a 1D
  dataset and a 2D charge-injection image (recovering the input traps), correct CTI, and reload a fit through the
  aggregator. Each asserts its result, so a clean run is proof the pipeline works.
- **The reference wiki**, [`wiki/core/`](wiki/core/index.md) — what CTI is, trap physics, FPR/EPER, the arctic
  algorithm and calibration strategy — and the **literature wiki**, [`wiki/literature/`](wiki/literature/index.md),
  with a verified bibliography.
- **Benchmark machinery** under [`benchmarks/`](benchmarks/README.md); no CTI benchmark card has been written or run
  yet, so there is no performance claim here to believe or disbelieve.

## Science Project

When you begin a specific study, the assistant can create a dedicated **science project**: a separate, structured
repository holding that study's datasets, configuration, analysis scripts, results and the record of your work with
the assistant. The workflow is owned by the [`start-new-project`](skills/start-new-project.md) skill:

```
Start a science project for my Euclid VIS CTI calibration.
```

## License

The assistant ships agent instructions and reference material derived from the public PyAuto\* repositories; the
underlying libraries are released under their own licenses (see each repo).
