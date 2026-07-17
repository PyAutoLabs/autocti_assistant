"""
Demonstration 2: Calibrate a charge-injection (CI) image and recover the traps
==============================================================================

The 2D analogue of demonstration 1, in the real-instrument geometry: charge is
injected into rows of a CCD and clocked out in the parallel direction through a
known trap model, and the fit recovers that model. It is deliberately small (a
100x50 image, one trap species, few live points) so it runs in a few minutes;
survey-scale CI images are far larger.

Grounded in `autocti_workspace:scripts/imaging_ci/{simulators,modeling}/start_here.py`.

__Contents__

 - Simulate a small charge-injection image with a known parallel trap model.
 - Mask the parallel FPR so the fit is driven by the trails.
 - Compose + fit the parallel CTI model with a factor graph.
 - Recover: input vs recovered trap density / release timescale.
"""
from os import path
import numpy as np

import autofit as af
import autocti as ac

"""__Input truth__ — one parallel trap species (see demo 1)."""
input_density = 0.13
input_release_timescale = 1.25

clocker = ac.Clocker2D(parallel_express=2, parallel_roe=ac.ROEChargeInjection(), parallel_fast_mode=True)
cti_input = ac.CTI2D(
    parallel_trap_list=[ac.TrapInstantCapture(density=input_density, release_timescale=input_release_timescale)],
    parallel_ccd=ac.CCDPhase(well_fill_power=0.58, well_notch_depth=0.0, full_well_depth=200000.0),
)

"""__Simulate__ a small CI image at several injection normalisations. `Region2D`
tuples are (y0, y1, x0, x1)."""
shape_native = (100, 50)
region_list = [(0, 30, 2, 48)]
# Several injection levels are needed to constrain the trap model (each probes a
# different well depth); three keeps the 2D fit tractable on a laptop while still
# breaking the density / release-timescale degeneracy. Survey calibration uses
# many more.
norm_list = [500.0, 5000.0, 50000.0]

layout_list = [
    ac.Layout2DCI(
        shape_2d=shape_native, region_list=region_list,
        parallel_overscan=ac.Region2D((80, 100, 2, 48)),
        serial_prescan=ac.Region2D((0, 100, 0, 2)),
        serial_overscan=ac.Region2D((0, 80, 48, 50)),
    )
    for _ in norm_list
]
dataset_list = [
    ac.SimulatorImagingCI(read_noise=1.0, pixel_scales=0.1, norm=norm).via_layout_from(
        clocker=clocker, layout=layout, cti=cti_input
    )
    for norm, layout in zip(norm_list, layout_list)
]

"""__Mask__ the parallel FPR so the fit sees the trails
(`wiki/core/concepts/fpr_and_eper.md`)."""
masked_list = []
for dataset in dataset_list:
    mask = ac.Mask2D.all_false(shape_native=dataset.shape_native, pixel_scales=dataset.pixel_scales)
    mask = ac.Mask2D.masked_fpr_and_eper_from(
        mask=mask, layout=dataset.layout,
        settings=ac.SettingsMask2D(parallel_fpr_pixels=(0, 30)), pixel_scales=dataset.pixel_scales,
    )
    masked_list.append(dataset.apply_mask(mask=mask))

"""__Model__ — the parallel trap + CCD, density and release timescale free."""
trap = af.Model(ac.TrapInstantCapture)
ccd = af.Model(ac.CCDPhase)
ccd.well_notch_depth = 0.0
ccd.full_well_depth = 200000.0
ccd.well_fill_power = 0.58
model = af.Collection(cti=af.Model(ac.CTI2D, parallel_trap_list=[trap], parallel_ccd=ccd))

"""__Fit__ — one AnalysisImagingCI per injection level, joined in a factor graph."""
analysis_factor_list = [
    af.AnalysisFactor(prior_model=model, analysis=ac.AnalysisImagingCI(dataset=dataset, clocker=clocker))
    for dataset in masked_list
]
factor_graph = af.FactorGraphModel(*analysis_factor_list)

search = af.Nautilus(
    path_prefix=path.join("demonstrations", "demo_2_calibrate_imaging_ci"),
    name="parallel[x1]", n_live=60,
)
result_list = search.fit(model=factor_graph.global_prior_model, analysis=factor_graph)

"""__Recover__ input vs recovered."""
trap_rec = result_list[0].max_log_likelihood_instance.cti.parallel_trap_list[0]
print("\n__ Input vs recovered (parallel CTI) __")
print(f"  trap density      : input {input_density:.4f}   recovered {trap_rec.density:.4f}")
print(f"  release timescale : input {input_release_timescale:.4f}   recovered {trap_rec.release_timescale:.4f}")

assert np.isclose(trap_rec.density, input_density, rtol=0.3), "density not recovered"
assert np.isclose(trap_rec.release_timescale, input_release_timescale, rtol=0.3), "release timescale not recovered"
print("\nRECOVERED: input parallel trap model recovered within tolerance.")
