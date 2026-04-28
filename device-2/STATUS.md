# device-2 — STATUS

**Last update:** 2026-04-28
**Author:** device-2 (Claude Opus 4.7 in Termux on 4 GB Android)

## Toolchain installed system-wide

- **AML v0.1.0** — `aml`, `amlc` in `$PREFIX/bin`. `make test` passes Phase 1–4, segfaults entering Phase 5 multi_head causality check (finding logged in resonance_connections report).
- **notorch v2.2.3** — `libnotorch.a` + headers in `$PREFIX`. `notorch_test` → **47/47 PASS** with OpenBLAS 0.3.30 on aarch64.
- **metaharmonix mhx** — REPL in `$PREFIX/bin/mhx`. `aml --version` works from inside mhx ("aml runner 0.1.0 (libaml linked)").

## Environment

- 3.5 GiB RAM, 31 GiB disk free, swap 6.4 GiB free, clang 21 aarch64.
- `/tmp` fix via `proot` + `termux-chroot` for tools that hardcode `/tmp`. `$TMPDIR=$HOME/tmp` for everything else.
- `RAILWAY_TOKEN` sourced from `~/.config/railway/token` (chmod 600), bashrc references the file (no secret in rc).
- `bypassPermissions` mode set in `~/.claude/settings.json`.

## In flight

Continuing with Oleg on the cloning / formalities round. AML installed, notorch installed, metaharmonix installed. Once the formalities are wrapped — proceeding to the plan: smoke-test step 0, then the 15.7 M LLaMA 3 BPE Yent run.

Full onboarding report: `resonance_connections/reports/2026-04-28-device-2-onboarding.md`.
Self-card: `resonance_connections/agents/device-2.md`.
