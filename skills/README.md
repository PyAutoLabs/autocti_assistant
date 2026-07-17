# skills/

Procedural how-to-do-X skills for the PyAuto\* lensing stack. Each skill is a single
Markdown file with YAML frontmatter; the body teaches an agent (and through them, the
user) how to write Python that accomplishes one lensing task.

Skills are also exposed at `.claude/skills/` (Claude Code) and `~/.codex/skills/` (when
configured) via symlinks; the canonical files live here.

## Conventions

- File names use the `ac_<task>` convention for lensing-API skills, e.g. `ac_run_search.md`.
- Project-workflow skills (repo-level operations, template manipulation) use a plain
  kebab-case name, e.g. `init-slam.md`, `start-new-project.md`.
- Domain-mode skills that pair an external pipeline repo to the assistant use that
  domain as prefix — `euclid_<task>.md` for the Euclid pipeline (euclid mode).
- Meta-skills (writing guide, bootstrap protocol) start with `_`.
- Every lensing-API skill is **python-first**: the deliverable is a runnable `.py` script
  + the understanding to evolve it. Project-workflow skills may instead drive `rsync`,
  `cp`, or other repo-level operations.
- Source citations use the project-name + repo-relative-path form,
  e.g. `PyAutoFit:autofit/non_linear/search/nest/nautilus/`, resolved via
  [`../sources.yaml`](../sources.yaml).
- Wiki references use workspace-relative paths,
  e.g. `wiki/core/concepts/non_linear_search.md`.

## Index

Every skill below is a **complete recipe** unless marked `(stub)` — the stubs are gathered
under "Pending — stubbed" at the end, with a queue of catalogued-but-unstubbed topics after
them.

### Meta

- [`_style.md`](./_style.md) — writing guide every skill is authored against. Read first
  before adding or editing any skill.
- [`_bootstrap_skill.md`](./_bootstrap_skill.md) — protocol for authoring a new skill on
  demand when a user requests a capability not yet covered.

### Setup & maintenance

- [`ac_setup_environment.md`](./ac_setup_environment.md) — detect absent or broken PyAuto\*
  environments, install via pip or editable clones when needed, configure caches, verify imports.
- [`ac_update_wiki.md`](./ac_update_wiki.md) — refresh `wiki/core/` pages whose pinned
  source commits have moved; surface new public APIs for review.
- [`ac_audit_skill_apis.md`](./ac_audit_skill_apis.md) — verify every PyAuto\* symbol
  cited in `skills/` and `wiki/core/api+stack/` resolves in the installed stack;
  report stale references with suggested replacements.
- [`ac_refresh_api_docs.md`](./ac_refresh_api_docs.md) — orchestrate a full maintenance
  sweep across skill recipes, wiki API pages, and pinned-source drift after a PyAuto\*
  upgrade or source refresh.
- [`ac_ingest_paper.md`](./ac_ingest_paper.md) — add a strong-lensing paper (local PDF
  or arxiv URL): project-local `wiki/project/bibliography.md` by default inside a science
  project; shared `wiki/literature/` in the assistant clone or on explicit promotion.

### Project workflow

- [`start-new-project.md`](./start-new-project.md) — the single bridge to a standalone
  **science project** and its full lifecycle (Create → Work → Collaborate → Publish):
  scaffold a lean repo that copies the reproducible science and refers back to the assistant
  for skills/wiki, run modelling with reproducibility manifests + the `wiki/project/` journal,
  build collaborator summaries, and harden for an open-science release (CITATION/license/Zenodo).
  Optional HPC folder.
- [`contribute-upstream.md`](./contribute-upstream.md) — prepare a scoped change,
  push it either to your collaborator branch on `PyAutoLabs/autocti_assistant`
  or to your fork, and open a draft PR into `PyAutoLabs/autocti_assistant`.
- [`init-slam.md`](./init-slam.md) — populate an empty `scripts/` folder with SLaM
  pipeline script(s) copied from `autocti_workspace` and tailored to the chosen data
  type.

### Euclid mode (pipeline-paired)

Skills pairing the collaboration's
[`euclid_strong_lens_modeling_pipeline`](https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline)
to the assistant; the paired literature context is the dedicated
[`wiki/euclid/`](../wiki/euclid/index.md) sub-wiki.

- [`euclid_setup_pipeline.md`](./euclid_setup_pipeline.md) — clone/install the pipeline,
  the `dataset/<sample>/<dataset>/` layout, and the black-box `start_here.py` run.
- [`euclid_prepare_data.md`](./euclid_prepare_data.md) — segmentation validation, binary
  mask tuning, extra-galaxy masks/centres via the GUI tools, hand-assembling a dataset
  folder.
- [`euclid_model_lens.md`](./euclid_model_lens.md) — choose and run the staged
  pipelines: initial MGE+SIE, Sersic photometry, lens-only subtraction, multi-waveband,
  full SLaM.
- [`euclid_workflow_products.md`](./euclid_workflow_products.md) — aggregate many fits
  into .csv catalogues, .fits stacks, and one-line .png summaries via `workflow/`.
- [`euclid_hpc_runs.md`](./euclid_hpc_runs.md) — `hpc/sync` configuration and the
  SLURM batch-array templates for sample-scale runs.

### Data preparation

- [`ac_prepare_imaging_data.md`](./ac_prepare_imaging_data.md) — load and preprocess
  FITS imaging, decide masking for real data, measure noise, prepare PSF.
