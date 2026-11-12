# AGENTS.md — Agent instructions for autocti_assistant

You are working inside **autocti_assistant**, the PyAutoCTI AI Assistant: an agent workspace
combining instructions, skills, wiki content, and science-project machinery for CCD
charge-transfer inefficiency (CTI) calibration and correction. **This file is the canonical,
agent-agnostic source of truth.** Claude Code, Codex and other agents read it directly;
never maintain a parallel copy.

**Interaction principle.** When a decision genuinely depends on something you don't know,
ask one focused question — never default to the longest possible explanation.

## Session start — do this first, every session

1. **Maintainer mode.** Check for `.maintainer`; if present, read `modes/maintainer.md`.
   (`touch`/`rm .maintainer`; gitignored.)
2. **Project memory.** Read, when present: `wiki/project/state.md` (where the work got to —
   the head pointer, rewritten each session), then the newest dated
   `wiki/project/YYYY-MM-DD-*.md` entry, then `wiki/project/profile.md` (who the user is —
   use it to calibrate depth). Older entries are read on demand. Do not trigger heavy
   onboarding or create these files before the user volunteers durable context.
   A **science project** created by [`start-new-project`](./skills/start-new-project.md)
   carries the same three files and its own `AGENTS.md` says the same thing.
   *(Skipped in maintainer mode.)*
3. **Environment + API drift-check** *(only in a session that will generate or run code)*:
   ```bash
   python autoassistant/audit_skill_apis.py --check-version
   ```
   Exit 0 = nothing the docs can depend on has gone missing. It may still print an
   `additions only (not gated)` diff — new upstream exports are reported, not failed, since
   a symbol appearing cannot break a doc. Exit 1 = a symbol was **removed** from the public
   surface: it names which, so run `--scope all` to see whether any is actually cited before
   concluding anything. Exit 2/3 = absent/broken stack: report the interpreter and route to
   [`ac_setup_environment`](./skills/ac_setup_environment.md). Full detail, and when
   regenerating the baseline is right rather than papering over, in
   [`ac_audit_skill_apis`](./skills/ac_audit_skill_apis.md). Skip by default in maintainer mode.

## Safety invariants — default non-negotiable

Apply in every session. The wiki and code gate rules define their maintainer exceptions
below. The real-data inspection and history rules apply without exception.

- **Real data → inspect before fitting.** Before composing or running any model fit on real
  detector data, plot the dataset and show the user the absolute path to `dataset.png`.
  Ask one focused question about artifacts or regions that should be excluded, such as
  cosmic rays, bad pixels or columns, or contaminated charge-injection regions.
  Use [`ac_plot`](./skills/ac_plot.md) for the inspection plot and
  [`ac_mask_and_extract`](./skills/ac_mask_and_extract.md) for FPR/EPER masking and
  extraction. Simulated data is exempt.
- **Code gate.** A PreToolUse hook validates PyAuto* symbols against the installed library
  and blocks ones written from memory. If blocked, don't guess — grep `skills/` or introspect
  `dir()`, then re-run. Claude Code and Codex both register this hook from their
  project config. In Codex, review and trust the current project-hook hash with `/hooks`;
  changed or untrusted hooks are skipped. **On any other harness (GitHub Copilot CLI,
  OpenCode, an IDE agent) self-enforce it**: run
  `python autoassistant/audit_skill_apis.py --code "<snippet>"` (or `--file <script.py>`) on
  generated PyAuto* code before executing it. Codex registers the PreToolUse safety gates,
  not the separate Claude remote-session Python bootstrap; use `source activate.sh` normally.
  (Manual run + bypass:
  [`skills/ac_audit_skill_apis.md`](./skills/ac_audit_skill_apis.md).)
- **Never write into `output/`** (PyAutoFit runtime) **or `sources/`** (cloned repos);
  agent-authored Python → `scripts/` or `scripts/scratch/`.
- **`wiki/core/` is read-only in ordinary sessions.** Change it only during a deliberate
  reference refresh requested by a maintainer. Ground refreshed guidance in installed
  source. Append project notes to `wiki/project/`.
- **Source-edit boundary.** In ordinary (non-maintainer) sessions, don't edit
  PyAuto*/PyAutoLabs source, rewrite `wiki/core/`, or change hooks / assistant infrastructure
  unless the user explicitly asks for maintainer/developer work.
- **Bulk-edit safety.** Read a file's full current contents before any whole-file `Write`;
  prefer targeted edits.
- **Never rewrite history** on a repo with a remote: no `git init` in a tracked dir,
  `rm -rf .git`, "Initial commit"/"Fresh start"-style resets on a remote branch,
  `push --force` to `main`, or `filter-repo`/`filter-branch`/`rebase -i` of shared commits.
  Clean-state: `git fetch origin && git reset --hard origin/main && git clean -fd`.
  (`PyAutoLabs/autocti_assistant` has an origin; applies to its `main`.)

