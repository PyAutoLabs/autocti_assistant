# wiki/

Three independently maintained sub-wikis. Each one answers a different question.

| Sub-wiki | Question | Provenance | Edited by |
|---|---|---|---|
| [`core/`](./core/) | *What is X / which X / why X* about CTI and the PyAuto\* stack? | Curated from source repos listed in [`../sources.yaml`](../sources.yaml), against pinned commits | `ac_update_wiki` skill (maintainer) |
| [`literature/`](./literature/) | *What does the CTI literature say about X?* | Compiled syntheses of public papers; schema in [`literature/AGENTS.md`](./literature/AGENTS.md), bibliography verified against arXiv/ADS | The user, when extending from new papers |
| [`project/`](./project/) | *What is the state of this project, and who is working here?* | `state.md` (project facts) + `profile.md` (on-demand user profile) + dated journal entries | Agent + user |

## When to read which

- *"What's the difference between the FPR and the EPER?"* / *"what does `express`
  do?"* → `core/` (follow [`core/index.md`](./core/index.md)).
- *"How is CTI corrected on HST?"* / *"why is CTI a weak-lensing systematic?"* →
  `literature/` (follow [`literature/index.md`](./literature/index.md)).
- *"Is PyAutoCTI on PyPI yet?"* / *"what's the release state?"* →
  [`project/state.md`](./project/state.md).

## When to write which

- **`core/`** is treated as read-only outside of `ac_update_wiki` runs. Don't
  edit pages ad-hoc as part of unrelated work.
- **`literature/`** has its own schema (see
  [`literature/AGENTS.md`](./literature/AGENTS.md)) with `sources/`, `entities/`
  and `[[wiki-link]]` cross-references, and a verified bibliography. Extend it
  when a new paper is read, following that schema — never fabricate citation
  metadata.
- **`project/`** — append to the journal after a meaningful session
  ([`project/_template.md`](./project/_template.md)); `state.md` holds durable
  project facts; `profile.md` is created from `_profile_template.md` only when a
  user volunteers durable context.

## Sub-wiki layout

```
wiki/
├── README.md            # this file
├── core/                # PyAuto* / CTI reference (what / which / why)
│   ├── README.md  index.md
│   └── concepts/
├── literature/          # CTI scientific reference
│   ├── AGENTS.md        # schema + usage rules (canonical; CLAUDE.md imports it)
│   ├── README.md  index.md  log.md
│   ├── concepts/  entities/  sources/  bibliography/
└── project/             # project state + running journal
    ├── README.md  state.md  _profile_template.md  _template.md
```
