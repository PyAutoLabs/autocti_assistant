---
name: _style
description: Writing guide for every workspace skill. Read first before adding or revising a skill. Defines tone (conversational, physics-first, encourages reading), structure (Orient → Ask → Branch → Combine), the four properties every skill must have, the python-first rule, and the source-citation form (project-name + repo-relative path).
---

# How to write a workspace skill

This file is a meta-skill: it does not help a user run a lensing task directly. It is
the writing guide every other skill in this folder is authored against. Read it before
adding a new skill and re-read it before revising one.

## What a skill is

A skill is a single Markdown file at `skills/<name>.md`. It guides an AI agent through
one lensing task — composing an imaging model, running a search, inspecting a fit,
simulating a dataset — and in doing so produces or evolves a **Python script** the user
can run. The deliverable is *understanding + a runnable script*, not a chat answer.

The agent reads the skill when activated (either by the user typing `/ac_<name>` or by
the agent matching the skill's frontmatter `description` to the user's request).

## The five properties every skill must have

1. **Scientific and statistical context first.** Before showing API calls, set both the
   physics and the inference. *Why* are we loading the result, fitting this model, or
   running this profile? *What is being inferred*, with what likelihood, what priors,
   what search? The API is in service of the science and the inference, not the other
   way around. Both framings come before code — neither is optional.

2. **Encourage reading the wiki.** Every skill should point at relevant `wiki/`
   pages for the *what* (what is a Sersic, what is Nautilus, what is a pixelisation).
   Skills are procedure; the wiki is content. If a piece of content doesn't exist yet,
   draft the wiki page in the same change as the skill.

3. **Conversational tone, invites questions.** Talk to the user the way a postdoc
   collaborator would. Ask what they want before doing it. After explaining a concept,
   invite a follow-up. Don't narrate procedures (`Step 1. Step 2.`) when prose works.

4. **Skills compose.** Each skill should leave breadcrumbs to other skills that build on
   it. Mention adjacent skills by name when chaining would unlock something a single
   skill can't.

5. **Records work to the project wiki.** When a skill produces or evolves a non-trivial
   script, the agent must offer (default-yes) to add a dated
   `wiki/project/YYYY-MM-DD-<slug>.md` entry covering (a) *domain motivation* — what
   physics question this is in service of, (b) *statistical motivation* — what's being
   inferred and how, (c) *implementation choice* — the script produced and the key
   decisions. Cross-link every named concept and profile/model into `wiki/core/` and
   `wiki/literature/` using `[[wiki-link]]` slugs (e.g. `[[Sersic1968]]`,
   `[[NavarroFrenkWhite1996]]`, `[[mass-sheet-degeneracy]]`). Default to **no** only
   for typo fixes, throwaway exploration, or repeated re-runs of an existing pipeline.

## Python-first

This is the rule that distinguishes the workspace from a tutorial workspace.

- Every skill's main deliverable is a Python script written *for this user's data*.
- The skill body contains the API recipe inline, in fenced ```python``` blocks.
- The skill should leave the user with a `.py` file in `scripts/` they can re-run and
  modify themselves.
- Do **not** just point the user at a pre-existing script in another repo. If you
  reference an example (e.g. inside `autocti_workspace`), say so as a citation but
  produce the user-specific script in the working directory regardless.

## Generated script style

Every Python script the agent saves — whether to `scripts/` or `scripts/scratch/` — follows the
PyAutoCTI **workspace** style, not ad-hoc banner comments. It is the same style used by
every script in `autocti_workspace/scripts/` (canonical example:
`autocti_workspace:scripts/dataset_1d/modeling/start_here.py`), and it exists for two reasons: it
keeps the science and inference narrative inline with the code, and it makes the script
mechanically convertible to a Jupyter notebook — each top-level `"""..."""` block becomes a
markdown cell and the code between blocks becomes a code cell.

Two rules.

