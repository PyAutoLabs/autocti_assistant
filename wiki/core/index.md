---
title: Core wiki — CTI reference
sources: []
last_updated: 2026-07-17
---

# Core wiki — CTI reference

The reference layer for everything an agent needs to understand about Charge
Transfer Inefficiency (CTI) and the PyAutoCTI stack when helping a user
calibrate, model, or correct it. Skills in [`../../skills/`](../../skills/) link
in here for the *what* / *which* / *why*; the *how* lives in the skills.

For the broader scientific literature — the papers behind these concepts, the
missions, and the software — see the [literature wiki](../literature/index.md).

## Concepts

- [Charge Transfer Inefficiency](./concepts/charge_transfer_inefficiency.md) —
  what CTI is, why it happens, and why it matters for precision astronomy.
- [Trap physics](./concepts/trap_physics.md) — capture and release of electrons
  by lattice defects; the volume-filling `CCDPhase` model.
- [FPR and EPER](./concepts/fpr_and_eper.md) — the anatomy of a CTI signal: the
  injected charge (First Pixel Response) and its trail (Extended Pixel Edge
  Response), and how a `Layout` locates them.
- [The arctic algorithm](./concepts/arctic_algorithm.md) — how the forward model
  clocks charge through the trap field; the `Clocker` wrapper and `express`.
- [Calibration strategy](./concepts/calibration_strategy.md) — measuring a trap
  model from calibration data (charge injection, EPER trails, trap pumping).
- [Parallel and serial CTI](./concepts/parallel_and_serial.md) — the two
  clocking directions on a CCD and how they combine in 2D.

## The stack

PyAutoCTI is built on the shared PyAuto\* libraries. The dependency chain is
**autonerves** (config) → **autoarray** (data structures) → **autofit** (model
fitting) → **autocti** (CTI). It does *not* depend on autogalaxy — that is the
lensing stack.

- **autocti** — `Clocker1D`/`Clocker2D`, trap species, `CCDPhase`,
  `CTI1D`/`CTI2D`, `Dataset1D`/`ImagingCI`, `Layout1D`/`Layout2DCI`, the
  `extract` API, per-dataset `Fit*`/`Analysis*`, and `autocti.plot`. It wraps
  the C++ **arctic** clocking code via `arcticpy`.
- **autofit** — model composition (`af.Model`/`af.Collection`), the non-linear
  search (`af.Nautilus`), and the factor graph (`af.AnalysisFactor` /
  `af.FactorGraphModel`) that fits several charge lines jointly.
- **autoarray** — the `Array1D`/`Array2D`, `Mask1D`/`Mask2D` and `Region`
  objects the datasets are built on.

Source of truth is always the installed library (`dir()` / reading the source),
then the validated `autocti_workspace` scripts — never changelogs or memory. See
[`../../skills/ac_workspace_navigation.md`](../../skills/ac_workspace_navigation.md).
