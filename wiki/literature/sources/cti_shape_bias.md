---
title: Sources — CTI as a weak-lensing shape bias
type: sources
topics: [cti, weak-lensing, systematics]
status: drafted
---

# Sources: CTI as a weak-lensing shape bias

Weak gravitational lensing measures a ~1% coherent distortion of galaxy shapes to
map dark matter. A CTI trail elongates every source in the read-out direction —
a *coherent, additive* distortion that mimics the lensing signal. This is why CTI
is a headline systematic for space-based lensing surveys, and why sub-percent CTI
correction is a mission-level requirement. Connects to the reference page on
[what CTI is](../../core/concepts/charge_transfer_inefficiency.md).

## Massey 2013 — origins of weak-lensing systematics and requirements

**Reference:** `Massey2013` — MNRAS 429, 661 — https://arxiv.org/abs/1210.7690
**Status:** drafted

The canonical requirements paper. It folds detector non-idealities — CTI among
them — together with PSF instability and shape-measurement error into the
additive and multiplicative systematics budget of a lensing survey, and derives
how well each must be known (or corrected) for the cosmological signal to survive.
It is the standard citation for *why* CTI correction has to reach the level
PyAutoCTI-style calibration aims for, and it frames CTI as one term in a larger
instrumental-systematics budget.

## Israel 2015 — residual bias after correction

**Reference:** `Israel2015` — MNRAS 453, 561 — https://arxiv.org/abs/1506.07831
**Status:** drafted

The bridge from correction quality to shape bias: it propagates imperfect
trap-model knowledge through iterative correction into the residual morphology
and photometry error — i.e. the leftover shape bias a lensing analysis must live
with. See [correction algorithms](./cti_correction_algorithms.md).

## Related

- [Euclid VIS calibration](./euclid_vis_calibration.md) · [HST ACS CTI](./hst_acs_cti.md)
- Entity: [Euclid VIS](../entities/euclid_vis.md)
