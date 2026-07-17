---
name: ac_workspace_navigation
description: Navigate the autocti_workspace script catalogue — the two dataset geometries (dataset_1d, imaging_ci), the per-geometry pipeline (simulators → modeling → correction → results), the overview tour, and where to find the validated example for any CTI task. Read this to locate the right start_here.py to adapt.
---

# Navigating autocti_workspace

Every CTI capability the assistant teaches is grounded in a **validated
workspace script**, not API memory. This skill is the map: given a task, it
tells you which script is the canonical example to read and adapt. When you're
about to write CTI code, check here (or the workspace's `llms.txt` / index)
first — an existing `start_here.py` almost always covers it.

`autocti_workspace` (clone into gitignored `sources/` if not installed) is
organised by **dataset geometry**, each with the same pipeline of stages.

## The two geometries

- **`scripts/dataset_1d/`** — 1D CTI data: a line of pixels with an injected
  charge signal. The simplest calibration geometry; start here to learn the API.
- **`scripts/imaging_ci/`** — 2D charge-injection imaging: the real-instrument
  geometry (Euclid VIS, HST ACS), with parallel and serial clocking directions.

## The per-geometry pipeline

Both geometries share the same stage folders, each with a `start_here.py`:

| Stage | Folder | Skill |
|-------|--------|-------|
| Simulate a dataset with a known trap model | `simulators/` | [`ac_simulate_dataset_1d`](./ac_simulate_dataset_1d.md) · [`ac_simulate_imaging_ci`](./ac_simulate_imaging_ci.md) |
| Compose + fit a CTI model | `modeling/` | [`ac_fit_cti_model`](./ac_fit_cti_model.md) |
| Correct CTI from data | `correction/` | [`ac_correct_cti`](./ac_correct_cti.md) |
| Inspect results / aggregate | `results/` | [`ac_load_results`](./ac_load_results.md) |
| Extract FPR/EPER regions | `extract.py` | [`ac_mask_and_extract`](./ac_mask_and_extract.md) |

Within `modeling/` and `simulators/`, an `examples/` (or `features/`) subfolder
holds variants: multi-species models, non-uniform injection, cosmic rays,
serial CTI, temporal variation. `advanced/` holds chaining pipelines and the
database/aggregator cookbook.

## Where to start reading

- **New to CTI?** `scripts/overview/overview_1_what_is_cti.py` through
  `overview_6_cti_calibration.py` are a narrated tour — what CTI is, parallel vs
  serial, charge-injection data, fitting, and calibration end-to-end.
- **A specific task?** Go straight to that stage's `start_here.py` in the
  matching geometry, then its `examples/` for the closest variant.
- **Plotting?** `scripts/plot/start_here.py` and [`ac_plot`](./ac_plot.md).

## Adapting a script

The workspace scripts are written in the PyAutoCTI **workspace style** (a
title-underlined docstring, `"""__Section__"""` dividers with physics framing,
`<Project>:<path>` citations). When you generate a script for a user, match that
style and cite the workspace example you adapted — see
[`_style.md`](./_style.md) "Generated script style".

## Further reading

- `autocti_workspace:README.rst` and `scripts/overview/` — the guided entry.
- `PyAutoCTI:AGENTS.md` — the library's own map of `Clocker`, `Fit*`,
  `Analysis*`, `extract/`, and the instrument heritage.
