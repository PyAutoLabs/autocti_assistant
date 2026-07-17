# Bibliography

Canonical citation metadata for the CTI literature wiki.

- [`autocti_literature.bib`](./autocti_literature.bib) — one BibTeX entry per
  paper; the citation key is **local to this repository**.
- [`bibkey_aliases.yaml`](./bibkey_aliases.yaml) — maps alternate/external keys
  to the canonical key here.

## Rules

- **Never fabricate metadata.** Record only fields you have verified against a
  source (arXiv, ADS, DOI, or the journal page). Where a full author list or a
  DOI is not verified, use the lead author + `and others` and the verified arXiv
  URL rather than a reconstructed value — the entries here follow that rule and
  say so in the file header.
- **Never record a local PDF path** — pages use public references and canonical
  keys, never file paths.
- Prefer an **arXiv ID / DOI / journal reference** as the locator. Author + year
  + title is an acceptable citation when a stable identifier is not available.
- A canonical key is local: before patching a science project's LaTeX, resolve
  the paper against that project's own `.bib` and reuse its existing key.

Users extend the wiki (and this bibliography) through a paper-ingest workflow;
add the verified `.bib` entry first, then the claim-oriented `sources/` section
that cites it.
