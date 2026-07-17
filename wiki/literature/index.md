# CTI Literature Wiki — Index

Top-level navigation for the scientific literature behind Charge Transfer
Inefficiency. See [`AGENTS.md`](./AGENTS.md) for the schema and how the assistant
should use this wiki; the PyAutoCTI *reference* (what CTI is, the API) is in
[`../core/`](../core/index.md).

## Sources (bibliography by topic)

One page per topic; each cites the verified entries in
[`bibliography/autocti_literature.bib`](./bibliography/autocti_literature.bib).

- [Detector physics](./sources/cti_detector_physics.md) — how radiation damage
  creates traps and how traps distort charge.
- [Correction algorithms](./sources/cti_correction_algorithms.md) — pixel-based
  and forward-model (arctic) CTI correction, and how well it can be done.
- [HST ACS CTI](./sources/hst_acs_cti.md) — the two-decade history that defined
  the field's methods.
- [Euclid VIS calibration](./sources/euclid_vis_calibration.md) — the analytical
  CTI model and the in-flight calibration programme.
- [Trap pumping](./sources/trap_pumping.md) — locating and characterising
  individual traps.
- [CTI as a shape bias](./sources/cti_shape_bias.md) — why CTI is a headline
  weak-lensing systematic.

## Entities

- [arctic](./entities/arctic.md) — the open-source CTI forward-model code.
- [Euclid VIS](./entities/euclid_vis.md) — the visible imager and its CTI
  requirements.
- [HST ACS/WFC](./entities/hst_acs.md) — the Advanced Camera for Surveys.

## How CTI connects to the code

The reference concepts these papers underpin:
[what CTI is](../core/concepts/charge_transfer_inefficiency.md),
[trap physics](../core/concepts/trap_physics.md),
[the arctic algorithm](../core/concepts/arctic_algorithm.md),
[calibration strategy](../core/concepts/calibration_strategy.md).
