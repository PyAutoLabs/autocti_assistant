---
name: ac_audit_skill_apis
description: Run the mechanical currency checks that keep this assistant's skills and wiki honest against the installed PyAutoCTI stack — the symbol audit (--scope), the public-surface gate (--check-version), the idiom deny-list, provenance and citation paths. Covers what wiki-currency runs in CI, and how to tell a stale baseline from a genuinely stale doc before regenerating anything.
---

# Auditing the documented API against the installed stack

Everything in `skills/` and `wiki/core/` is a claim about a library that keeps
moving. `autoassistant/audit_skill_apis.py` is the machine that checks those
claims. It is what the `wiki-currency` workflow runs in CI, what the session-start
protocol in `AGENTS.md` runs locally, and what the PreToolUse code gate calls on
generated Python.

All commands run from the repo root with the stack importable
(`source activate.sh`). If the stack is missing, fix that first —
[`ac_setup_environment`](./ac_setup_environment.md).

## The five checks

`wiki-currency` runs exactly these, in this order, and fails the job if any exits
non-zero:

| command | what it proves | fails when |
|---|---|---|
| `--check-version` | the installed **public surface** still contains everything the baseline recorded | a symbol was **removed** from `autonerves`, `autoarray`, `autofit`, `autocti` or `autocti.plot` |
| `--scope all` | every symbol **cited** in `skills/`, `wiki/` and `scripts/` resolves in the installed stack | a cited symbol does not resolve |
| `--lint-idioms` | no page uses a construction from the deny-list | a retired idiom survives, even though its constituent symbols still exist |
| `--check-provenance` | each `wiki/core` page's `pinned_commit` is real and reachable, and its `content_sha256` matches its body | a pin is forged or rewritten out of history, or a page was edited after stamping |
| `--check-citations` | every `Project:path` citation resolves to a real file | a cited path moved or was deleted |

`--scope` also takes `skills`, `wiki` or `scripts` on their own when you want a
narrower run, and `--out <file>` writes the report instead of printing it.

Two more entrypoints exist that CI does not run: `--code "<snippet>"` and
`--file <script.py>` validate generated PyAuto\* code against the installed
stack (the code gate — see `AGENTS.md` "Safety invariants"), and
`--install-check` reports whether the stack imports at all.

## `--check-version`: what it gates on, and why not more

It compares the installed stack's public API surface against
`wiki/core/api_audit_baseline.json`, which records, per module, the sorted list
of public names, a hash of that list, and a count.

**It fails on removals only. Additions are reported and pass.**

That narrowing is deliberate (autocti_assistant#25). The check covers the
*entire* public surface of `autoarray` and `autofit`, and this assistant
documents almost none of it. Worse, the workflow installs those libraries from
their **`main` source clones**, not a release — so the clock is every upstream
merge that exports a new name, which is fast. The red that forced this change
was 12 additions and 2 removals, and **not one of the 14 symbols was cited
anywhere** in `wiki/`, `skills/` or `modes/`. A gate that goes red on a schedule
nobody controls, for reasons that never touch what it gates, gets ignored — and
this repo's PRs opened red for over a month before anyone looked.

A symbol *appearing* cannot break a doc. A symbol *disappearing* can. So that is
the line.

It does **not** narrow further to "removals of *cited* symbols". That question is
precisely what `--scope all` already answers, against the real citation set, and
two mechanisms answering one question is how they drift apart. `--check-version`
is the cheap whole-surface tripwire; `--scope all` is the one with a direct
causal link to whether a doc is wrong.

The per-module `__version__` equality is **not** gated either (it is printed for
context). Since PyAutoConf#119 / PyAutoBuild#121 a release no longer commits the
version stamp back to library `main`, so a source checkout reports a frozen stamp
against a wheel-derived baseline — a permanent mismatch the surface comparison
already proves spurious.

## Reading a `--check-version` report

The report names the symbols. A passing one:

```
[drift] public API surface moved — additions only (not gated) (baseline generated 2026-08-24):
  autofit  160 -> 171
    + added:   AbstractClipper, AbstractScaler, ApproxUpdater, ...
  Nothing was removed, so no cited symbol can have stopped resolving. Not gating.
  Run `--write-baseline` to re-pin when convenient — the baseline is stale, not wrong.
```

A failing one:

```
[drift] public API surface moved — REMOVALS (baseline generated 2026-08-24):
  autoarray  122 -> 121
    - removed: TransformerNUFFTPyNUFFT
  A removed symbol can break a doc that cites it. Run `--scope all` to find out
  whether any of the above is actually cited, fix or re-word what is, then
  `--write-baseline` to re-pin.
```

Before autocti_assistant#25 the baseline stored only a hash, so the entire report
was `public API surface changed: autoarray, autofit`. Working out *what* moved
meant creating worktrees at the baseline's own commits, installing the libraries
from them, and diffing the symbol sets by hand. If you see that older wording, the
baseline predates symbol recording — `--write-baseline` upgrades it, and the check
keeps its old all-or-nothing behaviour until you do (an undiagnosable change is
treated as gating rather than assumed additive).

## Regenerating the baseline — the decision, not the reflex

`--write-baseline` overwrites `wiki/core/api_audit_baseline.json` from whatever
is installed. It is the right response **only when the drift does not implicate a
documented claim**. Otherwise it converts a true finding into a green tick, which
is strictly worse than the red.

Work through it in this order:

1. **Read the diff.** The report names every added and removed symbol.
2. **Additions only?** Regenerating is bookkeeping. The gate already passed;
   re-pin whenever convenient.
3. **Anything removed?** Run `--scope all`. If it is clean, no cited symbol
   moved and the removal is genuinely irrelevant to this assistant — record
   *which* symbols and that they were uncited in the commit message, then
   regenerate.
4. **`--scope all` reports a missing symbol?** Stop. The docs are wrong, not the
   baseline. Fix the page (or the idiom deny-list, if the construction was
   retired rather than the symbol), re-run, and regenerate only once both are
   clean.
5. **Regenerate against a stack you trust** — the same source clones CI builds
   from. A baseline written against a half-installed stack bakes in placeholders
   that read as drift forever. `compute_baseline` refuses to write if any library
   fails to import, which catches the worst version of this.

Say in the commit message which symbols moved and why regenerating was right.
"Regenerate baseline" alone is indistinguishable from papering over a real break.

## Do not pin to a released stack

The recurring suggestion is to make `wiki-currency` install a fixed PyPI version
so it stops moving. **Do not.** autocti's PyPI release is the pre-resurrection
`2024.11.13.2`; pinning would grade today's documentation against an API that
predates the work it describes — vacuously green, which is worse than noisily
red. The workflow's install step carries the same note. Considered and rejected
2026-08-24 (`PyAutoMind/complete/2026/08/wiki-currency-baseline-drift.md`).

The `stack_version` input exists for the *release-time* `workflow_call` path,
where PyAutoHands passes the version actually being released. That is a different
question — "does the wiki match the thing we are about to ship?" — and there a
pin is exactly right.

## Diagnosing a red run in CI

The workflow redirects every check into `drift-report.md`, so the job log never
names the failure — read the job summary or the `wiki-drift-report` artifact. The
report header records what was actually installed, including each source tree's
short SHA, so a red is diagnosable after the fact without reproducing the run.

If the artifact host is unreachable, reproduce locally: build the stack from the
`sources/` clones the way the workflow does and run the five commands above.
