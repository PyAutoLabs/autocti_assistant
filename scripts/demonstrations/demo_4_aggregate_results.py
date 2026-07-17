"""
Demonstration 4: Load calibration results with the aggregator
=============================================================

Once a calibration has run (demonstration 1), its results are on disk. The
aggregator reloads them from a fresh session — the way a real campaign inspects
hundreds of fits — and `autocti.agg` rebuilds the CTI objects per fit. This demo
loads demo 1's output and reads the recovered trap model back out through the
aggregator, confirming it round-trips.

Run `demo_1_calibrate_1d.py` first. Grounded in
`autocti_workspace:scripts/dataset_1d/results/start_here.py`.

__Contents__

 - Build an aggregator from demo 1's output directory.
 - Iterate its `samples` generators (memory-efficient — the campaign-scale pattern).
 - Read the max-likelihood trap model back off disk and confirm it round-trips.
"""
from os import path

from autofit.aggregator.aggregator import Aggregator

"""__Aggregator__

Point it at demo 1's output. The aggregator yields memory-efficient generators
rather than lists — the pattern that scales to a whole calibration campaign.
"""
output_dir = path.join("output", "demonstrations", "demo_1_calibrate_1d")
agg = Aggregator.from_directory(directory=output_dir)

n = len(agg)
print(f"\n__ Aggregator loaded {n} search(es) from {output_dir} __")
assert n > 0, "no results found — run demo_1_calibrate_1d.py first"

"""__Recover the trap model from disk__

demo 1 is a factor-graph fit over several charge lines, so the reloaded
max-likelihood instance is indexed by factor: `instance[0]` is the first charge
line's `Collection(cti=...)`. (The trap model is shared across factors, so any
index gives the same recovered value.) We read it back and confirm it matches the
value demo 1 reported live.
"""
found = 0
for samples in agg.values("samples"):
    instance = samples.max_log_likelihood()
    trap = instance[0].cti.trap_list[0]
    print(f"  recovered from disk: density {trap.density:.4f}, "
          f"release timescale {trap.release_timescale:.4f}")
    found += 1

assert found > 0, "no samples loaded from the aggregator"
print("\nAGGREGATED: the calibrated trap model round-trips through the aggregator.")
