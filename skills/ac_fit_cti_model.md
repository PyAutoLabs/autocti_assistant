---
name: ac_fit_cti_model
description: Compose a CTI model (trap species + CCD) and fit it to one or more calibration datasets with a non-linear search, recovering the trap densities and release timescales. Covers the model cookbook, the AnalysisDataset1D wiring, and — crucially — the factor-graph structure that fits several charge lines jointly. Writes a runnable script in scripts/.
---

# Fitting a CTI model

Calibration is the inverse of simulation: given data with CTI trails, recover
the trap model that produced them. You compose a model with the trap
densities/timescales and CCD parameters *free*, hand it to a non-linear search
with an `Analysis`, and read the recovered values off the result.

A CTI calibration dataset is almost always **several charge lines at different
normalisations**, fitted **jointly** — one shared trap model, one likelihood per
line, summed. That joint fit is a **factor graph**, and it is the part most
worth getting right. The canonical example is
`autocti_workspace:scripts/dataset_1d/modeling/start_here.py`.

## Ask

- *"How many trap species in the model?"* — must match (or bracket) what you
  believe is in the data. Two is standard.
- *"Fitting one dataset or several charge lines jointly?"* — several is the
  norm, and means a factor graph (below). One is the simplifying case.
- *"Which parameters free vs fixed?"* — e.g. fix `well_notch_depth=0.0` and
  `full_well_depth`, leave densities and release timescales free.
- *"Real or simulated data?"* — simulated has a saved `cti.json` truth to check
  the recovery against; real does not.

## Compose the model

The model uses `af.Model` and `af.Collection` (the model cookbook). Each trap
and the CCD is a `Model`; they combine into a `CTI1D`:

```python
import autofit as af
import autocti as ac

trap_0 = af.Model(ac.TrapInstantCapture)
trap_1 = af.Model(ac.TrapInstantCapture)
trap_list = [trap_0, trap_1]

ccd = af.Model(ac.CCDPhase)
ccd.well_notch_depth = 0.0          # fix a parameter by assigning it
ccd.full_well_depth = 200000.0

model = af.Collection(cti=af.Model(ac.CTI1D, trap_list=trap_list, ccd=ccd))
```

Ordered trap species can otherwise swap identities during the search; assert an
ordering to break the degeneracy:

```python
trap_0.add_assertion(trap_0.release_timescale < trap_1.release_timescale)
```

## The clocker and the analysis

The `Clocker1D` used for the fit should match the simulation (`express=5`).
Each dataset gets its own `AnalysisDataset1D`, which pairs the data with the
clocker and defines the likelihood:

```python
clocker = ac.Clocker1D(express=5)

analysis_list = [
    ac.AnalysisDataset1D(dataset=dataset, clocker=clocker)
    for dataset in dataset_list
]
```

## The factor graph — fitting several charge lines jointly

This is the structural heart of a CTI fit and the API changed in the modern
stack: **analysis objects are no longer combined with the `+` operator** — the
addition that used to sum per-dataset log-likelihoods is gone. Instead each
analysis is wrapped in an `AnalysisFactor` that pairs it with the (shared)
model, and the factors combine into a `FactorGraphModel`:

```python
analysis_factor_list = [
    af.AnalysisFactor(prior_model=model, analysis=analysis)
    for analysis in analysis_list
]

factor_graph = af.FactorGraphModel(*analysis_factor_list)
```

The factor graph's log likelihood is the sum of the per-line likelihoods, and
its structure keeps each line's outputs and visualisation separate on disk.

## Run the search and read the result

Fit the factor graph's `global_prior_model` with its analysis. The result comes
back as a **list** — one entry per factor (per charge line):

```python
search = af.Nautilus(
    path_prefix=path.join("dataset_1d", dataset_name), name="species[x2]", n_live=100
)

result_list = search.fit(model=factor_graph.global_prior_model, analysis=factor_graph)

print(result_list[0].max_log_likelihood_instance.cti.trap_list[0].density)
aplt.subplot_fit_dataset_1d(fit=result_list[0].max_log_likelihood_fit)
```

For a single dataset, wire one `AnalysisDataset1D` into a one-element factor
graph the same way — the factor-graph path is uniform, so scripts don't
special-case the single-line case.

Once the search is running, say that `output/<path_prefix>/<name>/<unique_id>/` is filling
**on the fly** from the best CTI model so far — `model.results` and the `image/` fit
subplot are worth opening immediately, per charge line. For a newcomer, or in teacher
mode, tour the folder per `_style.md` "Output folder announcement" and point at
`__Output Folder__` / `__On The Fly Outputs__` in
[`autocti_workspace/scripts/dataset_1d/modeling/start_here.py`](https://github.com/PyAutoLabs/autocti_workspace/blob/main/scripts/dataset_1d/modeling/start_here.py).

## Check the recovery

If the data was simulated, load the input `cti.json` truth and compare the
recovered densities/timescales against it — this is the calibration working.
See [`ac_simulate_dataset_1d`](./ac_simulate_dataset_1d.md) for the saved truth
and [`ac_load_results`](./ac_load_results.md) for pulling values across many
fits via the aggregator.

## Test mode

Under `PYAUTO_TEST_MODE=2` the non-linear search is bypassed (it returns quickly
at the prior medians) so a script runs end-to-end for smoke testing.
`PYAUTOFIT_TEST_MODE` does **not** exist; the knob is `PYAUTO_TEST_MODE`.

## Further reading

- `autocti_workspace:scripts/dataset_1d/modeling/` — `start_here.py`, plus
  `customize/priors.py` and `features/species_x3.py`.
- `autocti_workspace:scripts/imaging_ci/modeling/` — the 2D charge-injection
  equivalent (parallel + serial CTI, `Clocker2D`).
- [`ac_mask_and_extract`](./ac_mask_and_extract.md) — masking the FPR/EPER
  before the fit.