The level of detail in a saved script is **mode-invariant**. Teacher and assistant modes —
at any autonomy level — may change the pacing and depth of the surrounding conversation, but they must not
change the completeness of the script artefact. Write docstrings as if the script may become
part of the open-source repository accompanying a paper: preserve the scientific motivation,
what is inferred and how, consequential assumptions and configuration choices, enough context
to reproduce or adapt the analysis, and resolvable source citations. Avoid tutorial padding and
repetition, but do not remove this information merely because the user is experienced or has
asked for concise interaction.

**1. Title block + `__Contents__` header.** The module opens with a single docstring: a
title underlined with `=`, two or three sentences of orientation, then a `__Contents__`
list with one `- **Name:** one-line summary.` bullet per section that follows.

```python
"""
Lens Model: HST Imaging
=======================

Fit a galaxy-scale strong lens observed with HST imaging: load the data, compose an
SIE + external-shear mass model with a Sersic source, and fit it with Nautilus.

__Contents__

- **Imports:** Import the required libraries.
- **Dataset:** Load imaging, apply the mask and over-sampling.
- **Model:** Compose the lens (light + mass) and source galaxies.
- **Search:** Configure the Nautilus non-linear search.
- **Fit:** Run the fit and inspect the result.
- **Plot:** Save the best-fit subplot.
"""
```

