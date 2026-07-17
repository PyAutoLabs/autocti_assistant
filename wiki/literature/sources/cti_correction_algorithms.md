---
title: Sources — CTI correction algorithms
type: sources
topics: [cti, correction, arctic]
status: drafted
---

# Sources: CTI correction algorithms

The paper backing for how CTI is *removed* once a trap model is known, and how
well that removal can be trusted. Two families: **empirical pixel-based**
correction (measure trails from warm pixels, invert them) and **physical
forward-model** correction (clock a trap model, run it in reverse — the arctic
approach PyAutoCTI uses). Cites into
[the arctic algorithm](../../core/concepts/arctic_algorithm.md) and
[calibration strategy](../../core/concepts/calibration_strategy.md).

## Massey 2010 — pixel-based forward-model correction (ACS)

**Reference:** `Massey2010` — MNRAS 401, 371 — https://arxiv.org/abs/0909.0507
**Status:** drafted

The foundational forward-model correction for HST ACS/WFC. It builds a
physically motivated model that returns individual electrons to the pixels they
were dragged from during read-out, operating on **raw** data rather than
secondary products. Reported to reduce CTI trails by a factor of ~30 across the
CCD and at all flux levels (~97% correction). This is the direct ancestor of the
arctic forward model: capture/release governed by trap densities, release
timescales, and a volume-filling law.

## Anderson & Bedin 2010 — empirical warm-pixel correction (ACS)

**Reference:** `AndersonBedin2010` — PASP 122, 1035 — https://arxiv.org/abs/1007.3987
**Status:** drafted

The empirical counterpart, contemporaneous with Massey 2010. It characterises CTE
losses directly from the profiles of **warm pixels** in dark exposures, then
builds a pixel-based correction from those measured trails rather than from a
physical trap model. The two 2010 papers together established the two poles —
empirical vs physical — that the field has refined since.

## Massey 2014 — an improved model and algorithm (HST)

**Reference:** `Massey2014` — MNRAS 439, 887 — https://arxiv.org/abs/1401.1151
**Status:** drafted

Extends the forward-model correction with an improved trap model and correction
algorithm for HST, tracking how CTI evolved with accumulated radiation dose. It
is a key step in the lineage from the 2010 ACS work toward the arctic code used
for Euclid.

## Israel 2015 — how well can it be corrected?

**Reference:** `Israel2015` — MNRAS 453, 561 — https://arxiv.org/abs/1506.07831
**Status:** drafted

A parameter-sensitivity study for **iterative** forward-model correction: given
imperfect knowledge of the trap model, how much residual bias remains in
photometry and morphology? It quantifies which trap-model parameters matter most,
and therefore what a calibration must pin down — directly relevant to *why*
PyAutoCTI fits several charge normalisations jointly to constrain the
volume-filling non-linearity. (Note the published erratum, MNRAS 467, 4218.)

## Related

- Entity: [arctic](../entities/arctic.md)
- [HST ACS CTI](./hst_acs_cti.md) · [Euclid VIS calibration](./euclid_vis_calibration.md)
