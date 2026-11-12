# CTI maintenance queue

- [ ] Create the first CTI benchmark using the [simulated calibration demonstrations](scripts/demonstrations/README.md).
  Replace the inherited prompt examples in the [benchmark protocol](benchmarks/README.md)
  with a CTI prompt and a rubric covering data inspection, trap recovery, and residuals.
- [ ] Add a documented real-detector calibration example. Choose an openly reusable
  charge-injection dataset and record provenance, detector geometry, readout direction,
  and FPR/EPER regions. Demonstrate the pre-fit inspection, masking, and recovery checks
  described in [the agent instructions](AGENTS.md#safety-invariants--default-non-negotiable)
  and the [fitting skill](skills/ac_fit_cti_model.md).
- [ ] Review the inherited [configuration](config/README.md) against the installed
  PyAutoCTI stack and the 1D and 2D demonstrations. Identify the search, output,
  visualization, and prior settings the workflows actually use before changing any
  defaults. Include the inherited profile priors and configuration documentation in
  that review.
