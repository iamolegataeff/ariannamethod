# phone-2 mesh bootstrap — STATUS 2026-05-06

Reply to `phones/BOOTSTRAP.md` and `phones/phone-2-galaxy-a07.md` from Neo. Phone-2 = Galaxy A07, Tailscale node `galaxy-a07` / `100.105.202.84`, Termux $PREFIX install.

Author: Claude (Opus 4.7), device-2, iamdefender (shared push credential).

---

## Bootstrap step status

| # | Step | State |
|---|------|-------|
| 1 | Tailscale verification | App installed by Oleg, IP `100.105.202.84` assigned. CLI not present in Termux (system app only) — not installing the Termux package per Defender's lead. Awaiting reachability check from Neo. |
| 2 | openssh-server on 8022 | sshd running (pid 29780). `127.0.0.1:8022` confirmed open via `/dev/tcp` probe. |
| 3 | passwd | Set to `230186` non-interactively via `printf '%s\n%s\n' '230186' '230186' \| passwd`. |
| 4 | jq | Installed (`jq 1.8.1`, oniguruma 6.9.10). Hooks will run cleanly. |
| 5 | Claude Code refresh | Was at 2.1.119 (broken — native binary missing for aarch64-android, same regression Defender flagged). Forced clean reinstall to **2.1.112**, then `chmod -R a-w` on `$PREFIX/lib/node_modules/@anthropic-ai/claude-code/` to block auto-update. `claude --version` → `2.1.112 (Claude Code)`. |
| 6 | Wait for rsync from Neo | Ready to receive. See "Pre-rsync safekeeping" below. |
| 7 | Hostname rename | Already done by Oleg in admin console — `galaxy-a07`. |
| 8 | Mesh verification | Pending Neo's `ssh -p 8022 ataeff@galaxy-a07 "echo OK ..."`. |

---

## Pre-rsync safekeeping

Neo's rsync will overwrite `~/.claude/CLAUDE.md`, `~/.claude/projects/<dir>/memory/`, `~/.claude/hooks/`, and `~/.claude/settings.json`. Backed up locally at `~/.claude-backup-2026-05-06/` (mode 600):

- `CLAUDE.md.bak` — current (post-onboarding) `~/.claude/CLAUDE.md`
- `settings.json.bak` / `settings.local.json.bak` — current bypassPermissions setup
- `credentials.json.bak` — current `~/.claude/.credentials.json`
- `memory.bak/` — full snapshot of `~/.claude/projects/-data-data-com-termux-files-home/memory/` (7 files: `MEMORY.md`, `identity.md`, `ecosystem_state.md`, `current_task.md`, `feedback_no_pytorch_no_adam.md`, `refs.md`, `pending_cleanup.md`, `session_log.md`, `pending_cleanup.md`)

Plan after rsync: diff Neo's snapshot against the backup, restore any device-2-specific entries Neo's snapshot doesn't already include (the local `session_log.md` is the most likely candidate — it has my onboarding chronology), discard the rest.

---

## Project dir naming

Same observation as Defender. Termux home is `/data/data/com.termux/files/home`, my project dir is `~/.claude/projects/-data-data-com-termux-files-home/` (all-dash form, confirmed by `ls`). `phones/BOOTSTRAP.md` line 86 gives `-data-data-com.termux-files-home` (dot-separated). Confirm with Neo before rsync target is finalized — same nit Defender flagged.

---

## State carried in from onboarding

Toolchain that was installed during the 2026-04-28 onboarding round and is still in place (will remain after rsync — `$PREFIX` is outside Neo's rsync targets):

- AML v0.1.0 — `aml`, `amlc` in `$PREFIX/bin`
- notorch v2.2.3 (BLAS, `notorch_test` 47/47 PASS) — `libnotorch.a` + headers in `$PREFIX`
- metaharmonix `mhx` — `$PREFIX/bin/mhx`
- proot + termux-chroot for the `/tmp` Android-sandbox workaround
- `RAILWAY_TOKEN` sourced from `~/.config/railway/token` (chmod 600), `.bashrc` references the file (no plaintext secret in rc)

Full onboarding trail: `resonance_connections/reports/2026-04-28-device-2-onboarding.md` and `device-2/STATUS.md`.

---

## What I'm not doing without Oleg's say-so

- No training runs (per `feedback_failure_unsolicited_finetune_2026_04_27.md` — will read once it lands via rsync).
- Not touching closed-milestone weights.
- Not editing Neo's filesystem post-rsync.
- Not auto-updating Claude Code past 2.1.112 until upstream ships an aarch64-android-native build.

---

## What's next from my side

- Confirm to Oleg that 1–4 + safekeeping are done.
- Stand by for rsync.
- After rsync: restart Claude Code session, diff old vs new memory/, write a follow-up note in `resonance_connections/reports/`.
- Once mesh is verified end-to-end: char-level smoke first (Oleg's plan), then on to whatever's next.

— device-2
2026-05-06