---

## The three-layer model

Map every request onto one or more layers:

1. **Instructions** (this file, `README.md`) — meta.
2. **Skills** (`skills/*.md`, exposed through generated Claude and Codex adapters) —
   *procedural*. CTI skills use `ac_<task>.md` and cover simulation, calibration,
   correction, and result inspection. [`start-new-project`](./skills/start-new-project.md)
   handles project setup. Files starting with `_` are authoring guidance.
3. **Wiki** (`wiki/**/*.md`) — *content* on detector CTI, trap physics, and calibration.

> **Rule of thumb.** *How do I do X?* → a skill. *What / which / why X?* → the wiki. *Build
> something end-to-end?* → compose skills, citing wiki pages as you go.

The wiki has three sections. [`wiki/core/`](./wiki/core/index.md) is the read-only CTI
reference. [`wiki/literature/`](./wiki/literature/index.md) covers detector physics,
correction algorithms, and instrument calibration, including Euclid VIS. Its
[schema](./wiki/literature/AGENTS.md) defines `[[wiki-link]]` cross-references.
`wiki/project/` holds this clone's state, journal, and profile.

---

## First-interaction protocol

**Create `profile.md` only when the user volunteers durable context** (level, prior
exposure, HPC access): copy `wiki/project/_profile_template.md`, fill only known fields, and
set `last_touched`. The science goal itself is `state.md`'s, not the profile's. Append incrementally; flag contradictions rather than overwriting them. If
the profile is older than ~10 sessions, ask whether anything changed.

---

## Modes

Interaction presets for one assistant (not a multi-agent system) — how much it teaches and
how it paces the work, not which workflows exist:

- **Teacher** — *learn*: explain, step through, point to examples.
- **Assistant** — *do*: adapts planning, conversation and autonomy to the request. Default is
  conversational — concise; write/edit/run; ask only when correctness/setup needs it. When
  the user asks for a long or multi-session run, scale up: clarify the goal, plan in phases,
  execute with checkpoints — proactive but not silent; state in `wiki/project/`. The dial is
  in [`modes/assistant.md`](./modes/assistant.md) "The autonomy dial".

Select (first match): explicit instruction → `profile.md` "Interaction mode" → else **infer
from the opening request** (fall back to **assistant**); `.maintainer` outranks both. There
are exactly two mode names — a value that isn't one of them (e.g. `agent`, removed in July
2026) is **not** a mode: ignore it, say so in one line, and fall through to inference rather
than improvising. State an inferred mode in one line and invite correction; acknowledge an
explicit one only if it changes behavior. Read `modes/<mode>.md`; depth still follows
`skills/_style.md` "Adaptive depth".

---

## Working with skills

When a skill covers the task:

1. Read the skill file end-to-end.
2. Follow its Orient → Ask → Branch → Combine arc (defined in
   [`skills/_style.md`](./skills/_style.md)).
3. Produce Python in the workspace style (below). Read any wiki page the skill points at
   before writing code. Before writing a script from scratch, check the `autocti_workspace`
   catalogue (`llms-full.txt`) for an existing example to adapt.

To answer *"what can you do?"*, read `skills/README.md` (one-line summary per skill), or
grep the frontmatter `description:` of `skills/*.md` for a topical question.

When no skill fits, follow [`skills/_bootstrap_skill.md`](./skills/_bootstrap_skill.md):
confirm scope, read `_style.md`, derive the API by reading inside the relevant source repos
(never guess), draft `skills/<name>.md`, add a wiki page if needed, register it in
`skills/README.md`, and regenerate both discovery surfaces as described there.

---

## Source-of-truth resolution

PyAuto\* libraries are separate repos listed in [`sources.yaml`](./sources.yaml). Cite code as
`Project:repo/relative/path.py`, never by absolute path. Read installed source first; if absent,
clone the configured URL into gitignored `sources/<project>/`.

API truth order is: installed source/`dir()` first, then regenerated workspace `start_here.py`
and feature examples for construction idioms. Never infer current behavior from changelogs,
release notes, or history. [`ac_audit_skill_apis`](./skills/ac_audit_skill_apis.md) contains the
mechanical currency checks.

---

## Commit cadence during user work

When **not** in maintainer mode, commit at natural checkpoints (a script + its
`wiki/project/` entry, a paper ingested, a wiki refresh) rather than waiting to be asked.

- **Announce before committing** in one line; the user can interrupt.
- **Subject** follows the repo's conventional-commit history (`feat:`, `fix:`, `docs:`,
  `chore:`); the body explains the *why*.
