"""
Demonstration 1: Calibrate a 1D CTI dataset and recover the input traps
=======================================================================

This is the assistant's headline demonstration: simulate a 1D CTI calibration
dataset from a *known* trap model, fit that model back with a non-linear search,
and confirm the recovered trap density and release timescale match the input
truth. If calibration works, the fit returns the numbers we put in.

It is deliberately small (one trap species, a short image, few live points) so it
runs in a few minutes on a laptop — the point is the recovery, not survey-scale
precision. Grounded in `autocti_workspace:scripts/dataset_1d/modeling/start_here.py`.

__Contents__

 - Simulate: a 1D dataset with a known one-species trap model at several charge
   normalisations.
 - Mask: hide the FPR so the fit sees the EPER trails.
 - Model + fit: compose the trap + CCD with parameters free, fit across all
   charge lines with a factor graph.
 - Recover: print input vs recovered, and assert they agree.
"""
from os import path
import numpy as np

import autofit as af
import autocti as ac

"""__Input truth__

The trap model we will try to recover. One `TrapInstantCapture` species and a
`CCDPhase` volume-filling model. See `wiki/core/concepts/trap_physics.md`.
"""
input_density = 0.13
input_release_timescale = 1.25
input_well_fill_power = 0.58

clocker = ac.Clocker1D(express=5)
cti_input = ac.CTI1D(
    trap_list=[ac.TrapInstantCapture(density=input_density, release_timescale=input_release_timescale)],
    ccd=ac.CCDPhase(well_fill_power=input_well_fill_power, well_notch_depth=0.0, full_well_depth=200000.0),
)

"""__Simulate__

A short 1D image (200 px), FPR injected at pixels 10-20, at several charge
normalisations — each probes a different depth of the pixel well, which is what
breaks the density / volume-filling degeneracy.
"""
shape_native = (200,)
prescan = ac.Region1D((0, 10))
overscan = ac.Region1D((190, 200))
norm_list = [100.0, 1000.0, 10000.0, 100000.0]

layout_list = [
    ac.Layout1D(shape_1d=shape_native, region_list=[(10, 20)], prescan=prescan, overscan=overscan)
    for _ in norm_list
]
dataset_list = [
    ac.SimulatorDataset1D(read_noise=0.01, pixel_scales=0.1, norm=norm).via_layout_from(
        clocker=clocker, layout=layout, cti=cti_input
    )
    for norm, layout in zip(norm_list, layout_list)
]

"""__Mask__

Mask the FPR so the fit is driven by the EPER trails (where the trap signature
lives). See `wiki/core/concepts/fpr_and_eper.md`.
"""
masked_list = []
for dataset in dataset_list:
    mask = ac.Mask1D.all_false(shape_slim=dataset.shape_slim, pixel_scales=dataset.pixel_scales)
    mask = ac.Mask1D.masked_fpr_and_eper_from(
        mask=mask, layout=dataset.layout,
        settings=ac.SettingsMask1D(fpr_pixels=(0, 10)), pixel_scales=dataset.pixel_scales,
    )
    masked_list.append(dataset.apply_mask(mask=mask))

"""__Model__

The same trap + CCD, now with density, release timescale and well-fill power
*free*. See `wiki/core/concepts/calibration_strategy.md`.
"""
trap = af.Model(ac.TrapInstantCapture)
ccd = af.Model(ac.CCDPhase)
ccd.well_notch_depth = 0.0
ccd.full_well_depth = 200000.0
model = af.Collection(cti=af.Model(ac.CTI1D, trap_list=[trap], ccd=ccd))

"""__Fit__

One `AnalysisDataset1D` per charge line, wrapped into a factor graph so the shared
trap model is fit jointly across all of them. A small `Nautilus` search.
"""
analysis_factor_list = [
    af.AnalysisFactor(prior_model=model, analysis=ac.AnalysisDataset1D(dataset=dataset, clocker=clocker))
    for dataset in masked_list
]
factor_graph = af.FactorGraphModel(*analysis_factor_list)

search = af.Nautilus(
    path_prefix=path.join("demonstrations", "demo_1_calibrate_1d"),
    name="species[x1]", n_live=50,
)
result_list = search.fit(model=factor_graph.global_prior_model, analysis=factor_graph)

"""__Recover__

Read the recovered trap off the max-likelihood instance and compare to the input.
"""
instance = result_list[0].max_log_likelihood_instance
rec_density = instance.cti.trap_list[0].density
rec_release = instance.cti.trap_list[0].release_timescale

print("\n__ Input vs recovered __")
print(f"  trap density         : input {input_density:.4f}   recovered {rec_density:.4f}")
print(f"  release timescale    : input {input_release_timescale:.4f}   recovered {rec_release:.4f}")

# The recovery should land within a modest tolerance of the input truth.
assert np.isclose(rec_density, input_density, rtol=0.25), "density not recovered"
assert np.isclose(rec_release, input_release_timescale, rtol=0.25), "release timescale not recovered"
print("\nRECOVERED: input trap model recovered within tolerance.")
