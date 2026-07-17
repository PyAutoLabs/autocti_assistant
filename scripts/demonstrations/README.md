# scripts/demonstrations/

Four runnable, end-to-end demonstrations that exercise the assistant's whole CTI
calibration workflow — and double as its validation. Each is small enough to run
on a laptop in minutes, and each **asserts** its result, so a clean run is proof
the pipeline works, not just that it executes.

Run them with the PyAutoCTI stack on the path (see
[`../../skills/ac_setup_environment.md`](../../skills/ac_setup_environment.md) —
arcticpy is required). Fit output lands in the gitignored `output/`.

| Demo | What it proves | Cost |
|------|----------------|------|
| [`demo_1_calibrate_1d.py`](./demo_1_calibrate_1d.py) | Simulate a 1D CTI dataset from a known trap model, fit it, and **recover the input density and release timescale**. The headline calibration demonstration. | one real fit (~min) |
| [`demo_2_calibrate_imaging_ci.py`](./demo_2_calibrate_imaging_ci.py) | The same recovery in the 2D **charge-injection** geometry (the real-instrument case; parallel CTI, `Clocker2D`). | one real 2D fit (slower) |
| [`demo_3_correct_1d.py`](./demo_3_correct_1d.py) | Correct CTI with `clocker.remove_cti` and show the EPER trail is strongly suppressed. No fit — runs in seconds. | seconds |
| [`demo_4_aggregate_results.py`](./demo_4_aggregate_results.py) | Reload demo 1's fit from disk through the **aggregator** and confirm the calibrated trap model round-trips. | seconds (needs demo 1 first) |

Order: run demo 1 first (demo 4 reads its output); demos 2 and 3 are independent.

They are deliberately small (short images, one trap species, few live points) so
they finish quickly — the point is the *recovery*, not survey-scale precision.
For the science behind each step, follow the skill each demo cites and the
[wiki](../../wiki/core/index.md).
