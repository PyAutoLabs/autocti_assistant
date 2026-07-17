---
title: Calibration strategy
sources: []
last_updated: 2026-07-17
---

# Calibration strategy

Calibrating CTI means recovering a **trap model** — how many species, their
densities and release timescales, and the CCD volume-filling parameters — from
data whose input charge is known. Because CTI worsens as radiation accumulates,
this is done repeatedly over a mission's life, not once.

## The measurement: known charge in, trail out

Every CTI calibration works the same way: put a *known* charge signal onto the
detector, clock it out, and measure the [EPER trail](./fpr_and_eper.md) it
leaves. The trail's depth constrains trap density; its decay length constrains
release timescale. The techniques differ in how the known charge is produced:

- **Charge injection** — the electronics inject charge directly into rows of the
  CCD, bypassing the optics, giving clean uniform lines at chosen levels. This is
  the in-flight workhorse for instruments like Euclid VIS, and the geometry of
  PyAutoCTI's `ImagingCI` datasets.
- **Flat fields** — a uniform illumination; the EPER appears past the
  illuminated region and in the overscan.
- **Trap pumping** (pocket pumping) — charge is clocked back and forth so a
  single trap captures and releases repeatedly, amplifying its signature until
  individual traps can be located and characterised. The most sensitive probe of
  the trap *population*.

## Why several charge levels

A single injection level cannot break the degeneracy between trap density and the
volume-filling non-linearity, because the *fraction* of charge captured depends
on how much of the pixel well is filled (see [trap physics](./trap_physics.md)).
So calibration data is always **a series of charge normalisations** — each probes
a different well depth — fitted **jointly**. In PyAutoCTI that joint fit is the
factor graph in [`ac_fit_cti_model`](../../../skills/ac_fit_cti_model.md).

## The PyAutoCTI workflow

1. **Simulate or load** calibration data at several normalisations
   ([`ac_simulate_dataset_1d`](../../../skills/ac_simulate_dataset_1d.md),
   [`ac_simulate_imaging_ci`](../../../skills/ac_simulate_imaging_ci.md)).
2. **Mask** to the EPER (hide the FPR) so the fit sees the trail
   ([`ac_mask_and_extract`](../../../skills/ac_mask_and_extract.md)).
3. **Compose** a CTI model with the trap parameters free and **fit** it across
   all charge lines with a non-linear search
   ([`ac_fit_cti_model`](../../../skills/ac_fit_cti_model.md)).
4. **Check** the recovered model — against the input truth for simulations, and
   by [correcting](../../../skills/ac_correct_cti.md) the data to confirm the trails
   vanish. A clean residual is the strongest evidence the calibration worked.

## Validating a calibration

The two independent checks worth running every time:

- **Recovery** — do the fitted densities/timescales match the input (simulated)
  or an independent measurement (real)?
- **Correction residual** — [correct](../../../skills/ac_correct_cti.md) the data
  with the fitted model; residual trailing means under-fit, a dip in the injected
  charge means over-correction.

## Related

- [FPR and EPER](./fpr_and_eper.md) · [Trap physics](./trap_physics.md)
- Literature: [Euclid VIS calibration](../../literature/sources/euclid_vis_calibration.md),
  [trap pumping](../../literature/sources/trap_pumping.md),
  [HST ACS CTI](../../literature/sources/hst_acs_cti.md)
