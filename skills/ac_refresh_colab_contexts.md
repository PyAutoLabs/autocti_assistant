---
name: ac_refresh_colab_contexts
description: Maintainer upkeep for the link between this assistant's skills and the Colab notebooks of autocti_workspace. Runs the deterministic coverage check (`python -m autoassistant.colab_contexts check` plus PyAutoHands' `autohands gemini_context report`), then AI-scans what it flags — notebooks reached only by `default`, mapping entries that match nothing, missing or renamed skills, entries near the size cap — against the workspace script headers and the skill descriptions, proposes minimal `colab/contexts.yaml` edits, re-checks, re-stamps the workspace notebooks (the release does not regenerate them), and opens the matching PRs. Use after a skill is added, renamed or substantially resized, after the workspace gains or moves folders, and before a release. Not for user CTI questions, and never for editing the skills or the workspace scripts themselves.
---

# Refreshing the Colab Gemini skill map

Every notebook in `autocti_workspace` carries a Colab Gemini instruction in its
metadata, built from this repository's [`colab/contexts.yaml`](../colab/contexts.yaml):
the preface, the core rules, then the text of the one or two skills whose `match` glob
first fits the notebook's path. Colab's Gemini cannot read this repository, so that
mapping is the only way the skills reach it.

**CTI differs from the other assistants here.** The PyAutoHands release does not
regenerate `autocti_workspace`'s notebooks, so it never re-stamps them either. The
instruction a notebook carries is whatever was last applied with
`autohands gemini_context apply`. A mapping change therefore reaches users only when
you re-stamp the workspace notebooks and that change merges (pass 3).

The mapping goes stale quietly. A renamed skill breaks the next stamp. A new workspace
folder falls through to `default` and its users get generic help. A skill that grows
pushes an entry over the size cap. Nothing in a skill edit or a workspace PR flags
these, so this skill is the routine refresh: a deterministic report says *where* the
mapping is thin, and you read the notebooks and skills to decide *what* it should say.

The file's own header explains the matching rules (first match wins, `*` also crosses
`/`, `never_map`, the cap); [`autoassistant/colab_contexts.py`](../autoassistant/colab_contexts.py)
is the assistant-side check.

## When to run it

- After a skill is **added, renamed or removed**, or its text grows or shrinks
  substantially (sizes count against the cap).
- After `autocti_workspace` **gains, renames or moves a folder** of scripts, or its
  notebooks are regenerated (a regenerated notebook loses its stamp).
- **Before a release**, so the workspace notebooks carry a current map.

## Ask

Confirm with the maintainer before starting: **report only**, or **edit, re-stamp and
open PRs** in this session.

## Orient — locate the checkouts

You need this repository (the current directory), a PyAutoHands checkout for the
report and the stamp, and an `autocti_workspace` checkout. Prefer an existing checkout;
clone into the gitignored `sources/` folder only when none is found:

```bash
source activate.sh

find_checkout() {   # $1 = repository name; prints the first checkout found
  for d in "sources/$1" "../$1" "../../organs/$1"; do
    [ -d "$d/.git" ] || [ -f "$d/.git" ] && { echo "$d"; return; }
  done
  git clone --quiet --depth 1 "https://github.com/PyAutoLabs/$1" "sources/$1" && echo "sources/$1"
}
HANDS=$(find_checkout PyAutoHands)
WS_MAIN=$(find_checkout autocti_workspace)

refresh_checkout() {   # fast-forward only a clean checkout on main; never touch anything else
  if [ -z "$(git -C "$1" status --porcelain)" ] && [ "$(git -C "$1" branch --show-current)" = main ]; then
    git -C "$1" pull --quiet --ff-only || echo "WARNING: could not fast-forward $1"
  else
    echo "WARNING: $1 has local changes or is not on main; using it as it is"
  fi
}
for d in "$HANDS" "$WS_MAIN"; do refresh_checkout "$d"; done
"$HANDS/bin/autohands" gemini_context --help >/dev/null 2>&1 \
  || echo "STOP: Hands checkout predates #324 — update it"
```

`../<name>` is a sibling clone; `../../organs/PyAutoHands` is where PyAutoHands sits in
the PyAutoLabs development layout. `refresh_checkout` brings every located checkout up
to `main` so you map what users will get — but only a clean checkout already on `main`;
one with local changes or on another branch is used as it is, with a warning (say so in
the PR). If the last line prints `STOP`, the PyAutoHands checkout is older than the
`gemini_context` command: update it before going on. Never edit, commit to, push or
switch branches in the checkouts located here — they are read-only. The pass 3
re-stamp happens in a separate checkout made for that change.

