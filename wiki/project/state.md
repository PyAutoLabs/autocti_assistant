---
title: Project state
type: state
last_touched: 2026-08-28
---

# Project state

The head pointer for work in this clone — read first, every session, before the journal.
Rewritten each session, never appended (`_state_template.md` is the shape). Today it holds
no science project of its own, so it records the state of the **stack and this assistant**,
which is what an arriving session most needs to know.

## Science goal

CTI (charge transfer inefficiency) calibration and modelling for CCD imaging — the
instrument-calibration half of the PyAuto stack (Euclid VIS and HST ACS heritage; see the
[literature wiki](../literature/index.md)). No standalone science project has been
scaffolded from this clone yet; when one is, `start-new-project` gives it its own `state.md`
and this file goes back to describing only the assistant.

## Data on hand

The bundled examples under `dataset/`, plus the historical calibration material in
**`autocti_workspace_test/legacy/`** — `euclid/`, `tvac/` (thermal-vacuum test campaign),
`temporal/`, `validation/`, `config_2023/`. Treat `legacy/` as heritage reference, not as
current runnable examples; the modern equivalents are under `autocti_workspace/scripts/`.

## Where we are now

- **The stack is modern.** PyAutoCTI, `autocti_workspace` and `autocti_workspace_test` were
  brought fully up to date in the **CTI resurrection epic** — all six phases merged
  2026-07-17. The API taught by the skills and reference wiki is the post-resurrection API.
- All 118 `autocti_workspace` scripts were validated in that epic; they are the canonical
  examples the skills adapt.
- **This assistant** was born 2026-07-17 as a **lightweight-seed** clone of
  `autolens_assistant` (Clone Agent; PyAutoBrain#136). Born **private**; it flips public only
  after its Heart newborn-validation legs pass.

## In flight

- _nothing running_

## Open, carried forward

- **The release train is not wired.** `PyAutoMind:draft/release/autocti/cti_release_train_wiring.md`
  is formalised but **unstarted and human-required** — it touches the nightly's most dangerous
  machinery and needs a TestPyPI rehearsal in its own session.
- The queue of skills, wiki pages and datasets still to author is [`../../PENDING.md`](../../PENDING.md).

## Traps — don't repeat

- **PyPI serves a pre-resurrection wheel** (`autocti 2024.11.13.2`). Installing the modern
  stack means installing from **source** (the `main` checkouts), not `pip install autocti`.
  This is why [`ac_setup_environment`](../../skills/ac_setup_environment.md) and the
  `wiki-currency` CI both install from source, and why grading docs against the released
  wheel would be vacuous. Do not assume `pip install autocti` gives a current stack until the
  release train ships its first modern version.
- Never ground the API against pre-2026 examples or memory — use the installed source and the
  validated `autocti_workspace` scripts.

## Journal index

- _no entries yet_
