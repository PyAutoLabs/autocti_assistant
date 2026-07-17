---
title: Charge Transfer Inefficiency (CTI)
sources: []
last_updated: 2026-07-17
---

# Charge Transfer Inefficiency (CTI)

A CCD reads out by shuffling packets of photo-electrons pixel-by-pixel toward the
read-out amplifier, one row (or column) at a time. **Charge Transfer
Inefficiency** is the failure of that shuffle to be perfect: at each transfer, a
small fraction of the electrons in a packet is left behind, then released again a
short time later. The result is that charge is *smeared* in the direction of
read-out — a bright source grows a trail of electrons pointing away from the
amplifier.

The physical cause is **traps**: defects in the silicon lattice (created mostly
by radiation damage in orbit) that momentarily capture an electron from a passing
charge packet and release it after a characteristic delay. See
[trap physics](./trap_physics.md).

## Why it matters

CTI is a *systematic* — it distorts the very quantity being measured — so it
matters most for precision science:

- **Weak gravitational lensing.** The cosmological signal is a ~1% coherent
  distortion of galaxy shapes. A CTI trail elongates every source in the
  read-out direction, mimicking exactly that signal. Correcting CTI to the
  required level is a headline systematic for surveys like Euclid. See
  [CTI as a shape bias](../../literature/sources/cti_shape_bias.md).
- **Photometry and astrometry** of faint sources, where the fraction of charge
  lost to trails is largest and can bias fluxes and centroids.

CTI worsens over a mission's lifetime as radiation accumulates more traps, so it
must be **re-calibrated repeatedly** in flight rather than measured once on the
ground.

## The two things you do about it

1. **Calibrate** — measure the trap model (how many traps, their densities and
   release timescales, and the CCD's volume-filling behaviour) from dedicated
   calibration data. This is what PyAutoCTI is primarily for. See
   [calibration strategy](./calibration_strategy.md).
2. **Correct** — given a trap model, run the clocking in reverse to push the
   trailed charge back where it came from. See
   [`ac_correct_cti`](../../../skills/ac_correct_cti.md).

## How PyAutoCTI represents it

A CTI model is a set of **trap species** plus a **CCD** volume-filling model,
clocked by **arctic**:

- traps — e.g. `ac.TrapInstantCapture(density=, release_timescale=)`;
- the CCD — `ac.CCDPhase(well_fill_power=, well_notch_depth=, full_well_depth=)`;
- assembled into `ac.CTI1D(trap_list=, ccd=)` (1D) or
  `ac.CTI2D(parallel_trap_list=, parallel_ccd=, ...)` (2D);
- clocked by `ac.Clocker1D` / `ac.Clocker2D`, which wrap the
  [arctic algorithm](./arctic_algorithm.md).

The measurable signature CTI leaves in the data — the injected charge and its
trail — is the [FPR and EPER](./fpr_and_eper.md).

## Related

- [Trap physics](./trap_physics.md)
- [FPR and EPER](./fpr_and_eper.md)
- [The arctic algorithm](./arctic_algorithm.md)
- Literature: [detector physics](../../literature/sources/cti_detector_physics.md),
  [correction algorithms](../../literature/sources/cti_correction_algorithms.md)
