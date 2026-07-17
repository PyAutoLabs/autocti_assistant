---
name: ac_plot
description: Plot CTI datasets, fits and arrays using the autocti.plot function API — aplt.subplot_dataset_1d, aplt.subplot_imaging_ci, aplt.subplot_fit_dataset_1d, aplt.plot_yx, aplt.plot_array, aplt.plot_cti_1d and the *_list combined subplots. There is no MatPlot/Output/Visuals object; output paths are passed straight to the call.
---

# Plotting CTI data and fits

PyAutoCTI's plotting is a **matplotlib function API**: you call `aplt.<something>`
directly and pass the output path to the call. There is deliberately no
`Output` / `MatPlot2D` / `Visuals` object to construct and thread through (that
is the lensing stack's pattern, not this one). Follow the workspace scripts,
which use functions throughout.

Grounded in `autocti_workspace:scripts/plot/start_here.py` and the plotting
calls across the simulator/modeling/results scripts.

## The functions you'll actually use

**Whole datasets and fits** — the high-level subplots:

```python
import autocti.plot as aplt

aplt.subplot_dataset_1d(dataset=dataset)          # a 1D dataset
aplt.subplot_imaging_ci(dataset=imaging_ci)       # a 2D charge-injection image
aplt.subplot_fit_dataset_1d(fit=result.max_log_likelihood_fit)   # a 1D fit
aplt.subplot_fit_ci(fit=fit)                      # a 2D charge-injection fit
```

**Combined subplots over a list** — one figure showing every charge line, via
the `*_list` variants:

```python
aplt.subplot_dataset_1d_list(dataset_list=dataset_list)
aplt.subplot_fit_dataset_1d_list(fit_list=fit_list)
aplt.subplot_imaging_ci_list(dataset_list=imaging_ci_list)
```

**Single figures and raw arrays** — for one panel or an extracted region:

```python
aplt.figure_dataset_1d_data(dataset=dataset)      # one named figure
aplt.plot_yx(y=array_1d)                          # a 1D array (e.g. an extracted EPER)
aplt.plot_array(array=array_2d)                   # a 2D array
aplt.plot_cti_1d(cti=cti)                         # the CTI model itself
```

## Output paths — passed to the call, then announced

There is no separate output object: pass `output_path`, `output_filename` and
`output_format` straight to the plotting function.

```python
aplt.subplot_fit_dataset_1d(
    fit=fit,
    output_path="scripts/scratch/fit/",
    output_filename="fit_species_x2",
    output_format="png",
)
```

After running, **print the absolute path and quote it back to the user**, then
offer to open it (`xdg-open` on Linux, `open` on macOS, `explorer.exe` /
`wslview` from WSL). Don't just say "plot saved" — one offer per plot. The full
convention is in `AGENTS.md` "Plot path announcement".

## Note on Plotter objects

`aplt.PlotterDataset1D` and `aplt.PlotterImagingCI` do exist in the namespace,
but the workspace scripts do **not** use them — the function API above is the
taught, validated surface. Prefer the functions; reach for a Plotter only if a
user has an existing script built on one.

## Further reading

- `autocti_workspace:scripts/plot/start_here.py` — the plotting catalogue
  (`ccd/`, `diagnostics/`, `plotters/` subfolders for specific figures).
- Run `python -c "import autocti.plot as aplt; print(dir(aplt))"` for the full
  current function list before writing an unfamiliar plot call.
