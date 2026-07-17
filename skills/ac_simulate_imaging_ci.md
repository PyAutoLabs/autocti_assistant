---
name: ac_simulate_imaging_ci
description: Simulate a 2D charge-injection (CI) imaging dataset — injected charge regions clocked through a parallel (and/or serial) trap model with Clocker2D, the Euclid VIS / HST ACS calibration geometry. Writes a runnable script in scripts/. For the simpler 1D geometry see ac_simulate_dataset_1d.
---

# Simulating a charge-injection (CI) image

Charge-injection imaging is the 2D calibration geometry used by real
instruments (Euclid VIS, HST ACS): known charge is injected into rows of the
CCD, then clocked out through the trap field, and the trails it leaves calibrate
the CTI model. It is the 2D analogue of the 1D dataset — same trap physics, but
now with a **parallel** clocking direction (and optionally **serial**), 2D
regions, and `Clocker2D`.

Grounded in `autocti_workspace:scripts/imaging_ci/simulators/start_here.py`.

## Ask

- *"Parallel CTI only, or parallel + serial?"* — parallel-only is the standard
  starting point; serial adds a second clocking direction and a second trap set.
- *"Injection normalisations?"* — as in 1D, one image per charge level.
- *"CCD geometry — image shape, prescan/overscan regions?"* — the defaults below
  match the fiducial Euclid-like VIS layout.

## Geometry — 2D regions and layout

`Region2D` tuples are `(y0, y1, x0, x1)`. A `Layout2DCI` names the injection
regions and the parallel/serial overscans and prescans:

```python
import autocti as ac

shape_native = (2000, 100)
parallel_overscan = ac.Region2D((1980, 2000, 5, 95))
serial_prescan = ac.Region2D((0, 2000, 0, 5))
serial_overscan = ac.Region2D((0, 1980, 95, 100))
region_list = [(0, 200, 5, 95), (400, 600, 5, 95)]   # injected-charge rows
norm_list = [100, 5000, 25000, 200000]

layout_list = [
    ac.Layout2DCI(
        shape_2d=shape_native,
        region_list=region_list,
        parallel_overscan=parallel_overscan,
        serial_prescan=serial_prescan,
        serial_overscan=serial_overscan,
    )
    for norm in norm_list
]
```

## The 2D clocker and CTI model

This is where the 1D/2D difference bites. `Clocker2D` takes
**direction-prefixed** kwargs — `parallel_express`, `parallel_roe`,
`parallel_fast_mode` — not the bare `express`/`roe` of `Clocker1D`. The
`ROEChargeInjection` read-out electronics model is the charge-injection default:

```python
clocker = ac.Clocker2D(
    parallel_express=5,
    parallel_roe=ac.ROEChargeInjection(),
    parallel_fast_mode=True,   # only clocks unique columns for uniform charge — a big speedup
)

parallel_trap_0 = ac.TrapInstantCapture(density=0.13, release_timescale=1.25)
parallel_trap_1 = ac.TrapInstantCapture(density=0.25, release_timescale=4.4)
parallel_ccd = ac.CCDPhase(well_fill_power=0.58, well_notch_depth=0.0, full_well_depth=200000.0)

cti = ac.CTI2D(parallel_trap_list=[parallel_trap_0, parallel_trap_1], parallel_ccd=parallel_ccd)
```

Adding serial CTI means a `serial_trap_list` / `serial_ccd` on the `CTI2D` and
`serial_express` / `serial_roe` on the `Clocker2D` — see the `serial_cti.py`
example.

## Simulate and save the truth

The simulator call is identical in shape to 1D — `via_layout_from`:

```python
simulator_list = [
    ac.SimulatorImagingCI(read_noise=4.0, pixel_scales=0.1, norm=norm)
    for norm in norm_list
]
dataset_list = [
    simulator.via_layout_from(clocker=clocker, layout=layout, cti=cti)
    for simulator, layout in zip(simulator_list, layout_list)
]

aplt.subplot_imaging_ci(dataset=dataset_list[0])
ac.output_to_json(obj=cti, file_path=path.join(dataset_path, "cti.json"))
```

## Further reading

- `autocti_workspace:scripts/imaging_ci/simulators/` — `start_here.py` plus
  `examples/` (serial CTI, cosmic rays, non-uniform injection, Poisson traps).
- [`ac_fit_cti_model`](./ac_fit_cti_model.md) — the fit uses the same factor
  graph; the 2D masking uses `Mask2D` / `SettingsMask2D(parallel_fpr_pixels=...)`.
- Euclid VIS / HST ACS heritage — `wiki/core/` (once populated).
