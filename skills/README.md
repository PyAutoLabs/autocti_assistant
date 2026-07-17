# skills/

Procedural how-to-do-X skills for the PyAutoCTI stack. Each skill is a single
Markdown file with YAML frontmatter; the body teaches an agent (and through them,
the user) how to write Python that accomplishes one CTI calibration task.

Skills are also exposed at `.claude/skills/` (Claude Code) and `~/.codex/skills/`
(when configured) via symlinks; the canonical files live here.

## Conventions

- File names use the `ac_<task>` convention for CTI-API skills, e.g.
  `ac_fit_cti_model.md`.
- Project-workflow skills (repo-level operations, template manipulation) use a
  plain kebab-case name, e.g. `start-new-project.md`.
- Meta-skills (writing guide, bootstrap protocol) start with `_`.
- Every CTI-API skill is **python-first**: the deliverable is a runnable `.py`
  script + the understanding to evolve it, grounded in a validated
  `autocti_workspace` example — never API memory.
- Source citations use the project-name + repo-relative-path form, e.g.
  `PyAutoCTI:autocti/clocker/`, resolved via [`../sources.yaml`](../sources.yaml).
- Wiki references use workspace-relative paths, e.g.
  `wiki/core/concepts/charge_transfer_inefficiency.md`.

## Index

The recipes below are the assistant's current CTI capability. The full growth
queue — skills, wiki pages and datasets still to be authored — is
[`../PENDING.md`](../PENDING.md); this cell was born as a lightweight seed and is
grown in use.

### Meta

- [`_style.md`](./_style.md) — writing guide every skill is authored against.
  Read first before adding or editing any skill.
- [`_bootstrap_skill.md`](./_bootstrap_skill.md) — protocol for authoring a new
  skill on demand when a user requests a capability not yet covered.

### Setup

- [`ac_setup_environment.md`](./ac_setup_environment.md) — install and verify the
  PyAutoCTI stack, **including arcticpy** (the C++ arctic clocking code `import
  autocti` needs but pip won't install). The #1 setup failure; covers the
  libgsl-dev + numpy/cython + arcticpy recipe and the numpy-downgrade trap.

### The CTI calibration pipeline

Grounded per-skill in the matching `autocti_workspace` stage; navigate the whole
catalogue with `ac_workspace_navigation`.

- [`ac_workspace_navigation.md`](./ac_workspace_navigation.md) — the map: the two
  geometries (`dataset_1d`, `imaging_ci`), their shared stage pipeline, and which
  `start_here.py` to read for any task.
- [`ac_simulate_dataset_1d.md`](./ac_simulate_dataset_1d.md) — simulate a 1D CTI
  dataset (charge lines + a known trap model) to generate ground truth.
- [`ac_simulate_imaging_ci.md`](./ac_simulate_imaging_ci.md) — simulate a 2D
  charge-injection image (the Euclid VIS / HST ACS geometry; parallel/serial CTI,
  `Clocker2D`).
- [`ac_mask_and_extract.md`](./ac_mask_and_extract.md) — mask the FPR/EPER before
  fitting, and extract FPR/EPER regions as arrays (`layout.extract.fpr/eper`).
- [`ac_fit_cti_model.md`](./ac_fit_cti_model.md) — compose a CTI model and fit it
  with a non-linear search, including the **factor graph** that fits several
  charge lines jointly. The core capability.
- [`ac_correct_cti.md`](./ac_correct_cti.md) — remove CTI from data with
  `clocker.remove_cti`, to correct science data or diagnose a calibration.
- [`ac_load_results.md`](./ac_load_results.md) — inspect a fit's `result`, and
  aggregate across many fits (`Aggregator`, `ac.agg.CTIAgg` and its generators).

### Plotting

- [`ac_plot.md`](./ac_plot.md) — the `autocti.plot` **function API**
  (the `subplot_*` / `figure_*` families, `aplt.plot_yx`, `aplt.plot_array`, `aplt.plot_cti_1d`, the
  `*_list` combined subplots). No MatPlot/Output/Visuals object.

### Project workflow

- [`start-new-project.md`](./start-new-project.md) — bridge to a standalone
  **science project** repo and its lifecycle (Create → Work → Collaborate →
  Publish).
- [`contribute-upstream.md`](./contribute-upstream.md) — prepare a scoped change
  and open a draft PR into `PyAutoLabs/autocti_assistant`.
