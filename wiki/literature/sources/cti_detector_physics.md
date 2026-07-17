---
title: Sources — CTI detector physics
type: sources
topics: [cti, detector-physics, traps]
status: drafted
---

# Sources: CTI detector physics

The physical basis of CTI: radiation in orbit displaces silicon atoms, creating
lattice defects (**traps**) with energy levels in the band gap. A trap captures
an electron from a passing charge packet and releases it after a
characteristic delay, and the aggregate of many such capture/release events is
the CTI trail. This page backs the reference concept
[trap physics](../../core/concepts/trap_physics.md).

## Short 2013 — an analytical model of radiation-induced CTI

**Reference:** `Short2013` — MNRAS 430, 3078 — https://arxiv.org/abs/1302.1416
**Status:** drafted

Formalises radiation-induced CTI at the detector level: capture and release
governed by trap densities and emission time constants, with the crucial
**volume-filling** dependence — a trap can only capture from packets that reach
it, so the captured fraction depends non-linearly on packet size. This is the
physics the arctic forward model implements and the reason calibration data spans
several charge levels. Developed for Gaia's CCD mode and applied to Euclid.

## Massey 2010 — traps in the correction model

**Reference:** `Massey2010` — MNRAS 401, 371 — https://arxiv.org/abs/0909.0507
**Status:** drafted

The forward-model correction paper is also a working description of the trap
physics it inverts: densities, release timescales, and the well-fill behaviour
that together reproduce the observed trails. Read alongside Short 2013 for the
model that PyAutoCTI's `TrapInstantCapture` + `CCDPhase` parameterise.

## Related

- Reference: [trap physics](../../core/concepts/trap_physics.md),
  [the arctic algorithm](../../core/concepts/arctic_algorithm.md)
- [Correction algorithms](./cti_correction_algorithms.md)
