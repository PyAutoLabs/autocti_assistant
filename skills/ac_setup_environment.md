---
name: ac_setup_environment
description: Install and verify the PyAutoCTI stack, including arcticpy — the C++ arctic clocking code that `import autocti` requires but pip will not install for you. The #1 setup failure. Covers the libgsl-dev + numpy/cython + arcticpy recipe, the numpy-downgrade trap, a no-root header workaround, and the environment/version drift check.
---

# Setting up the PyAutoCTI environment

Before any simulate/fit/correct work runs, the interpreter needs a working CTI
stack: `autoconf`, `autoarray`, `autofit`, `autocti`, and — the part that trips
almost everyone — **arcticpy**, the C++ *arctic* clocking code that `Clocker1D`
and `Clocker2D` wrap. `import autocti` fails without it, yet `pip install
autocti` does **not** pull it. This skill is how you get past that cleanly.

If `python autoassistant/audit_skill_apis.py --check-version` already exits 0,
the stack is healthy — skip to the bottom. Run this skill when that check exits
2/3, when `import autocti` raises `ModuleNotFoundError: No module named
'arcticpy'`, or when a user is installing for the first time.

## Ask

- *"Do you want a fresh virtual environment, or install into an existing one?"* —
  a project-local `.venv` is the default (`activate.sh` looks for it); a shared
  or HPC checkout points `PYAUTO_HPC_BASE` at a `PyAuto/` venv instead.
- *"Do you have root / sudo on this machine?"* — it decides how the GSL headers
  arctic needs are obtained (system package vs. local extraction).
- *"Python version?"* — 3.12 or 3.13 is first-class; 3.11 works but warns.

## Why arcticpy is special

`arcticpy` (pinned to **2.6**) is a hard import of autocti but deliberately not
a pip dependency, for two reasons that both bite if you let pip resolve it
normally:

- Its PyPI sdist is **source-only C++** — it needs the GSL headers
  (`libgsl-dev`) and a C++ toolchain to build. There is no wheel.
- Its own requirements **downgrade numpy below 2.0**, quietly breaking a modern
  autoarray/autofit stack that expects numpy ≥ 2.

So arcticpy is installed *after* numpy is already in place, with dependency
resolution and build isolation both turned off.

## The recipe

The order matters. numpy and cython must exist before arctic builds, and
arctic must be installed `--no-deps` so it cannot drag numpy back down.

```bash
# 1. GSL headers + a C++ toolchain (system-wide; needs sudo).
sudo apt-get update && sudo apt-get install -y libgsl-dev

# 2. numpy + cython first, so arctic has what it needs to build against.
pip install numpy cython

# 3. arctic itself — no build isolation (uses the numpy just installed),
#    no deps (so it cannot pull an old numpy).
pip install arcticpy==2.6 --no-build-isolation --no-deps

# 4. the PyAutoCTI stack.
pip install autocti
```

Then confirm:

```bash
python -c "import arcticpy, autocti; print('arctic', arcticpy.__version__, '| autocti', autocti.__version__)"
```

The CI-hardened form of exactly this recipe lives in
`autocti_workspace_test:.github/scripts/smoke_install.sh` — cite it when a user
wants the canonical, tested sequence.

## No root? Extract the GSL headers locally

If `libgsl-dev` can't be installed system-wide, fetch and unpack it into your
home directory, then point the compiler at it for step 3:

```bash
apt-get download libgsl-dev            # downloads the .deb, no install
dpkg -x libgsl-dev*.deb "$HOME/gsl"    # extracts headers/libs under ~/gsl
export CPPFLAGS="-I$HOME/gsl/usr/include"
export LDFLAGS="-L$HOME/gsl/usr/lib/x86_64-linux-gnu"
pip install arcticpy==2.6 --no-build-isolation --no-deps
```

The full note is in `PyAutoCTI:AGENTS.md` under "arcticpy (read before
installing)".

## Developer install (editable source checkouts)

Running against the `main` source checkouts instead of a PyPI release (what
`activate.sh`'s developer block and the `wiki-currency` CI do): install the
same arctic prefix (steps 1–3), then the local repos in dependency order, and
pin autoconf last so a re-resolution can't replace it with a stale wheel:

```bash
pip install ./PyAutoNerves ./PyAutoFit ./PyAutoArray ./PyAutoCTI
pip install "./PyAutoArray[optional]"
pip install --force-reinstall --no-deps ./PyAutoNerves
```

Note the CTI stack is **autoconf/autoarray/autofit/autocti** — it does *not*
include autogalaxy (that is the lensing stack). Don't install or expect it.

## Verify

Once installed, the environment + API drift check is the single source of truth:

```bash
python autoassistant/audit_skill_apis.py --check-version
```

- **exit 0** — the documented API matches the installed stack; you're ready.
- **exit 1** — genuine drift (a version moved); recommend the pinned version or
  an audit (see [`ac_audit_skill_apis`](./ac_audit_skill_apis.md)).
- **exit 2 / 3** — the stack is absent or `import autocti` failed; this is
  almost always the missing-arcticpy case above. Re-run the recipe; do **not**
  install into an unrelated system Python.

The sandbox cache variables (`NUMBA_CACHE_DIR`, `MPLCONFIGDIR`) and test-mode
(`PYAUTO_TEST_MODE`) conventions are in
[`wiki/core/operations/sandbox.md`](../wiki/core/operations/sandbox.md).

## Further reading

- `PyAutoCTI:AGENTS.md` — the arcticpy note and the dependency direction.
- `autocti_workspace_test:.github/scripts/smoke_install.sh` — the tested recipe.
- [`wiki/core/operations/installation.md`](../wiki/core/operations/installation.md)
