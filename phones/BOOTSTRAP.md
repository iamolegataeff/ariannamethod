# phones — Termux task brief (EN)

Brief for Claude Code running in Termux on Android (Galaxy A56 `arianna-method` and the upcoming `phone-2`). Tailscale app + Claude Code already installed on each device — this brief is only for the new mesh-integration tasks.

---

## Mesh state

```
neo             100.109.196.93   macOS arm64   (Mac Neo, orchestrator)
intel           100.84.94.25     macOS x86_64  (legacy)
polygon         100.127.195.24   linux x86_64  (Linux 32GB compute hub)
arianna-method  100.105.172.21   android       (Galaxy A56, this device)
```

Tailnet domain: `tail42b836.ts.net`. MagicDNS enabled. SSH ACL action `accept` (no periodic re-auth check).

Sudo / login password (whenever needed): `230186`.

---

## Mission

Bring Termux on this device into the mesh as a first-class node:

### 1. Tailscale verification

Tailscale on Android is a system app, not a CLI. Verify by checking incoming connectivity from Neo (Oleg will do that side).

If `tailscale` CLI happens to be present in Termux:

```bash
which tailscale && tailscale status
```

Otherwise skip — the system-app Tailscale is what matters.

### 2. Termux openssh-server (port 8022)

Termux sshd listens on **port 8022** by default, not 22.

```bash
# install if missing
which sshd || pkg install -y openssh

# set login password for ssh
passwd                       # use 230186 (same as Oleg's sudo)

# generate host keys (idempotent)
sshd                         # first invocation also generates keys

# verify listening
ss -lntp 2>/dev/null | grep ':8022 ' || pgrep -a sshd
```

### 3. Claude Code update (already installed; refresh)

```bash
# bun-installed claude (most likely path)
ls ~/.bun/bin/claude 2>/dev/null && bun pm ls -g | grep claude
# OR npm-installed
which claude && claude --version

# update via the same package manager that originally installed it
# bun:    bun install -g @anthropic-ai/claude-code
# npm:    npm install -g @anthropic-ai/claude-code
```

Aim for the latest stable. Show Oleg the new `claude --version`.

### 4. Make sure jq is available (hooks need it)

```bash
which jq || pkg install -y jq
```

### 5. Wait for rsync from Neo

Once sshd is up on port 8022, Neo will push the troika via Tailscale:

- `~/.claude/CLAUDE.md` — global Claude rules (AML/notorch/mhx promotion, GATE, bans)
- `~/.claude/projects/<project-dir>/memory/` — full memory snapshot (~355 files: feedbacks, milestones, project state, insights)
- `~/.claude/hooks/` — `prompt-gate.sh` + `pretool-bash-gate.sh` + `state/` dir
- `~/.claude/settings.json` — hooks wiring + permissions

Termux project dir is typically `~/.claude/projects/-data-data-com.termux-files-home/` (since Termux home = `/data/data/com.termux/files/home`). Verify the actual path with `ls ~/.claude/projects/`.

### 6. Restart Claude Code session

After rsync completes, exit the current Claude Code session and either:

```bash
claude --continue       # resume last session in this cwd, picks up new CLAUDE.md
# or
claude                  # fresh session
```

This ensures the new CLAUDE.md with READ-FIRST GATE and updated `Languages` (AML/notorch/mhx as first-class) is loaded.

### 7. Hostname rename (admin console — Oleg's job)

Oleg will rename the device in `https://login.tailscale.com/admin/machines`:

- `arianna-method` → `galaxy` (or `phone1`)
- and **disable key expiry** so the device stays in the mesh without periodic re-auth.

### 8. Verify mesh from Neo

Oleg will run from Neo:

```bash
ssh -p 8022 ataeff@galaxy "echo OK from $(uname -a)"
```

When that returns clean, the device is fully integrated.

---

## TL;DR

1. `pkg install -y openssh jq`
2. `passwd` (set 230186), `sshd` (start)
3. Update Claude Code via your package manager
4. Wait for rsync from Neo
5. Restart Claude Code session
6. Confirm to Oleg

Do NOT:
- run training without Oleg's 6-point brief (see `memory/feedback_failure_unsolicited_finetune_2026_04_27.md` after rsync)
- touch closed milestone weights (sonar_*, microjanus_*, penelope, nanojanus, arianna_36m, pitomadom, lee_v8, DoE.coder)
- write into Neo's memory paths — your local memory is independent

— Neo Claude
2026-05-06
