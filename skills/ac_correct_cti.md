---
name: ac_correct_cti
description: Remove CTI from a dataset given a trap model — the inverse-clocking operation clocker.remove_cti, used to correct science data or as a diagnostic of a calibrated CTI model's quality. Writes a runnable script in scripts/.
---

# Correcting CTI

Correction is arctic run in reverse: given a CTI model, `remove_cti` un-clocks a
dataset, pushing the trailed electrons back toward where they were captured. Two
uses:

1. **Correct science data** with a CTI model calibrated elsewhere.
2. **Diagnose a calibration** — correct the *calibration* data with the fitted
   model and check the trails vanish. Residual trailing means the model is
   imperfect; over-correction means it's too strong. It's a direct, visual
   quality check on a fit.

Grounded in `autocti_workspace:scripts/dataset_1d/correction/start_here.py`
(the 2D equivalent is `imaging_ci/correction/start_here.py`).

## Ask

- *"Where does the CTI model come from — a fit, or known input values?"* — a fit
  gives you `result.max_log_likelihood_instance.cti`; known values you build
  directly (below).
- *"Correcting to check a calibration, or to clean science data?"* — same call,
  different intent; the diagnostic use compares corrected-vs-original trails.

## Build the model and correct

The CTI model is built with concrete values (not `af.Model` — this is an
instance, not something being fitted). If it came from a fit, use
`result.max_log_likelihood_instance.cti` instead of constructing it:

```python
import autocti as ac

clocker = ac.Clocker1D(express=5)

trap_0 = ac.TrapInstantCapture(density=0.13, release_timescale=1.25)
trap_1 = ac.TrapInstantCapture(density=0.25, release_timescale=4.4)
ccd = ac.CCDPhase(well_fill_power=0.58, well_notch_depth=0.0, full_well_depth=200000.0)
cti = ac.CTI1D(trap_list=[trap_0, trap_1], ccd=ccd)
```

`remove_cti` takes the data and the model and returns the corrected data:

```python
data_corrected_list = [
    clocker.remove_cti(data=dataset.data, cti=cti) for dataset in dataset_list
]

for data_corrected, norm in zip(data_corrected_list, norm_list):
    aplt.plot_yx(y=data_corrected, output_path=..., output_filename="data_corrected",
                 output_format="png")
```

For 2D charge-injection data the call is identical with a `Clocker2D`, `CTI2D`
and an `ImagingCI` dataset.

## Read it as a diagnostic

The most useful thing to show a user is the *before and after*: plot the
original trailed data and the corrected data side by side (or the residual
between them). If EPER trails remain after correction, the trap model
under-fits; if the injected charge develops a dip, it over-corrects. This is
often more legible than staring at posterior contours.

## Further reading

- `autocti_workspace:scripts/dataset_1d/correction/start_here.py`
- `autocti_workspace:scripts/imaging_ci/correction/start_here.py`
- [`ac_fit_cti_model`](./ac_fit_cti_model.md) — where the calibrated model
  comes from.