The report reads the workspace's committed `notebooks/` tree. A folder that exists
only under `scripts/` (its notebooks not generated yet) is invisible to it; pass 1's
hand check finds those.

## Branch — pass 1: the deterministic report

Run the assistant-side check, then the PyAutoHands coverage report:

```bash
python -m autoassistant.colab_contexts check

"$HANDS/bin/autohands" gemini_context report --workspace "$WS_MAIN" \
    --project autocti --assistant-root . --json "${TMPDIR:-/tmp}/colab_report_autocti.json"
```

`check` fails on a mapped skill that does not exist, a `never_map` skill that is mapped,
or an entry over the cap. The report prints a short summary and writes JSON with:

- `default_notebooks` / `default_only_folders` — notebooks no entry matches.
- `unused_entries` — entries for this workspace that match no notebook.
- `missing_skills`, `never_map_violations` — mapped skills that are gone or banned.
- `sizes` (`max`, `median`, `over_cap`, `largest`) and `entries` (per-entry notebook
  count and `max_chars`) — how close each entry sits to `cap`.

Without `--json` the JSON follows the summary on stdout. A report exits 1 on a missing
skill, a `never_map` violation or an over-cap notebook. Save the text summary; it goes
into the PR body.

Two gaps the report cannot see, so check them by hand:

```bash
python - "$WS_MAIN" autocti_workspace <<'EOF'
import sys
from pathlib import Path
from autoassistant.colab_contexts import load, match
ws, repo = Path(sys.argv[1]), sys.argv[2]
ctx = load()
# Scripts whose notebooks would reach only `default`.
for py in sorted((ws / "scripts").rglob("*.py")):
    if py.name == "__init__.py":
        continue
    rel = py.relative_to(ws / "scripts").with_suffix(".ipynb").as_posix()
    if match(ctx, f"{repo}/notebooks/{rel}")[0] == "default":
        print("default only (script):", rel)
# Skills neither mapped anywhere nor listed in never_map.
used = set(ctx["default"]["skills"]) | {s for e in ctx["contexts"] for s in e["skills"]}
for p in sorted(Path("skills").glob("*.md")):
    if p.stem != "README" and p.stem not in used | set(ctx.get("never_map") or []):
        print("unmapped skill:", p.stem)
EOF
```

Ignore helper modules that never become notebooks; a script folder whose notebooks do
not exist yet is a real gap.

## Branch — pass 2: the AI scan

Work only on what pass 1 flagged. For each item, read before you propose:

- **The notebook's purpose.** The docstring at the top of the matching
  `scripts/<path>.py` in the workspace (and the folder's `README.rst` or `README.md`
  if it has one) says what the notebook teaches.
- **The candidate skills.** The `description` line in each skill's frontmatter
  (`grep -m1 '^description:' skills/ac_*.md`) says what the skill covers and what it
  is not for.

Then propose the smallest edit that fixes each item:

- **Notebooks reached only by `default`.** Add one entry with the narrowest glob that
  covers the folder (`.../folder/*`) — per notebook only when one notebook needs
  different skills from its siblings. Give it one or two skills, the closest to the
  notebook's task first. Place it **above** every broader entry that would otherwise
  match, since the first match wins. If `default` really is the best fit, leave it and
  say so in the PR.
- **Entries that match nothing.** Find where the folder went (`git -C "$WS_MAIN" log
  --diff-filter=R --summary -- scripts/` or a search of the tree). Retarget the glob if
  it moved; delete the entry if the folder is gone. Keep an entry whose folder exists
  under `scripts/` but has no notebooks yet — they will exist once generated.
- **Missing skills.** A renamed skill → swap in the new name. A deleted skill → pick
  the replacement from the skill descriptions, or drop it if the other skill suffices.
- **New skills nobody maps.** Map a user-facing skill where its workspace folder is; add
  a maintainer or agent-infrastructure skill (one that needs this repository checked
  out) to `never_map`. A skill with no workspace notebook to serve (one paired with a
  separate pipeline, say) can stay unmapped — note it in the PR rather than forcing it
  onto a folder.
- **Entries over the cap** must be fixed: drop the second skill or swap in a shorter
  one. **Entries near it** (`max_chars` above about 90% of `cap`) only need a line in
  the PR; a single-skill entry near the cap means that skill wants trimming, which is a
  separate change. Never raise `cap` yourself: it is a human decision (default 20,000,
  ceiling 50,000) — propose it in the PR instead.