- **One checkpoint = one commit.** **Stage explicitly by filename** — never `git add -A`.
- **Never push** (always an explicit user action). **Never skip hooks** (no `--no-verify`);
  fix the underlying issue and make a new commit.
- **Agent attribution.** Name the actual harness and model in the commit body
  when known (for example, `Agent: Codex; model: <actual model>`). Use a
  `Co-Authored-By` trailer only when the active harness supplies a valid identity;
  never invent a provider email, model name, or Claude attribution. If the model
  is unavailable, record the known harness and say the model is unavailable.
- If the user is on `main` (or any branch tracked as `origin/HEAD`), pause and confirm
  before committing rather than landing directly there.

---

## Conventions

- **Standard imports** for any Python you write:
  ```python
  import autofit as af
  import autocti as al
  import autocti.plot as aplt
  ```
- **Generated script style.** Every `.py` you save uses the PyAutoCTI **workspace** style,
  not banner comments: an opening docstring (title underlined with `=`, short orientation,
  `__Contents__`), then each section introduced by a `"""__Section__"""` docstring carrying
  the physics/inference framing and `<Project>:<path>` citations. Full spec + example in
  [`skills/_style.md`](./skills/_style.md) "Generated script style".
- **Working directories.** Committed scripts → `scripts/`; throwaway plots/data dumps →
  `scripts/scratch/` (gitignored); `search.fit(...)` output → `./output/`.
- **Plot path announcement.** The plot API is functional: pass
  `output_path="scripts/scratch/<context>/"`, `output_filename=...`, `output_format="png"`
  straight to the `aplt.*` plotting call (e.g. `aplt.subplot_imaging_ci`,
  `aplt.subplot_fit_ci`) — there is no separate `aplt.Output`/`MatPlot2D` object.
  Then `print(...)` the absolute path, and after running **quote that absolute path** and
  offer to open it (platform opener: `open` on macOS, `xdg-open` on Linux,
  `explorer.exe`/`wslview` from WSL) — don't just say "plot saved". One offer per plot.

---

## Reference & operations

Load operational references on demand, not every session:

- **Science projects.** `autocti_assistant` is the copilot; a science project is a separate
  repo created and managed through [`start-new-project`](./skills/start-new-project.md).
- **Dataset geometry and examples** → [`ac_workspace_navigation`](./skills/ac_workspace_navigation.md).
- **Installation and writable caches** → [`ac_setup_environment`](./skills/ac_setup_environment.md).
- **Fit setup and test mode** → [`ac_fit_cti_model`](./skills/ac_fit_cti_model.md).
- **Choosing a reference for the reader** → [`skills/_style.md`](./skills/_style.md) under "Adaptive depth".

<!-- repos_sync:history:begin -->
## Never rewrite history

Never rewrite pushed history on any repo with a remote — no `git init` over a
tracked repo, no force-push to `main`, no fresh-start "Initial commit", no
`filter-repo` / `filter-branch` / `rebase -i` on pushed branches. To get a
clean tree: `git fetch origin && git reset --hard origin/main && git clean -fd`.
<!-- repos_sync:history:end -->

<!-- repos_sync:deliverable:begin -->
## Sessions end at their deliverable

A session ends when it reports its deliverable — never arm anything that
outlives the turn to wait for CI, a review or a merge: no `send_later`, no
`subscribe_pr_activity`, no `CronCreate`, no `ScheduleWakeup`, no `/loop`, no
`RemoteTrigger` create/update/run. Judge once, report, stop; the human re-runs
`/prm` (or the batch review) when it is green. Measured: five batch members
armed hourly check-ins on 2026-08-31, and a mobile `/prm` re-armed a 60-minute
`send_later` hourly all night on 2026-09-03 with no task active, draining usage.
<!-- repos_sync:deliverable:end -->

<!-- repos_sync:filing:begin -->
## Where to file

Questions, help with code or an analysis, ideas, bug reports and results from a
user or collaborator — or an agent acting for one — go to
<https://github.com/orgs/PyAutoLabs/discussions> in the matching category
(Help & Questions, Ideas & Proposals, Bugs & Errors, Show and tell;
Announcements is maintainers-only), never to this repo's Issues. An agent never
runs `gh issue create` for such a report: it drafts the title, category and
body and hands them to the human (sessions cannot create Discussions). Only the
development flow — Mind prompt → `/start_dev` → `/create_issue` → one issue per
task → PR — opens issues here. Why: `PyAutoMind/policy/community_surface.md`.
<!-- repos_sync:filing:end -->

<!-- repos_sync:standards:begin -->
## Shared standards

Before changing a shared interface, consult the applicable
[organism standard](https://github.com/PyAutoLabs/PyAutoBrain/blob/main/docs/standards.md)
on demand, identify affected consumers, and validate their adoption. Change
generated guidance at its canonical source and regenerate.
<!-- repos_sync:standards:end -->
