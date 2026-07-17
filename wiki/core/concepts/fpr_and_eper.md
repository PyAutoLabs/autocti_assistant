---
title: FPR and EPER
sources:
  - project: PyAutoCTI
    paths:
      - autocti/extract/
    pinned_commit: eca130ca30c69d24c3e1c134ce77471e9957f549
last_updated: 2026-07-17
---

# FPR and EPER — the anatomy of a CTI signal

A CTI calibration measurement has a deliberately simple structure: a block of
**injected charge**, and the **trail** that CTI drags out of it. Two names for
the two halves:

- **FPR — First Pixel Response.** The injected-charge region itself: the pixels
  where a known signal was placed (a charge-injection line, or a flat block).
  It is what goes *into* the trap field.
- **EPER — Extended Pixel Edge Response.** The trail of captured-then-released
  electrons that appears *after* the FPR in the read-out direction, spilling into
  the pixels beyond the injected region (and into the overscan). It is what comes
  *out* of the trap field, and its shape encodes the trap model — a short
  release timescale gives a sharp EPER, a long one a stretched EPER.

Reading the EPER is, in essence, reading the traps: its total captured charge
scales with trap density, and its decay length with release timescale.

## Geometry: prescan, overscan, injection

A dataset's `Layout` names where each of these lives. In 1D:

```python
prescan  = ac.Region1D((0, 10))       # read out before any injected charge
overscan = ac.Region1D((190, 200))    # extra clocks past the last real pixel
region_list = [(10, 20)]              # the FPR — where charge is injected
```

The **overscan** matters for CTI: clocking continues past the last illuminated
pixel, so the EPER trail extends into the overscan where there is no competing
signal — often the cleanest place to measure the faint end of the trail.

In 2D charge-injection imaging the same idea gains a direction: a `Layout2DCI`
names `parallel_overscan`, `serial_prescan`, `serial_overscan`, and the injection
`region_list`, because charge is clocked in two directions (see
[parallel and serial CTI](./parallel_and_serial.md)).

## Extracting FPR / EPER regions

`Layout.extract` pulls either region out as an array — for inspection, or for
stacking many injection lines to boost the faint trail's signal-to-noise:

```python
eper = layout.extract.eper.stacked_array_1d_from(
    array=data, settings=ac.SettingsExtract(pixels=(0, 10)))
fpr  = layout.extract.fpr.array_1d_list_from(
    array=data, settings=ac.SettingsExtract(pixels=(0, 10)))
```

The 2D layout exposes direction-qualified regions — `parallel_fpr`,
`parallel_eper`, and the serial equivalents — through the same `extract`
interface. The skill is
[`ac_mask_and_extract`](../../../skills/ac_mask_and_extract.md).

## Masking by region

Before a fit, masking the FPR leaves only the EPER trails (the usual calibration
target); masking the EPER leaves the injected charge. Both use
`Mask1D.masked_fpr_and_eper_from` / `Mask2D.masked_fpr_and_eper_from`.

## Related

- [Charge Transfer Inefficiency](./charge_transfer_inefficiency.md)
- [Calibration strategy](./calibration_strategy.md)
- [Parallel and serial CTI](./parallel_and_serial.md)