Constraints on every edit: most specific entries first; one or two skills per entry;
never map a `never_map` skill; every entry within `cap`; touch only the entries the
report flagged, and keep the file's section comments in place.

## Branch — pass 3: apply, re-check and re-stamp

Edit `colab/contexts.yaml`, then repeat pass 1 until it is clean:

```bash
python -m autoassistant.colab_contexts check
python -m pytest -q autoassistant/tests/test_colab_contexts.py
"$HANDS/bin/autohands" gemini_context report --workspace "$WS_MAIN" --project autocti \
    --assistant-root . --json "${TMPDIR:-/tmp}/colab_report_autocti.json"
```

The report should exit 0, with no `default only` lines you did not choose on purpose.

Then re-stamp the workspace notebooks, because no release will do it. That is a change
to `autocti_workspace`, so it runs in a checkout made for this change — never in
`$WS_MAIN`, which the skill only located (in the PyAutoLabs layout it is the canonical
checkout). In the PyAutoLabs development setup, use the `autocti_workspace` worktree
that `start_dev` / `start_workspace` creates for the task:

```bash
WS_EDIT=<the task's autocti_workspace worktree>
```

Elsewhere, make a throwaway clone on a dated branch:

```bash
WS_EDIT="sources/autocti_workspace_restamp_$(date +%Y%m%d)"
git clone --quiet --depth 1 https://github.com/PyAutoLabs/autocti_workspace "$WS_EDIT"
git -C "$WS_EDIT" switch -c "colab-contexts-refresh-$(date +%Y%m%d)"
```

Then stamp it and look at the diff:

```bash
"$HANDS/bin/autohands" gemini_context apply "$WS_EDIT/notebooks" \
    --project autocti --assistant-root .
git -C "$WS_EDIT" diff --stat
```

`apply` prints how many notebooks it stamped; `Stamped 0 notebooks` means a wrong path.
The diff must touch notebook metadata only — no cell source or output. If anything else
changed, stop and find out why before going on. The workspace README's Colab Gemini
note documents the same command for whoever regenerates the notebooks.

## Combine — open the PRs

Show the maintainer both diffs. With their go-ahead, commit each on a branch (never
`main`), push the branches and open two PRs through the normal maintainer workflow (in
the PyAutoLabs development setup, `start_dev` → `ship_workspace`):

1. **autocti_assistant** — the `colab/contexts.yaml` change. The PR body carries the
   before and after report summaries, pasted as printed; one line per edit (the entry,
   the skills, and why); and anything left for a human: a proposed cap change, a
   `default` kept on purpose, a skill that needs trimming.
2. **autocti_workspace** — the metadata-only re-stamp, linking the assistant PR. Merge
   it after the assistant PR, so the stamped text matches the mapping on `main`.

Merging stays with a human.

The same report is upkeep evidence elsewhere: PyAutoBroca reads the
`autohands gemini_context report` output to record how fresh the skill↔workspace link
is and to flag "refresh needed". It never runs this scan or edits the mapping, so keep
the report itself the record — paste its output rather than re-describing it.

## When NOT to invoke this skill

- For a user's CTI question, or while helping someone with a notebook.
- To edit a skill's content or a workspace script — those are their own changes; run
  this skill afterwards.
- Inside unrelated feature work. A mapping diff should be its own reviewable PR.

## Agent procedural checklist

1. Confirm report-only or edit, re-stamp and PR.
2. `source activate.sh`; locate (or clone into `sources/`) PyAutoHands and
   `autocti_workspace`; bring the workspace up to `main`.
3. Run `python -m autoassistant.colab_contexts check` and `autohands gemini_context
   report --project autocti`; save the summary.
4. Run the script-tree and unmapped-skill scan.
5. For each flagged item, read the script header and the skill descriptions, then
   propose the minimal `colab/contexts.yaml` edit (most specific first, one or two
   skills, `never_map` and `cap` respected).
6. Apply; re-run `check`, the colab tests and the report until clean.
7. In the task's workspace worktree (or a throwaway dated-branch clone) — never the
   located `$WS_MAIN` — re-stamp with `autohands gemini_context apply
   <that checkout>/notebooks --project autocti --assistant-root .`; confirm the diff is
   metadata only.
8. With the maintainer's go-ahead, commit both on branches, push them and open the two
   PRs (assistant first, workspace re-stamp linked). Never push to `main`.
