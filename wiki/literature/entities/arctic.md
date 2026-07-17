---
title: arctic (CTI forward-model code)
type: entity
topics: [software, cti, arctic]
status: drafted
---

# arctic

**arctic** — "Algorithm for Charge Transfer Inefficiency Clocking" — is the
open-source C++ code that forward-models CTI: given a trap model and a CCD, it
clocks a clean image to produce the trailed image, and run in reverse it removes
CTI. It is the engine PyAutoCTI calls (through the `arcticpy` Python wrapper)
inside every `Clocker1D` / `Clocker2D`.

- **Repository:** <https://github.com/jkeger/arctic>
- **Python wrapper:** `arcticpy` (pinned 2.6) — a hard import of `autocti`, but
  deliberately not a pip dependency; see
  [`ac_setup_environment`](../../../skills/ac_setup_environment.md).
- **Reference concept:** [the arctic algorithm](../../core/concepts/arctic_algorithm.md).

## Lineage

arctic is the generalisation of the HST forward-model correction lineage
(`Massey2010` → `Massey2014`; see [HST ACS CTI](../sources/hst_acs_cti.md)) into a
mission-independent code, now used for Euclid VIS CTI work. The `express`
parameter is arctic's speed/accuracy control (see the concept page).

## Related

- Entity: [Euclid VIS](./euclid_vis.md) · [HST ACS/WFC](./hst_acs.md)
- Sources: [correction algorithms](../sources/cti_correction_algorithms.md)
