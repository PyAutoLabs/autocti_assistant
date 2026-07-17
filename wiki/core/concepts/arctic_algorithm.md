---
title: The arctic algorithm
sources:
  - project: PyAutoCTI
    paths:
      - autocti/clocker/
    pinned_commit: eca130ca30c69d24c3e1c134ce77471e9957f549
last_updated: 2026-07-17
---

# The arctic algorithm

**arctic** ("Algorithm for Charge Transfer Inefficiency Clocking") is the forward
model at the heart of PyAutoCTI: given a trap model and a CCD, it takes a clean
image and produces the image *with* CTI trails — simulating the read-out. Run in
reverse, the same algorithm *removes* CTI. It is written in C++ (for speed) and
called from Python through `arcticpy`; PyAutoCTI wraps it in a `Clocker` object.

## What it does, conceptually

arctic walks the charge through the CCD one transfer at a time, and at each pixel:

1. computes how much of the pixel volume the current charge packet fills (the
   [volume-filling](./trap_physics.md) `CCDPhase` relation), hence how many traps
   are exposed;
2. **captures** electrons into those traps;
3. **releases** previously-captured electrons according to each species' release
   timescale, into the packet now passing.

Summed over every trap species and every transfer, this reproduces the FPR and
its EPER trail. Correction is the same walk solved for the *input* given the
*output* — pushing trailed charge back toward its origin.

## The `Clocker` — and `express`

PyAutoCTI calls arctic through a clocker:

```python
clocker = ac.Clocker1D(express=5)
```

Clocking every one of thousands of transfers exactly is expensive. **`express`**
is arctic's key speed/accuracy knob: it groups transfers so that the algorithm
evaluates the trap state a limited number of times rather than at every single
transfer. `express=1` is the fastest/coarsest; higher values approach the exact
calculation. `express=5` is the workspace's standard balance.

## 1D vs 2D — different kwargs

The clocker's keywords differ by geometry, and this is a common mistake:

- **`Clocker1D(express=, roe=)`** — one clocking direction.
- **`Clocker2D(parallel_express=, parallel_roe=, parallel_fast_mode=, serial_express=, ...)`**
  — direction-prefixed kwargs, because a 2D CCD clocks in two directions.

The `roe` ("read-out electronics") object models the read-out; for
charge-injection data it is `ac.ROEChargeInjection()`. `parallel_fast_mode=True`
speeds a uniform-charge simulation by only clocking unique columns. See
[parallel and serial CTI](./parallel_and_serial.md).

## Where it's used

- **Simulation** — `simulator.via_layout_from(clocker=, layout=, cti=)` adds CTI
  ([`ac_simulate_dataset_1d`](../../../skills/ac_simulate_dataset_1d.md)).
- **Fitting** — each `ac.AnalysisDataset1D(dataset=, clocker=)` clocks a trial
  model inside the likelihood ([`ac_fit_cti_model`](../../../skills/ac_fit_cti_model.md)).
- **Correction** — `clocker.remove_cti(data=, cti=)`
  ([`ac_correct_cti`](../../../skills/ac_correct_cti.md)).

arctic is developed openly at <https://github.com/jkeger/arctic>; installing its
Python wrapper is the trickiest part of setup — see
[`ac_setup_environment`](../../../skills/ac_setup_environment.md).

## Related

- [Trap physics](./trap_physics.md) · [FPR and EPER](./fpr_and_eper.md)
- Literature: [correction algorithms](../../literature/sources/cti_correction_algorithms.md)
