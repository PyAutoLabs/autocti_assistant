---
name: ac_load_results
description: Load and inspect CTI fit results — from a single search's result object, or across many fits with the aggregator (Aggregator.from_directory, ac.agg.CTIAgg / Dataset1DAgg / FitDataset1DAgg and their max_log_likelihood / weighted generators). Writes a runnable script in scripts/.
---

# Loading CTI results

Two ways to get at a fit's output:

1. **The `result` object** returned by `search.fit(...)` — immediate, in-memory,
   the fastest path when you still have it. For a factor-graph fit it's a
   `result_list` (one per charge line).
2. **The aggregator** — reloads results from disk, so you can inspect a run from
   a fresh session or sweep over *many* fits at once. This is how calibration
   campaigns (hundreds of datasets) are analysed.

Grounded in `autocti_workspace:scripts/dataset_1d/results/start_here.py` and
`.../results/examples/` (plus the `advanced/database/` examples).

## From the `result` object

```python
result = result_list[0]                       # factor-graph fits return a list

instance = result.max_log_likelihood_instance
print(instance.cti.trap_list[0].density)
print(instance.cti.trap_list[0].release_timescale)

fit = result.max_log_likelihood_fit           # a Fit object for plotting
samples = result.samples                       # the full posterior
```

The `samples_summary` gives medians and confidence intervals *without*
recomputing over the full sample list — prefer it when the value you want is
there, and fall back to `samples` only when it isn't.

## With the aggregator

Build an aggregator from the search's output directory (or a database), then use
`values(name)` to get a memory-efficient **generator** of any stored object.
Generators are single-use — remake them at the point of use rather than storing
them:

```python
from autofit.aggregator.aggregator import Aggregator

agg = Aggregator.from_directory(directory=path.join("output", "results_folder"))

for samples in agg.values("samples"):
    print(samples.parameter_lists[0])
```

## CTI-aware aggregation

Raw `values("samples")` gives you PyAutoFit objects. For the *CTI* objects
themselves, `autocti.agg` wraps the aggregator and rebuilds `CTI`, `Dataset` and
`Fit` instances per result:

```python
import autocti as ac

cti_agg = ac.agg.CTIAgg(aggregator=agg)

# the max-likelihood CTI model of every fit:
for cti in cti_agg.max_log_likelihood_gen_from():
    print(cti.trap_list[0].density)

# posterior-weighted draws, for propagating uncertainty:
for cti_list in cti_agg.all_above_weight_gen_from(minimum_weight=1e-4):
    ...
for weights in cti_agg.weights_above_gen_from(minimum_weight=1e-4):
    ...
for cti_list in cti_agg.randomly_drawn_via_pdf_gen_from(total_samples=2):
    ...
```

The sibling aggregators follow the same shape: `ac.agg.Dataset1DAgg` and
`ac.agg.FitDataset1DAgg` for 1D, `ac.agg.ImagingCIAgg` and
`ac.agg.FitImagingCIAgg` for 2D charge-injection. Each stores its objects in the
consolidated per-fit format and yields generators, not lists — the memory
discipline matters once you're aggregating hundreds of calibration fits.

## Checking recovery against the truth

For simulated data, load the input `cti.json` (saved by
[`ac_simulate_dataset_1d`](./ac_simulate_dataset_1d.md)) and compare the
recovered trap densities/timescales against it — a table of input-vs-recovered
per species is the clearest evidence the calibration works.

## Further reading

- `autocti_workspace:scripts/dataset_1d/results/` — `start_here.py` +
  `examples/{cti,fits,samples}.py`.
- `autocti_workspace:scripts/dataset_1d/advanced/database/` — the full
  aggregator/database cookbook and every `*_gen_from` generator.
