---
title: Trap physics
sources: []
last_updated: 2026-07-17
---

# Trap physics

A **trap** is a defect in the CCD's silicon lattice with an energy level inside
the band gap, able to hold an electron. As a charge packet is clocked past a
trap, the trap can **capture** an electron from the packet; it then **releases**
it after a random delay drawn from an exponential distribution with a
characteristic **release timescale**. Capture removes charge from the packet
that is passing *now*; release deposits it into a packet passing *later* — which
is why the net effect is a trail in the read-out direction.

This capture-and-release is the Shockley–Read–Hall picture of trapping. Two
numbers characterise a trap species:

- **density** — how many traps per pixel (per unit length of transfer). More
  traps → deeper trails. Radiation damage raises the density over a mission.
- **release timescale** — how long, on average, a captured electron is held. A
  short timescale releases charge into the very next pixel (a sharp, close
  trail); a long timescale spreads it over many pixels (a long, faint trail).

Real detectors have **several trap species** with different timescales, so a
calibration model is usually a list of traps, not one.

## Volume-filling: why capture depends on how much charge is present

A trap can only capture from charge packets that physically reach it. A large
charge packet fills more of the pixel volume and exposes more traps; a small
packet reaches fewer. So the *fraction* of charge captured is **not** constant —
it depends on the packet's size relative to the well. This non-linearity is the
single most important subtlety in CTI, and it is why calibration data spans
**several charge normalisations**: each level probes a different depth of the
well.

PyAutoCTI models this with the **`CCDPhase`**:

```python
ccd = ac.CCDPhase(well_fill_power=0.58, well_notch_depth=0.0, full_well_depth=200000.0)
```

- `full_well_depth` — the pixel's capacity in electrons.
- `well_fill_power` — the exponent of the volume-filling relation; it sets how
  steeply the exposed-trap fraction grows with packet size.
- `well_notch_depth` — a floor below which no traps are exposed.

## In PyAutoCTI

Traps and the CCD are re-exported from the C++ **arctic** code via `arcticpy`:

```python
trap_0 = ac.TrapInstantCapture(density=0.13, release_timescale=1.25)
trap_1 = ac.TrapInstantCapture(density=0.25, release_timescale=4.4)
```

`TrapInstantCapture` is the standard "instant capture, delayed release" species;
continuum and other variants exist for more complex release behaviour. Assembled
with a `CCDPhase` into a `CTI1D`/`CTI2D`, they are what the
[arctic algorithm](./arctic_algorithm.md) clocks.

## Related

- [Charge Transfer Inefficiency](./charge_transfer_inefficiency.md)
- [The arctic algorithm](./arctic_algorithm.md)
- [Calibration strategy](./calibration_strategy.md) — how these numbers are measured.
- Literature: [detector physics](../../literature/sources/cti_detector_physics.md)
