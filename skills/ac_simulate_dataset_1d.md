---
name: ac_simulate_dataset_1d
description: Simulate a 1D CTI calibration dataset — charge lines with a known trap model clocked through arctic, so a later fit can be checked against the input truth. Writes a runnable script in scripts/. The 1D dataset is the simplest CTI calibration geometry; for 2D charge-injection imaging see ac_simulate_imaging_ci.
---

# Simulating a 1D CTI dataset

A 1D CTI dataset is the simplest calibration geometry: a line of pixels with an
injected charge signal (the **FPR**, First Pixel Response) that arctic clocks
through a trap model, leaving a trail of captured-and-released electrons behind
it (the **EPER**, Extended Pixel Edge Response). Simulating one with a *known*
trap model is how you generate ground truth — the input densities and release
timescales a later fit must recover.

The canonical example is
`autocti_workspace:scripts/dataset_1d/simulators/start_here.py`. This skill
writes the equivalent for the user's chosen trap model and geometry.

## Ask

- *"How many trap species, and what densities / release timescales?"* — the
  input truth. Two species is the standard starting point.
- *"What charge normalisations?"* — a calibration dataset is several charge
  lines at different injection levels; the list length is how many 1D datasets
  are simulated.
- *"Image length and region layout?"* — where the prescan, overscan and FPR
  sit. The defaults below (200 px, 10-px prescan/overscan, FPR at 10–20) match
  the fiducial workspace dataset.

## The script

Standard imports and geometry. `Region1D` tuples are `(x0, x1)` pixel ranges.

```python
import autocti as ac
import autocti.plot as aplt

shape_native = (200,)
prescan = ac.Region1D((0, 10))
overscan = ac.Region1D((190, 200))
region_list = [(10, 20)]                 # the FPR — charge injected here
norm_list = [100, 5000, 25000, 200000]   # one 1D dataset per normalisation
```

The `Layout1D` ties the geometry together — it knows where the FPR, EPERs and
overscans are, and the simulator uses it to place the initial charge:

```python
layout_list = [
    ac.Layout1D(
        shape_1d=shape_native,
        region_list=region_list,
        prescan=prescan,
        overscan=overscan,
    )
    for norm in norm_list
]
```

The CTI model — this is the ground truth. `Clocker1D` wraps arctic;
`express` trades speed for accuracy (5 is a good balance). Traps are
`TrapInstantCapture(density, release_timescale)`; the `CCDPhase` sets the
volume-filling behaviour:

```python
clocker = ac.Clocker1D(express=5)

trap_0 = ac.TrapInstantCapture(density=0.13, release_timescale=1.25)
trap_1 = ac.TrapInstantCapture(density=0.25, release_timescale=4.4)
trap_list = [trap_0, trap_1]

ccd = ac.CCDPhase(well_fill_power=0.58, well_notch_depth=0.0, full_well_depth=200000.0)

cti = ac.CTI1D(trap_list=trap_list, ccd=ccd)
```

> **Clocker kwargs are geometry-specific.** 1D uses `Clocker1D(express=, roe=)`.
> The 2D charge-injection clocker is `Clocker2D(parallel_express=,
> parallel_roe=, ...)` — different keyword names. Don't carry 1D kwargs into a
> 2D script (see [`ac_simulate_imaging_ci`](./ac_simulate_imaging_ci.md)).

Simulate one dataset per normalisation and plot:

```python
simulator_list = [
    ac.SimulatorDataset1D(read_noise=0.01, pixel_scales=0.1, norm=norm)
    for norm in norm_list
]
dataset_list = [
    simulator.via_layout_from(clocker=clocker, layout=layout, cti=cti)
    for simulator, layout in zip(simulator_list, layout_list)
]

aplt.subplot_dataset_1d(dataset=dataset_list[0])
```

Save the input `Clocker1D` and `CTI1D` alongside the data as JSON, so the fit
can be checked against the truth later (`ac.from_json()` reloads them):

```python
ac.output_to_json(obj=cti, file_path=path.join(dataset_path, "cti.json"))
ac.output_to_json(obj=clocker, file_path=path.join(dataset_path, "clocker.json"))
```

## Verify the truth is recoverable

The point of a simulated dataset is that a fit recovers its input trap model.
After simulating, the natural next step is
[`ac_fit_cti_model`](./ac_fit_cti_model.md) — compose a model with the trap
densities/timescales free and confirm the search returns the values above.

## Further reading

- `autocti_workspace:scripts/dataset_1d/simulators/` — `start_here.py` plus
  `examples/` (multi-species, continuum, temporal variants).
- [`ac_plot`](./ac_plot.md) — the `aplt.*` function plotting API.
- `wiki/core/` — trap physics and the FPR/EPER anatomy (once populated).
