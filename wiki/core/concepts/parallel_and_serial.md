---
title: Parallel and serial CTI
sources: []
last_updated: 2026-07-17
---

# Parallel and serial CTI

A CCD reads out in two stages, and CTI happens in both. Understanding the two
directions is what separates the simple 1D picture from real 2D
charge-injection imaging.

- **Parallel transfer** — the whole image is shifted **row by row** toward the
  serial register at the edge of the CCD. Traps encountered here produce trails
  in the *parallel* (column) direction.
- **Serial transfer** — each row, once in the serial register, is shifted
  **pixel by pixel** along the register to the read-out amplifier. Traps here
  produce trails in the *serial* (row) direction.

Every pixel therefore experiences **both**: it is clocked through the parallel
traps to reach the register, then through the serial traps to reach the
amplifier. The two trap populations are physically distinct (different regions of
silicon, different radiation exposure) and are calibrated as **separate trap
models**.

## The 1D simplification

A 1D `Dataset1D` collapses this to a single clocking direction — it is the
cleanest way to learn the API and to calibrate one direction in isolation. There
is one `Clocker1D(express=)`, one `trap_list`, one `CCDPhase`. Most of the
concepts (traps, FPR/EPER, volume filling, the joint fit) are identical; only the
geometry is reduced.

## The 2D picture in PyAutoCTI

2D charge-injection imaging (`ImagingCI`) carries both directions explicitly:

```python
clocker = ac.Clocker2D(
    parallel_express=5, parallel_roe=ac.ROEChargeInjection(), parallel_fast_mode=True,
    # serial_express=..., serial_roe=... to add the serial direction
)

cti = ac.CTI2D(
    parallel_trap_list=parallel_trap_list, parallel_ccd=parallel_ccd,
    # serial_trap_list=..., serial_ccd=... for serial CTI
)
```

- The **`Clocker2D`** takes direction-prefixed kwargs
  (`parallel_*`, `serial_*`) — not the bare `express`/`roe` of `Clocker1D`.
- The **`CTI2D`** holds a parallel trap list + CCD and, optionally, a serial
  set. Parallel-only is the standard starting point; serial adds the second.
- The **`Layout2DCI`** names both `parallel_overscan` and
  `serial_prescan`/`serial_overscan`, and the extract/mask APIs gain
  direction-qualified regions (`parallel_fpr`, `serial_eper`, …).

## Which direction to calibrate

Real calibration campaigns often characterise the two directions with different
data and even separately, because a charge-injection line trails cleanly in the
parallel direction while serial CTI needs its own injection geometry. The
workspace's `imaging_ci` examples cover parallel-only, serial-only, and combined
(`features/serial_cti.py`).

## Related

- [The arctic algorithm](./arctic_algorithm.md) — the `Clocker` and `express`.
- [FPR and EPER](./fpr_and_eper.md) — regions in 2D.
- Skills: [`ac_simulate_imaging_ci`](../../../skills/ac_simulate_imaging_ci.md)
