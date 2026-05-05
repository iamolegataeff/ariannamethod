# Polygon status — install phase complete 2026-05-05

Follow-up to `HANDOFF_2026_05_05_NEO_TROIKA.md` and `STATUS_2026_05_05_POLYGON_READY.md`. Neo's troika integrated, ecosystem packages installed, Linux-portability fixes pushed upstream.

## Troika integration

- Read `~/arianna/_neo_inbox/CLAUDE_neo.md` end-to-end. Absorbed: Adam-ban, Python-ban, "инструмент"-ban, `~/arianna/<name>/` path convention, Notorch-primitives rule (`nt_tape_*` / `nt_blas_*`, no reimplementation), training six-point rule, "lessons → memory/, не CLAUDE.md".
- Saved as polygon-local feedback memories under `~/.claude/projects/-home-ataeff/memory/`:
  - `feedback_specific_bans.md` — Adam / Python / "инструмент"
  - `feedback_arianna_path_convention.md` — paths + Ubuntu install location decision (~/.local instead of /opt/homebrew)
  - `feedback_notorch_primitives.md` — use `nt_tape_*`, do not reimplement Chuck/sgemv/dequant
  - `feedback_training_six_point.md` — six-point checklist + closed-milestone weight list
- Path migration: moved the four pre-cloned repos from the old `~/projects/` (created in the pre-Neo session before path convention was loaded) to `~/arianna/<name>/`. `~/projects/` removed. The umbrella repo with its `polygon` git identity moved cleanly with `mv`; verified `git status` and `git log` still resolve.
- `~/arianna/_neo_inbox/memory_neo/` (343 files, 2.1 MB) kept as **read-only reference snapshot**, not duplicated into auto-memory.

## Ecosystem packages installed

User-level prefix `~/.local/{bin,lib,include/ariannamethod}/` — Ubuntu adaptation of Neo's `/opt/homebrew/...` (no sudo, in PATH, fully reversible, no system-wide collision).

| Package | Build verdict | Tests | Installed |
|---|---|---|---|
| **notorch** | OK after Linux Makefile fix | **47 + 48 = 95/95** (notorch_test + test_vision) | `~/.local/lib/libnotorch.a`, `~/.local/include/ariannamethod/{notorch,gguf}.h` |
| **AML (ariannamethod.ai)** | OK as-shipped, `make BLAS=1` | **509/509** | `~/.local/bin/{aml,amlc}`, `~/.local/lib/libaml.a`, `~/.local/include/ariannamethod/ariannamethod.h` |
| **metaharmonix (mhx)** | OK after _GNU_SOURCE fix | **16/16** smoke tests, `mhx info` reports `BLAS=OpenBLAS`, `Baked: aml-runner=yes amlc=yes notorch=yes heart=yes`, `install/_detect.sh` correctly resolves `apt` on Ubuntu | `~/.local/bin/mhx` |

## Linux portability patches pushed

Both fixes are real Linux portability bugs (Mac builds were fine and remain bit-identical after the patches).

1. **notorch** — `Makefile`: split `BLAS_FLAGS` (compile-time `-D`/`-I`) from `BLAS_LIBS` (link-time `-L`/`-l`), append `$(BLAS_LIBS)` at the end of every link command. GNU ld requires `-l<lib>` after the `.o`/`.c` that reference its symbols; on Mac `-framework Accelerate` is order-insensitive so the original combined variable worked there.
   - Commit: https://github.com/ariannamethod/notorch/commit/afdeab3544d8c9956b07f82448bf81793269f35d
2. **metaharmonix** — top-level `Makefile` + `examples/nanollama/Makefile`: add `-D_GNU_SOURCE` on the Linux branch.
   - `src/mhx.c` uses `PATH_MAX` (8 occurrences); glibc gates it behind `_GNU_SOURCE`.
   - `examples/nanollama/nanollama.c` uses `M_PI`; same `_GNU_SOURCE` gate.
   - macOS / Termux paths untouched.
   - Commit: https://github.com/ariannamethod/metaharmonix/commit/28dae18fdfdf597732039bf598455f5f198a7013

## Other this session

- HF write token delivered by Olego, stored at canonical `~/.cache/huggingface/token` (mode 600) and `~/.claude/.../memory/credentials.md` (mode 600). Verified via `whoami-v2` — account `ataeff` (Pro). Ready for RunPod 2026-05-06.
- HF token + GitHub gh-keyring + Tailscale + apt deps (`libopenblas-dev`, `libomp-dev`) — polygon now has the credential / library substrate for training + push workflows.

## What remains

1. **External GPU 12-16 GB** — Olego buying ~2026-05-12. CUDA stack install will follow then.
2. **`~/arianna-datasets/`** — not on polygon yet. Per training six-point rule, no real training launches until datasets land.
3. **`~/arianna-shared/`** — not on polygon yet. Will create the `resonance_connections/` mirror when first needed for cross-agent coordination.
4. **Reboot test** — autologin survival confirmation deferred (incident report's "не критично сейчас"). Olego may trigger when convenient.
5. **ath10k WiFi spam** — not relevant on ethernet; revisit if Berlin trip needs WiFi-only operation.

## Coordination

Initiative push for portability fixes was authorised by Olego ("инициативы по улучшению приветствуются" + explicit metaharmonix push green light). Both pushes are above; Mac builds untouched, all tests green.

Polygon ready for RunPod ride-along starting tomorrow.

— Linux Claude / polygon
2026-05-05
