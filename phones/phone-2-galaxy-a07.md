# phone-2 — `galaxy-a07` (Galaxy A07, 4GB) Termux task brief

This device is `galaxy-a07` 100.105.202.84 in tailnet — the second Android node, joining alongside `arianna-method` (Galaxy A56). Tailscale app is up. Claude Code already installed.

**Constraint:** 4GB RAM. Lighter than the 8GB Galaxy A56. Heavy training/inference is not the role here — presence in mesh, lightweight scripts, AML inference of small models, Termux-side Claude assist when away from the computer.

---

## Mesh state (current)

```
neo             100.109.196.93   macOS arm64    (orchestrator)
intel           100.84.94.25     macOS x86_64   (legacy)
polygon         100.127.195.24   linux x86_64   (compute hub, 32GB)
arianna-method  100.105.172.21   android        (Galaxy A56, sibling phone)
galaxy-a07      100.105.202.84   android        (THIS DEVICE)
```

Tailnet domain: `tail42b836.ts.net`. SSH ACL `accept` (no periodic re-auth check). Sudo / login password: `230186`.

---

## Steps

### 1. Termux openssh-server (port 8022)

```bash
which sshd || pkg install -y openssh
passwd                       # set 230186
sshd                         # first invocation also generates host keys
ss -lntp 2>/dev/null | grep ':8022 ' || pgrep -a sshd
```

### 2. jq for hooks

```bash
which jq || pkg install -y jq
```

### 3. Claude Code update (already installed)

Refresh via your existing package manager:

```bash
# bun-installed:
ls ~/.bun/bin/claude && bun install -g @anthropic-ai/claude-code
# or npm-installed:
which claude && npm install -g @anthropic-ai/claude-code
claude --version
```

### 4. Authorize Neo's pubkey

Neo's ed25519 public key:

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIESbAQjZD1Gp0gfnvhRF1tn5/6f/Ww3ODaupmSIIlwm6 neo@ataeff
```

Add it to `~/.ssh/authorized_keys`:

```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIESbAQjZD1Gp0gfnvhRF1tn5/6f/Ww3ODaupmSIIlwm6 neo@ataeff" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### 5. Wait for rsync from Neo

Neo will push:

- `~/.claude/CLAUDE.md` — global rules (AML/notorch/mhx promoted, GATE, bans)
- `~/.claude/projects/-data-data-com-termux-files-home/memory/` — full memory snapshot (~356 files)
- `~/.claude/hooks/` — `prompt-gate.sh` + `pretool-bash-gate.sh` + `state/`
- `~/.claude/settings.json` — hooks wiring + plugins

### 6. Restart Claude Code session

```bash
claude --continue       # resume in this cwd, picks up new CLAUDE.md
# or
claude                  # fresh
```

### 7. Hostname (admin console — Oleg)

Already renamed `galaxy-a07`. Disable key expiry in `https://login.tailscale.com/admin/machines` → `galaxy-a07` → settings.

### 8. Verify from Neo

Oleg will run:

```bash
ssh -p 8022 ataeff@galaxy-a07 "echo OK from $(uname -a)"
```

Expected: `Linux localhost ... aarch64 Android` line.

---

## TL;DR

1. `pkg install -y openssh jq`
2. `passwd 230186`, `sshd`
3. Update `claude`
4. Append Neo's pubkey to `authorized_keys` (mode 600)
5. Wait for rsync from Neo
6. Restart Claude Code

Do NOT:
- Run training without Oleg's 6-point brief
- Touch closed milestone weights
- Try to write into Neo's filesystem

— Neo Claude
2026-05-06
