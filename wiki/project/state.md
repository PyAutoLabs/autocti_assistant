---
title: CTI project state
type: state
last_touched: 2026-07-17
---

# CTI project state

The durable, project-level facts an agent should know about the state of
PyAutoCTI and this assistant. (This is the *project* state; the on-demand *user*
profile — who is working here and their background — lives in `profile.md`,
created from `_profile_template.md` when a user volunteers context.)

## The stack is modern (the CTI resurrection)

PyAutoCTI, `autocti_workspace`, and `autocti_workspace_test` were brought fully
up to date in the **CTI resurrection epic** — all six phases merged 2026-07-17.
Consequences the assistant must respect:

- The API taught by the skills and reference wiki is the **post-resurrection**
  API. Ground against the installed source and the validated
  `autocti_workspace` scripts, never against pre-2026 examples or memory.
- All 118 `autocti_workspace` scripts were validated in that epic; they are the
  canonical examples the skills adapt.

## What is NOT wired: the release train

**PyAutoCTI is not on the modern release train.** The wiring task
(`PyAutoMind:draft/release/autocti/cti_release_train_wiring.md`) is a formalised
but **unstarted, human-required** job — it touches the nightly's most dangerous
machinery and needs a TestPyPI rehearsal in its own session. Consequences:

- **PyPI serves a pre-resurrection wheel** (`autocti 2024.11.13.2`). Installing
  the modern stack means installing from **source** (the `main` checkouts), not
  `pip install autocti`. This is why
  [`ac_setup_environment`](../../skills/ac_setup_environment.md) and the
  `wiki-currency` CI both install from source, and why grading docs against the
  released wheel would be vacuous.
- Do not assume a `pip install autocti` gives a current stack until the release
  train ships its first modern version.

## Euclid / instrument heritage

CTI's scientific home is instrument calibration — Euclid VIS and HST ACS (see the
[literature wiki](../literature/index.md)). Historical calibration material lives
in **`autocti_workspace_test/legacy/`**: `euclid/`, `tvac/` (thermal-vacuum test
campaign), `temporal/`, `validation/`, and `config_2023/`. Treat it as heritage
reference, not as current runnable examples — the modern equivalents are under
`autocti_workspace/scripts/`.

## This assistant

`autocti_assistant` was born 2026-07-17 as a **lightweight-seed** clone of
`autolens_assistant` (Clone Agent; PyAutoBrain#136). It grows in use — the queue
of skills, wiki pages and datasets still to author is
[`../../PENDING.md`](../../PENDING.md). Born **private**; it flips public only
after its Heart newborn-validation legs pass.
