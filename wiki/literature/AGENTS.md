# PyAutoCTI AI Assistant — CTI Literature Wiki

This sub-wiki (`autocti_assistant/wiki/literature/`) gives the assistant the
broad scientific context of Charge Transfer Inefficiency: the detector physics,
the correction algorithms, the missions where CTI is a headline systematic, and
the software. It is a compiled, cross-linked knowledge layer the assistant reads
at query time — the *what the field knows*, paired with the *how* in
[`../../skills/`](../../skills/) and the PyAutoCTI *reference* in
[`../core/`](../core/index.md).

It ships as a **self-contained base literature wiki** paired with a canonical
BibTeX bibliography. It is not tied to a PDF library: pages use public references
and canonical keys, never local file paths.

## References and citation metadata

Two layers with separate roles:

- `sources/*.md` records compact, claim-oriented guidance about what a paper
  supports (one paper = one section).
- `bibliography/autocti_literature.bib` records canonical citation metadata and
  keys; `bibliography/bibkey_aliases.yaml` maps alternate keys.

Use an arXiv ID, DOI, journal reference, or author/year/title **when verified**.
Never record a local PDF path or fabricate metadata; where a field is unverified,
prefer the lead author + `and others` and the verified arXiv URL. Detailed rules
are in [`bibliography/README.md`](./bibliography/README.md).

## Layout

```
wiki/literature/
├── AGENTS.md      # this file — schema + usage rules (canonical)
├── CLAUDE.md      # one-line import stub of AGENTS.md
├── index.md       # top-level navigation
├── log.md         # append-only compilation log
├── entities/      # specific detectors, missions, software (one per page)
├── sources/       # per-topic claim support (one paper = one section)
└── bibliography/  # the .bib, the alias map, and the rules
```

Concept-level science that the *reference* needs (what CTI is, trap physics,
FPR/EPER) lives in [`../core/concepts/`](../core/index.md); this wiki is the
*literature* behind it. `[[wiki-link]]` cross-refs and workspace-relative
`../core/...` links tie the two together.

## Using it

- A *what does the field say about X?* question → read the matching `sources/`
  page (and the `entities/` page for a mission/detector), then cite the `.bib`
  key.
- Cite as `Author Year` in prose, keyed to `autocti_literature.bib`; never invent
  a citation that is not in the `.bib`.
