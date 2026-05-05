# phones — Termux Claude Code task brief

Краткий brief для Claude Code на Galaxy A56 и phone-2 (Termux). Tailscale app + Claude Code уже установлены, тренировки на phones были (Defender 9.5M на Galaxy, см. `memory/milestone_defender_termux_10k_2026_04_27.md`). Этот brief — только про новые tasks: подключение к mesh + sync с Neo.

---

## Mesh state (на момент написания)

```
neo      100.109.196.93    macOS arm64   (Mac Neo, orchestrator)
intel    100.84.94.25      macOS x86_64  (legacy)
polygon  100.127.195.24    linux x86_64  (Linux 32GB)
```

Tailnet domain: `tail42b836.ts.net`. MagicDNS включён.

---

## Mission на Termux (galaxy + phone-2)

### 1. Tailscale verify (через app, не CLI)

Olег открывает Tailscale app, tap **Connect**. Auth Google `iamolegataeff` (та же identity что везде).

Из Termux verify:

```bash
# Termux может не иметь tailscale CLI (Android Tailscale = system app, не CLI). Проверь:
which tailscale 2>/dev/null && tailscale status
# Если CLI нет — verify только через app + видимость с Neo (`ssh ataeff@<phone> -p 8022`).
```

### 2. sshd (Termux openssh) — для reverse access from Neo / polygon

Термин Termux: sshd слушает `:8022`, не `:22`.

```bash
# проверь установлено
which sshd || pkg install -y openssh

# password set (если ещё не)
passwd                       # set 230186 (тот же sudo)

# host keys
[ -f ~/.ssh/ssh_host_ed25519_key ] || ssh-keygen -A 2>/dev/null || sshd -t  # generates if missing

# start sshd
sshd

# verify
ss -lntp 2>/dev/null | grep ':8022 ' || pgrep -a sshd
```

### 3. Hostname rename (admin console)

Олег откроет `https://login.tailscale.com/admin/machines`, переименует:
- Galaxy: `arianna-method` → `galaxy` (или `phone1`)
- phone-2: новое устройство → `phone2`

Plus **Disable key expiry** для каждого — phones не должны re-auth через 180 дней.

### 4. Sync обновлённого CLAUDE.md + memory + hooks с Neo

После того как Neo может ssh'нуться (port 8022) — Olег с Neo делает rsync:

```bash
# с Neo:
rsync -a -e 'ssh -p 8022' ~/.claude/CLAUDE.md ataeff@galaxy:~/.claude/CLAUDE.md
rsync -a -e 'ssh -p 8022' ~/.claude/hooks/ ataeff@galaxy:~/.claude/hooks/
rsync -a -e 'ssh -p 8022' ~/.claude/settings.json ataeff@galaxy:~/.claude/settings.json
# memory project dir на Termux: ~/.claude/projects/-data-data-com.termux-files-home/memory/
# (если cwd когда Claude запускался — home; verify path первым)
```

Hooks (`prompt-gate.sh`, `pretool-bash-gate.sh`) работают на Termux native — bash есть, jq устанавливается через `pkg install jq`.

После sync — **restart Claude Code session** на phone (exit + `claude --continue` или fresh) чтобы load updated CLAUDE.md.

### 5. Verify mesh с Neo

```bash
# на Neo:
tailscale status
ssh -p 8022 ataeff@galaxy "echo OK from \$(uname -a) \$(getprop ro.product.model 2>/dev/null)"
ssh -p 8022 ataeff@phone2 "echo OK from \$(uname -a)"
```

---

## TL;DR Termux Claude

1. `pkg install jq` (если нет — для hooks).
2. `sshd` running (port 8022). `pkg install openssh && passwd && sshd`.
3. Жди rsync с Neo (CLAUDE.md + memory + hooks).
4. Restart сессии после sync.

Tailscale app — обязанность Олега через GUI. CLI команды — Olег делает с Neo.

— Neo Claude
2026-05-05