**2. Per-section narrative docstrings, not banner comments.** Each logical section is
introduced by a `"""__Section__"""` docstring whose name matches a `__Contents__` bullet.
The prose carries the physics and inference framing (property #1) and any source citations
(see below) — *not* `# ---` banner comments and *not* `# source:` lines.

Do this:

```python
"""
__Dataset__

We load three ingredients for lens modeling: the image (CCD counts), a per-pixel
noise-map, and the PSF. `pixel_scales` converts pixels to arcseconds — set it correctly
for your instrument (HST/ACS ~ 0.05"). Loading is handled by `al.Imaging.from_fits`
(`PyAutoArray:autoarray/dataset/imaging/dataset.py`).
"""
dataset = al.Imaging.from_fits(
    data_path=DATASET_PATH / "data.fits",
    noise_map_path=DATASET_PATH / "noise_map.fits",
    psf_path=DATASET_PATH / "psf.fits",
    pixel_scales=PIXEL_SCALES,
)
```

Not this:

```python
# ---------------------------------------------------------------------------
# 1. Load imaging
# ---------------------------------------------------------------------------
# source: PyAutoArray:autoarray/dataset/imaging/dataset.py  (Imaging.from_fits)
dataset = al.Imaging.from_fits(...)
```

Short clarifying `#` comments *inside* a code block are still fine (e.g. annotating a
single prior). What changes is that section structure and citations live in the docstring,
not in comment banners.

## Source citations

Code references inside a skill must use the **project name + path relative to that
project's repo root**, resolvable via [`../sources.yaml`](../sources.yaml).

Good:

> See `PyAutoFit:autofit/non_linear/search/nest/nautilus/` for the search's default
> settings, and `wiki/core/api/searches.md#nautilus` for when to pick it.

Bad:

> See `/Users/other/autocti/fit/autofit/non_linear/search/nest/nautilus.py`.

The reason: this workspace is meant to be cloned to other machines. Absolute local paths
break the moment anyone else opens it.

The same `<Project>:<path>` form is used in **generated scripts**, but there it belongs
inside the section docstring prose (see "Generated script style" above) — woven into the
sentence that explains what the call does, never as a standalone `# source:` comment
banner.

## Adaptive depth

Adaptive depth governs the conversation and teaching around a script; it does not reduce the
publication-quality docstring detail required by "Generated script style" above.

Users arrive with different backgrounds. The same skill needs to serve all of them:

- **New to CTI.** Start with the [CTI concept page](../wiki/core/concepts/charge_transfer_inefficiency.md)
  or the narrated overview in [`ac_workspace_navigation`](./ac_workspace_navigation.md).
- **New to PyAutoCTI.** Use [`ac_workspace_navigation`](./ac_workspace_navigation.md) to
  find the `start_here.py` for the relevant dataset geometry and task.
- **Returning user.** Lead with the workspace example closest to the user's task.

Pick depth from the user's question and `wiki/project/profile.md` when it exists.
If the user's current cues differ from the profile, trust the user's latest input
and update the profile.

### Newcomer mode

1. Link the relevant CTI overview or concept before showing code.
2. Explain one detector effect at a time. For example, explain how traps cause
   trailing charge before discussing how the trail constrains a trap species.
3. Connect the physics to the inference, then show the code.
4. Invite a follow-up after a concept and point to a runnable workspace example
   the user can try.

## The conversation arc — Orient → Ask → Branch → Combine

Structure every skill as a conversation, not a checklist.

**Orient.** When the skill activates, give a short opening: what this task is
scientifically, what the user is about to do, the most relevant wiki page, and one
concrete data example tailored to what they mentioned (HST, JWST, Euclid, ALMA, JVLA…).
Two short paragraphs at most.

**Ask.** Before writing code, ask what the user wants out of the task. *"Want to fit the
mass model first or the source first?"* The answer chooses the branch and lets the skill
calibrate depth. Skip this step only when the user has already told you.

**Branch.** Each sub-task lives in its own narrative branch. A branch has four parts:

- Physics framing (one or two sentences, scaled to the user's depth).
- The Python recipe — actual code, in a fenced block, that the agent should adapt and
  save to `scripts/`. When the recipe is a full saved script (not a one-off fragment),
  write it in the **Generated script style** above: title + `__Contents__` header and
  `"""__Section__"""` narrative sections rather than banner comments.
- The wiki page that teaches this in depth, plus the source-code citation
  (`<Project>:<path>`).
- An invitation to dig deeper.

**Combine.** End the skill (or the chosen branch) with a short note on what else the
user could do, especially with other skills. *"Once you have the fit running, feed the
output into `ac_load_results` and `ac_plot`."*

A slim agent-facing procedural checklist at the very bottom of the file is fine — but
the user-facing content above should read like a conversation arc, not a recipe.

## Voice rules

**Do**

- Speak in second person. The user is the protagonist.
- Invite questions explicitly (*"ask if you want me to explain how this works"*).
- Tie at least one concrete example to the user's data when their data type is known.
- Point at the wiki by relative path every time you teach a concept.
- For newcomers, surface the relevant CTI overview before the code block. See "Newcomer mode" in Adaptive depth above.
- When a script produces plot files, quote the absolute path and offer to open it
  with the platform's opener. See "Plot output and path announcement" below.

**Don't**

- Don't open with a numbered procedure.
- Don't dump a wall of links — one or two per concept, chosen for relevance.
- Don't present code as the deliverable on its own — the deliverable is understanding +
  a saved script.
- Don't adopt a "just run this for me" tone. The user is here to learn lensing with
  the agent's help; gently route requests for black-box automation back through the
  wiki and existing skills.

## Frontmatter

Every skill file starts with YAML frontmatter:

```markdown
---
name: <kebab-case-name>
description: <one paragraph the agent reads when deciding whether to activate this skill>
---
```

The `description` is what the agent uses to decide when the skill applies. Write it so
a future agent that has only read the description (not the body) can decide from it
alone. Mention the kind of task, the kind of input, and what the skill should NOT be
used for.

## When a skill needs new wiki content

If you cannot point at a wiki page that explains a concept your new skill uses, draft
the wiki page in the same change. The wiki page should follow the wiki frontmatter
format (see `wiki/README.md`) and cite source code by `<Project>:<path>`.

The reverse is also true: don't write a wiki page nobody references. The wiki exists to
back up the skills.

## Plot output and path announcement

Skills that produce visualisations save them through the function-style
`autocti.plot` API — every entry point takes `output_path` / `output_filename`
/ `output_format` kwargs directly (see
[`ac_plot`](./ac_plot.md)). Three rules:

1. **Pass `output_path` / `output_filename` / `output_format` directly to
   each plot function.** Every `autocti.plot` `plot_*` and `subplot_*` helper accepts
   these kwargs, e.g. `aplt.subplot_imaging_ci(dataset=…,
   output_path="scripts/scratch/<context>/", output_filename=…,
   output_format="png")`. Never rely on interactive display — the user is
   often running the script from a terminal where `plt.show()` flashes and
   vanishes. The `<context>` slug is usually the dataset name; for general
   exploration any short slug works.
2. **`print(...)` each plot's path** at the end of the Python recipe so the
   absolute location lands in stdout. Use
   `print(f"Saved to: {PLOT_DIR.resolve()}")` once per branch (sufficient
   because each `aplt.*` call writes deterministically inside `PLOT_DIR`); for
   single-figure calls it's fine to print the exact `.png` path instead.
3. **The agent quotes the path back** to the user after running the script
   and offers to open it — one offer per plot run, not nagging. Use the
   platform's opener: `open <path>` on macOS, `xdg-open <path>` on Linux,
   `explorer.exe` (or `wslview`) from WSL.

The full convention — committed Python lives in `scripts/`; throwaway plots and data
dumps go to the gitignored `scripts/scratch/` — is in `AGENTS.md`
"Conventions". Skills here are the application of that rule.

## Output folder announcement

A running fit is not a black box. `search.fit(...)` writes to
`output/<path_prefix>/<name>/<unique_id>/` **on the fly**, using the highest-likelihood
CTI model found so far, so the folder is worth opening the moment the search starts — not
when it terminates hours later. Users new to the stack rarely know this and sit watching
a silent terminal. Three rules:

1. **Announce the folder at launch, not at the end.** Quote the absolute path once the
   fit is running, and say `model.results` and the `image/` subplots refresh as the
   search goes — there is nothing to wait for.
2. **Point at the workspace's own layout prose; don't restate it.** `__Output Folder__`
   and `__On The Fly Outputs__` in
   [`autocti_workspace/scripts/dataset_1d/modeling/start_here.py`](https://github.com/PyAutoLabs/autocti_workspace/blob/main/scripts/dataset_1d/modeling/start_here.py)
   walk the folder and the on-the-fly writes, and explain the unique identifier that makes
   a re-run resume rather than restart (`scripts/imaging_ci/modeling/start_here.py` has
   the same sections for charge-injection imaging). Link it once per fit; never copy the
   layout into a skill, where it would rot.
3. **Name what to open first.** `model.results` for the human-readable fit summary and
   the on-the-fly `FitDataset1D` / `FitImagingCI` subplot under `image/` for how good the
   fit currently is — then [`ac_load_results`](./ac_load_results.md) for the programmatic
   read. Under a factor graph one fit per charge line is written, each in its own
   subfolder, so name the line whose output you are quoting.

Depth follows "Adaptive depth" above. For users new to CTI or PyAutoCTI, and whenever
[`modes/teacher.md`](../modes/teacher.md) is active, walk all three rules — reading the
output folder *is* part of the workflow being taught. For a returning user, rule 1 alone
(one line quoting the path) is enough.

## External resource citation

End each `ac_*` skill with a single `## Further reading` block above the agent
checklist, if present. Cite up to three references that directly support the
workflow. Choose from a CTI concept page, a canonical source reference, or a
validated workspace example. Use [`ac_workspace_navigation`](./ac_workspace_navigation.md)
to find the relevant example, then cite the specific script.

Surface the best match for the user's experience and task in conversation. For
project workflow and meta-skills, include this section when a canonical reference
would help the reader.

## Iteration

This guide is the workspace v1 writing guide. As patterns emerge, update this file in
the same change as whatever motivated the update. Note the change at the top of that
PR description.
