---
name: ac_mask_and_extract
description: Mask a CTI dataset to isolate the FPR or EPER before fitting, and extract FPR/EPER regions as arrays for inspection or diagnostics. Covers Mask1D/Mask2D.masked_fpr_and_eper_from and the layout.extract.fpr / layout.extract.eper API. Writes a runnable script in scripts/.
---

# Masking and extracting FPR / EPER regions

A CTI dataset has structure a fit cares about: the injected charge (**FPR**,
First Pixel Response) and the trail arctic leaves behind it (**EPER**, Extended
Pixel Edge Response). Two related operations exploit that structure — *masking*
(hide the FPR so the fit sees only the trails, or vice versa) and *extracting*
(pull a region out as a plain array to plot or diagnose).

Grounded in `autocti_workspace:scripts/dataset_1d/modeling/start_here.py`
(masking) and `autocti_workspace:scripts/dataset_1d/extract.py` (extraction).

## Ask

- *"Fit the trails or the injected charge?"* — masking the FPR leaves the EPER
  trails (the usual calibration target); masking the EPER leaves the FPR.
- *"1D dataset or 2D charge-injection image?"* — `Mask1D` / `Layout1D` vs
  `Mask2D` / `Layout2DCI`; the extract region strings differ (below).

## Masking before a fit

Start from an all-false mask (nothing masked) and add the FPR/EPER masking. The
`fpr_pixels` setting says how many pixels of the FPR to mask:

```python
import autocti as ac

mask = ac.Mask1D.all_false(
    shape_slim=dataset_list[0].shape_slim,
    pixel_scales=dataset_list[0].pixel_scales,
)

mask = ac.Mask1D.masked_fpr_and_eper_from(
    mask=mask,
    layout=dataset_list[0].layout,
    settings=ac.SettingsMask1D(fpr_pixels=(0, 10)),
    pixel_scales=dataset_list[0].pixel_scales,
)

dataset_list = [dataset.apply_mask(mask=mask) for dataset in dataset_list]
```

Plotting the masked dataset now shows only the EPER trails — the FPR is hidden.
This masked dataset is what you hand to [`ac_fit_cti_model`](./ac_fit_cti_model.md).

For 2D charge-injection imaging the shape is the same but the objects are 2D and
the settings name the *direction* — `ac.Mask2D`,
`ac.SettingsMask2D(parallel_fpr_pixels=(0, 200))`, over a `Layout2DCI`.

## Extracting a region as an array

A `Layout` exposes `extract.fpr` and `extract.eper`, each with three shapes of
getter. `SettingsExtract(pixels=(0, 10))` selects the pixel window relative to
the region (negative starts reach into the pixels *before* it — useful for the
overscan side of an EPER):

```python
layout_1d = ac.Layout1D(shape_1d=(200,), region_list=[(10, 20)],
                        prescan=ac.Region1D((0, 10)), overscan=ac.Region1D((190, 200)))
data_1d = ac.Array1D.from_fits(file_path=..., pixel_scales=0.1)

# just the pixel ranges each region occupies:
eper_regions = layout_1d.extract.eper.region_list_from(
    settings=ac.SettingsExtract(pixels=(0, 10)))

# the data in each region, one array per charge region:
eper_arrays = layout_1d.extract.eper.array_1d_list_from(
    array=data_1d, settings=ac.SettingsExtract(pixels=(0, 10)))
aplt.plot_yx(y=eper_arrays[0])

# all regions stacked into one averaged array (boosts the trail S/N):
eper_stacked = layout_1d.extract.eper.stacked_array_1d_from(
    array=data_1d, settings=ac.SettingsExtract(pixels=(0, 10)))
aplt.plot_yx(y=eper_stacked)
```

`layout.extract.fpr.*` mirrors this exactly for the injected-charge region.

The 2D region vocabulary is richer — instead of `fpr`/`eper`, a `Layout2DCI`
exposes direction-qualified regions (`parallel_fpr`, `parallel_eper`, and the
serial equivalents) reachable through the same `extract` interface.

## Further reading

- `autocti_workspace:scripts/dataset_1d/extract.py` — every extract getter.
- `autocti_workspace:scripts/imaging_ci/extract.py` — the 2D region strings.
- [`ac_plot`](./ac_plot.md) — plotting extracted arrays with `aplt.plot_yx`.