- [`ac_simulate_dataset.md`](./ac_simulate_dataset.md) — synthesise a lens dataset
  (imaging or interferometer) from a ground-truth model.

### Model building

- [`ac_build_imaging_model.md`](./ac_build_imaging_model.md) — compose a `Tracer` from
  light + mass profiles and wrap it in an `AnalysisImaging`.
- [`ac_build_interferometer_model.md`](./ac_build_interferometer_model.md) — same, but
  for visibility-plane data.
- [`ac_custom_profile.md`](./ac_custom_profile.md) — write a new light or mass profile
  subclass and register it for use in models.

### Fitting

- [`ac_configure_search.md`](./ac_configure_search.md) — pick and tune a non-linear
  search (Nautilus, Dynesty, Emcee, Zeus, …) for your problem.
- [`ac_run_search.md`](./ac_run_search.md) — execute `search.fit(model=..., analysis=...)`
  and monitor convergence.
- [`ac_chain_searches.md`](./ac_chain_searches.md) — sequence searches so a later phase
  inherits priors from an earlier one.
- [`ac_run_slam_pipeline.md`](./ac_run_slam_pipeline.md) — run a Source-Light-Mass
  pipeline (the canonical automated lensing workflow).
- [`ac_debug_fit_failure.md`](./ac_debug_fit_failure.md) — diagnose a fit that didn't
  converge or produced unphysical results.

### Results & visualisation

- [`ac_load_results.md`](./ac_load_results.md) — load a completed fit's `Tracer`,
  `Samples`, dataset and FITS products from its output folder.
- [`ac_inspect_results_mcp.md`](./ac_inspect_results_mcp.md) — the read-only
  results-inspector MCP server: browse fits, summaries, result images and bulk
  subplot/FITS extraction from chat harnesses without code execution (Claude
  Desktop first).
- [`ac_plot_tracer.md`](./ac_plot_tracer.md) — plot ray tracing, critical curves,
  caustics, magnification maps.
- [`ac_plot_fit_residuals.md`](./ac_plot_fit_residuals.md) — plot model image,
  residuals, normalised residuals, chi-squared map.
- [`ac_inspect_source_reconstruction.md`](./ac_inspect_source_reconstruction.md) —
  inspect a pixelised inversion: regularisation, source-plane image, reconstruction
  diagnostics.
- [`ac_to_notebook.md`](./ac_to_notebook.md) — convert a generated narrative-docstring
  script to a Jupyter notebook (docstrings → markdown cells, code → code cells) via the
  stdlib-only `autoassistant/to_notebook.py`.

### Pending — stubbed (need full recipes)

Drafted as scaffolds during the 2026-05-22 coverage audit against
`autocti_workspace/scripts/`. Each has frontmatter + Orient/Ask/Branch/Combine
structure + `Further reading`; the `Branch` recipes are TODO markers. Fill in
one at a time, paired with their companion wiki/core stub.

**Data types and regimes**

- [`ac_point_source.md`](./ac_point_source.md) (stub) — quasar / multi-image
  position fits, flux ratios, point-source deblending.
- [`ac_time_delay_cosmography.md`](./ac_time_delay_cosmography.md) (stub) — H0
  from time-delay strong lenses.
- [`ac_group_lensing.md`](./ac_group_lensing.md) (stub) — extra galaxies,
  scaling-relation members.
- [`ac_cluster_csv_api.md`](./ac_cluster_csv_api.md) (stub) — cluster-scale
  CSV-driven model composition.
- [`ac_multi_dataset.md`](./ac_multi_dataset.md) (stub) — joint imaging +
  interferometer, multi-band, wavelength-dependent sources.
- [`ac_weak_lensing.md`](./ac_weak_lensing.md) (stub) — shear catalogue fits
  (`WeakDataset` / `AnalysisWeak`).
- [`ac_datacube_modeling.md`](./ac_datacube_modeling.md) (stub) — interferometer
  spectral cubes.

**Dark-matter substructure**

- [`ac_subhalo_detect.md`](./ac_subhalo_detect.md) (stub) — Bayesian-evidence
  grid search for perturbing subhaloes.
- [`ac_sensitivity_mapping.md`](./ac_sensitivity_mapping.md) (stub) — quantitative
  detectability calibration.

**Advanced techniques**

- [`ac_hierarchicac_inference.md`](./ac_hierarchicac_inference.md) (stub) —
  population-level / graphical models, expectation propagation.
- [`ac_aggregator_bulk_analysis.md`](./ac_aggregator_bulk_analysis.md) (stub) —
  bulk operations across many completed fits, optional result database.
- [`ac_adaptive_pixelization.md`](./ac_adaptive_pixelization.md) (stub) — adaptive
  mesh + adaptive regularisation source reconstructions.
- [`ac_mge_decomposition.md`](./ac_mge_decomposition.md) (stub) — Multi-Gaussian
  Expansion workflows for lens / source.
- [`ac_custom_analysis.md`](./ac_custom_analysis.md) (stub) — subclassing
  `Analysis` to add custom likelihood terms.

**Queue (catalogued, not yet stubbed):** `ac_multi_plane`, `ac_los_halos`,
`ac_over_sampling`, `ac_workflow_outputs`, `ac_data_prep_interactive`,
`ac_bayesian_model_comparison`.
