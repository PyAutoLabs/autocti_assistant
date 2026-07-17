"""
Demonstration 3: Correct CTI and show the residual improvement
==============================================================

Correction is arctic run in reverse. Given a trap model, `clocker.remove_cti`
un-clocks a dataset, pushing the trailed electrons back toward where they were
captured. This demo simulates a dataset with a known trap model, corrects it with
that same model, and shows — as a single number — that the EPER trail shrinks
dramatically. It needs no fit, so it runs in seconds.

Grounded in `autocti_workspace:scripts/dataset_1d/correction/start_here.py`.

__Contents__

 - Simulate a 1D dataset with a known trap model.
 - Measure the EPER trail power before correction.
 - Correct with `clocker.remove_cti` and measure the trail power after.
 - Assert the trail is strongly suppressed.
"""
import numpy as np

import autocti as ac

"""__Simulate__ a 1D dataset with a known trap model (see demo 1)."""
clocker = ac.Clocker1D(express=5)
cti = ac.CTI1D(
    trap_list=[ac.TrapInstantCapture(density=0.13, release_timescale=1.25)],
    ccd=ac.CCDPhase(well_fill_power=0.58, well_notch_depth=0.0, full_well_depth=200000.0),
)
layout = ac.Layout1D(
    shape_1d=(200,), region_list=[(10, 20)],
    prescan=ac.Region1D((0, 10)), overscan=ac.Region1D((190, 200)),
)
dataset = ac.SimulatorDataset1D(read_noise=0.01, pixel_scales=0.1, norm=10000.0).via_layout_from(
    clocker=clocker, layout=layout, cti=cti
)

"""__Measure the trail__

The EPER lives in the pixels just after the FPR (which ends at pixel 20). Sum the
absolute signal there as a simple measure of "how much trailing is present".
"""
def eper_power(data):
    native = np.asarray(data.native)
    return float(np.sum(np.abs(native[20:40])))

before = eper_power(dataset.data)

"""__Correct__ with the same (known) trap model."""
data_corrected = clocker.remove_cti(data=dataset.data, cti=cti)
after = eper_power(data_corrected)

print("\n__ EPER trail power (pixels 20-40) __")
print(f"  before correction : {before:.2f}")
print(f"  after correction  : {after:.2f}")
print(f"  suppression       : {before / max(after, 1e-6):.1f}x")

# The residual after correction is dominated by read noise; the trail itself is
# largely removed. A >2x drop in trail power is a clear, honest demonstration.
assert after < 0.5 * before, "correction did not suppress the trail"
print("\nCORRECTED: the EPER trail is strongly suppressed by remove_cti.")
