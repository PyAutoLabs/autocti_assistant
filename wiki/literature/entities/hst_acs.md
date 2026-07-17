---
title: HST ACS/WFC
type: entity
topics: [mission, hst, acs, detector, cti]
status: drafted
---

# HST ACS/WFC

The **Advanced Camera for Surveys**, Wide Field Channel, on the Hubble Space
Telescope is where space-based CTI correction was first solved. Two decades of
accumulated radiation damage made its CCDs the proving ground for both the
empirical and the forward-model correction methods that every later mission
(including [Euclid VIS](./euclid_vis.md)) inherited.

- **The 2010 methods:** Massey 2010's physical forward model and Anderson &
  Bedin 2010's empirical warm-pixel correction — see
  [HST ACS CTI](../sources/hst_acs_cti.md) and
  [correction algorithms](../sources/cti_correction_algorithms.md).
- **Time evolution:** `MasseySM4_2010` and `Massey2014` track how CTI grew with
  dose after Servicing Mission 4 — the empirical case for repeated
  re-calibration.
- **Software heritage:** PyAutoCTI carries ACS support directly
  (`autocti/instruments/acs`); the ACS forward model is arctic's ancestor.

## Related

- Sources: [HST ACS CTI](../sources/hst_acs_cti.md),
  [correction algorithms](../sources/cti_correction_algorithms.md)
- Entity: [arctic](./arctic.md)
