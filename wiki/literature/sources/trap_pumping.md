---
title: Sources — Trap pumping
type: sources
topics: [cti, trap-pumping, calibration]
status: drafted
---

# Sources: Trap pumping

Trap pumping (pocket pumping) is the most direct probe of the trap *population*:
by clocking charge back and forth so a single trap captures and releases
repeatedly, it produces an identifiable "dipole" signal that localises and
characterises **individual traps** — their density, emission time constants, and
sub-pixel position. It underpins [calibration
strategy](../../core/concepts/calibration_strategy.md) as the technique that
measures the trap model most directly.

## Skottfelt 2017 — trap pumping for Euclid CCD273

**Reference:** `Skottfelt2017` — JINST 12, C12033 — https://ui.adsabs.harvard.edu/abs/2017JInst..12C2033S
**Status:** drafted

Trap-pumping schemes for the Euclid VIS CCD273 detector: characterising the
electrodes and the radiation-induced defects. It establishes trap pumping as part
of the in-orbit calibration routine for Euclid VIS — measuring the very trap
parameters (density, release timescale) that a forward-model calibration like
PyAutoCTI's fits from charge-injection data. The two techniques are
complementary: pumping localises individual traps; charge-injection fitting
measures the population's aggregate effect on science data.

## Related

- [Euclid VIS calibration](./euclid_vis_calibration.md)
- Reference: [trap physics](../../core/concepts/trap_physics.md),
  [calibration strategy](../../core/concepts/calibration_strategy.md)
