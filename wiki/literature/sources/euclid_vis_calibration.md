---
title: Sources — Euclid VIS CTI calibration
type: sources
topics: [cti, euclid, calibration]
status: drafted
---

# Sources: Euclid VIS CTI calibration

Euclid's visible imager (VIS) is a weak-lensing instrument, so CTI is a headline
systematic (see [CTI as a shape bias](./cti_shape_bias.md)), and its in-flight
CTI calibration programme is the modern context PyAutoCTI is built for. See the
entity page [Euclid VIS](../entities/euclid_vis.md).

## Short 2013 — the analytical CTI model

**Reference:** `Short2013` — MNRAS 430, 3078 — https://arxiv.org/abs/1302.1416
**Status:** drafted

A generalised analytical model of radiation-induced CTI for CCD detectors,
developed for the Gaia CCD operating mode and applied to assess radiation damage
for Euclid. It formalises the capture/release-with-volume-filling picture that
the arctic forward model implements, and is a standard reference for the
detector-level CTI model behind both missions.

## Israel 2015 — correction requirements for a lensing mission

**Reference:** `Israel2015` — MNRAS 453, 561 — https://arxiv.org/abs/1506.07831
**Status:** drafted

Quantifies how imperfect trap-model knowledge propagates into residual shape and
photometry bias under iterative correction — i.e. how precisely a Euclid-class
calibration must measure the trap model. This is the requirements-side companion
to the correction algorithm itself; see
[correction algorithms](./cti_correction_algorithms.md).

## Skottfelt 2017 — trap pumping for the VIS detector

**Reference:** `Skottfelt2017` — JINST 12, C12033 — https://ui.adsabs.harvard.edu/abs/2017JInst..12C2033S
**Status:** drafted

Trap-pumping schemes for the Euclid CCD273 detector — the in-orbit calibration
technique that locates and characterises individual traps (density, emission time
constants, sub-pixel position). See [trap pumping](./trap_pumping.md).

## Related

- Entity: [Euclid VIS](../entities/euclid_vis.md)
- [CTI as a shape bias](./cti_shape_bias.md) · [Trap pumping](./trap_pumping.md)
