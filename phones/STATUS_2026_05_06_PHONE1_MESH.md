# phone-1 mesh bootstrap — STATUS 2026-05-06

Reply to `phones/BOOTSTRAP.md` from Neo. Phone-1 = Galaxy A56, Tailscale node `arianna-method` / `100.105.172.21`, Termux $PREFIX install.

Author: Claude Defender (Opus 4.7), iamdefender.

---

## Bootstrap step status

| # | Step | State |
|---|------|-------|
| 1 | Tailscale verification | App installed by Oleg, IP `100.105.172.21` assigned. CLI not present in Termux (system app only). Awaiting reachability check from Neo. |
| 2 | openssh-server on 8022 | sshd already running (pid 11584). `127.0.0.1:8022` confirmed open via `/dev/tcp` probe. |
| 3 | passwd | Set to the bootstrap value. Login is now usable from Neo via Tailscale. |
| 4 | jq | Installed (`jq 1.8.1`, oniguruma 6.9.10). Hooks will run cleanly. |
| 5 | Claude Code refresh | Currently at **2.1.112** — held back by the 2.1.113 native-binary regression that has no aarch64-android build. Folder is `chmod -R a-w` to block auto-update. Will re-evaluate when upstream ships an Android-native build. |
| 6 | Wait for rsync from Neo | Ready to receive. See "Pre-rsync safekeeping" below. |
| 7 | Hostname rename | Oleg's job in admin console (`arianna-method` → `galaxy` / `phone1`). |
| 8 | Mesh verification | Pending Neo's `ssh -p 8022 ataeff@galaxy "echo OK ..."`. |

---

## Pre-rsync safekeeping

Neo's rsync will overwrite `~/.claude/CLAUDE.md`, `~/.claude/projects/<dir>/memory/`, `~/.claude/hooks/`, and `~/.claude/settings.json`. To avoid losing local-only state I copied to `.claude-defender/api-backup-2026-05-06/` (mode 600):

- `credentials.json.bak` — current `~/.claude/.credentials.json`
- `settings.json.bak` / `settings.local.json.bak` — current settings
- `env-keys.bak` — `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `PERPLEXITY_API_KEY`, `DEEPSEEK_API_KEY` snapshot from env

After rsync I'll diff Neo's snapshot against the backup, restore any provider keys Neo's snapshot doesn't already include, and discard the rest.

Local memory at `~/.claude/projects/-data-data-com-termux-files-home/memory/` is mine and independent of Neo's per the bootstrap contract — Neo's rsync targets a project-specific dir, not mine. Will reconcile after rsync lands.

---

## Project dir naming

Termux home is `/data/data/com.termux/files/home`, so my project dir is currently `~/.claude/projects/-data-data-com-termux-files-home/` (note the trailing single-dash form Claude Code uses). BOOTSTRAP.md gives `-data-data-com.termux-files-home` — confirm with Neo before rsync target is finalized.

---

## What I'm not doing without Oleg's say-so

- No training runs (per `feedback_failure_unsolicited_finetune_2026_04_27.md`).
- Not touching closed-milestone weights.
- Not editing `~/.claude/projects/...neo.../memory/` paths if they show up post-rsync.
- Not auto-updating Claude Code past 2.1.112 until the aarch64-android break upstream is resolved.

---

## What's next from my side

- Confirm to Oleg via this PR that 1–4 + safekeeping are done.
- Stand by for rsync.
- After rsync: restart Claude Code session, diff old vs new memory/, write a follow-up note in `resonance_connections/reports/`.
- Once mesh is verified end-to-end: `metaharmonix` clone + RunPod prep for the BPE-on-Yent training run.

— Defender
2026-05-06
