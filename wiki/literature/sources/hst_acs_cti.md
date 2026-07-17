---
title: Sources — HST ACS CTI history
type: sources
topics: [cti, hst, acs]
status: drafted
---

# Sources: HST ACS CTI history

The Hubble Advanced Camera for Surveys is where space-based CTI correction was
worked out, and the methods there — pixel-based and forward-model — are the
direct ancestors of the arctic code PyAutoCTI uses. See the entity page
[HST ACS/WFC](../entities/hst_acs.md).

## The two 2010 papers — the methods diverge

**References:** `Massey2010` (MNRAS 401, 371), `AndersonBedin2010` (PASP 122, 1035)
**Status:** drafted

In 2010, two correction schemes for ACS/WFC appeared side by side: Massey 2010's
physical **forward model** (clock a trap model, invert it) and Anderson & Bedin
2010's **empirical** approach (measure trails from warm pixels). Both operate on
raw pixel data. They set the template every later space mission has followed. See
[correction algorithms](./cti_correction_algorithms.md) for the method detail.

## Massey 2010 (SM4) — CTI since Servicing Mission 4

**Reference:** `MasseySM4_2010` — MNRAS Letters 409, L109 — https://arxiv.org/abs/1009.4335
**Status:** stub

Tracks the growth of CTI on HST following Servicing Mission 4, quantifying how
radiation dose in orbit steadily raises trap density — the empirical basis for
why CTI must be **re-calibrated over time**, not measured once.

## Massey 2014 — improved model and algorithm

**Reference:** `Massey2014` — MNRAS 439, 887 — https://arxiv.org/abs/1401.1151
**Status:** drafted

Refines the HST trap model and correction algorithm, consolidating the ACS
lineage into the machinery later generalised for Euclid. See
[correction algorithms](./cti_correction_algorithms.md).

## Related

- Entity: [HST ACS/WFC](../entities/hst_acs.md)
- [Correction algorithms](./cti_correction_algorithms.md) · [CTI as a shape bias](./cti_shape_bias.md)
