---
title: Euclid VIS
type: entity
topics: [mission, euclid, detector, cti]
status: drafted
---

# Euclid VIS

The **VIS**ible imager on ESA's Euclid mission is a wide-field, high-resolution
camera built to measure the shapes of billions of galaxies for weak
gravitational lensing. Because the cosmological signal is a ~1% coherent shape
distortion, VIS has stringent instrumental-systematics requirements — and CTI,
which elongates sources in the read-out direction, is one of the headline terms
(see [CTI as a shape bias](../sources/cti_shape_bias.md)).

- **Detector:** CCD273 (Teledyne e2v), the array trap-pumping is characterised on
  (`Skottfelt2017`).
- **CTI model:** the analytical radiation-induced-CTI model of `Short2013`
  (developed for Gaia, applied to Euclid) and the arctic forward model.
- **Calibration:** in-orbit **charge injection** and **trap pumping**, repeated
  over the mission as radiation dose accumulates. This is the science context
  PyAutoCTI's `ImagingCI` datasets and joint-fit calibration are built for; see
  [Euclid VIS calibration](../sources/euclid_vis_calibration.md).

## Related

- Sources: [Euclid VIS calibration](../sources/euclid_vis_calibration.md),
  [trap pumping](../sources/trap_pumping.md)
- Entity: [arctic](./arctic.md)
- Reference: [calibration strategy](../../core/concepts/calibration_strategy.md)
