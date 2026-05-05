# phones — Galaxy A56 + phone-2 bootstrap

Briefing для Termux setup на двух Android устройствах после Tailscale app login. Шаги в Termux на каждом телефоне.

---

## Mesh state (на момент написания)

```
neo      100.109.196.93    macOS arm64   (Mac Neo, orchestrator)
intel    100.84.94.25      macOS x86_64  (Mac Intel, legacy)
polygon  100.127.195.24    linux x86_64  (Linux 32GB, mini-polygon)
```

Tailnet domain: `tail42b836.ts.net`. MagicDNS включён.

---

## Step 1 — Tailscale (через Tailscale app, не Termux)

Уже сделано:
- Tailscale app from Play Store
- Sign in Google `iamolegataeff` (та же identity что везде)
- Tap **Connect**

Verify on Neo:
```bash
ssh ataeff@neo  # с phone в Termux
# или с Mac:
tailscale status  # должен показать phone online
```

---

## Step 2 — Termux baseline (на каждом телефоне)

```bash
# update packages
pkg update -y && pkg upgrade -y

# core utilities
pkg install -y openssh git curl wget jq nodejs python  # python optional
termux-setup-storage  # доступ к /sdcard
```

---

## Step 3 — Termux SSH server (для reverse access from Neo)

Termux sshd по default слушает `:8022`, не `:22`.

```bash
# install
pkg install -y openssh

# set password (для SSH login)
passwd  # введи 230186 (тот же что sudo)

# generate host keys + start sshd
sshd

# verify listening
ss -lntp | grep ':8022 '

# port forwarding (если нужно через nginx или подобное — опционально)
```

Проверь с Neo (после того как phone в tailnet):

```bash
ssh ataeff@galaxy -p 8022   # или другой tailnet name
ssh ataeff@phone2 -p 8022   # для второго
```

Pubkey auth (вместо пароля):

```bash
# на phone в Termux:
mkdir -p ~/.ssh && chmod 700 ~/.ssh

# с Neo: copy pub key
ssh-copy-id -p 8022 ataeff@<phone-tailnet-ip>
# или manually scp:
# scp -P 8022 ~/.ssh/id_ed25519.pub ataeff@<phone>:~/.ssh/authorized_keys
```

---

## Step 4 — Claude Code (Galaxy A56 only — phone-2 4GB слаб)

Claude Code на Galaxy:

```bash
pkg install -y nodejs
npm install -g @anthropic-ai/claude-code
claude --version
```

При первом запуске — login (открой URL в browser, авторизуй).

Если установлен старый — update:

```bash
npm update -g @anthropic-ai/claude-code
```

**Phone-2 (4GB):** Claude Code избыточен. Только Tailscale + sshd для presence.

---

## Step 5 — Bootstrap CLAUDE.md + memory (Galaxy only)

Если хочешь Galaxy Claude знал rules + project context — Neo / polygon могут rsync через Tailscale:

```bash
# с Neo:
rsync -a ~/.claude/CLAUDE.md -e 'ssh -p 8022' ataeff@galaxy:~/.claude/CLAUDE.md
rsync -a ~/.claude/projects/-Users-ataeff/memory/ -e 'ssh -p 8022' ataeff@galaxy:~/.claude/projects/-data-data-com.termux-files-home/memory/
rsync -a ~/.claude/hooks/ -e 'ssh -p 8022' ataeff@galaxy:~/.claude/hooks/
rsync -a ~/.claude/settings.json -e 'ssh -p 8022' ataeff@galaxy:~/.claude/settings.json
```

(Termux Claude project dir =`~/.claude/projects/-data-data-com.termux-files-home/` потому что home = `/data/data/com.termux/files/home`. Verify path первым.)

После rsync — Galaxy Claude получает full troika (CLAUDE.md + memory + hooks).

Hooks (`prompt-gate.sh`, `pretool-bash-gate.sh`) работают на Termux native — bash есть.

---

## Step 6 — admin console rename

`https://login.tailscale.com/admin/machines`:
- `arianna-method` → `galaxy` (или `phone1`)
- new device → `phone2` (или `pixel`)

Также **disable key expiry** для headless behavior (phones не должны re-auth каждые 180 дней).

---

## Step 7 — verify mesh с Neo

```bash
tailscale status
ssh ataeff@galaxy -p 8022 "echo OK from \$(hostname)"
ssh ataeff@phone2 -p 8022 "echo OK from \$(hostname)"
```

После — phones officially в mesh, можно команды слать через ssh с Neo.

---

## Phone constraints

- **Galaxy A56 (8GB)** — Claude Code OK, training inference small models OK, ssh full duplex.
- **Phone-2 (4GB)** — Tailscale + sshd only. Don't run Claude Code there. Не training. Used as reachable endpoint.

---

## Coordination

Phones в mesh — extension не replacement. Mac Neo + polygon — primary compute. Phones для:
- Mobile presence (Telegram-style messaging eventually через mesh-agent когда написан)
- Termux-side Claude (Galaxy) когда не у компа
- Termux scripts, AML inference small models

Push reports / questions — этот repo `polygon/` style (если нужен handoff). Phone Claude push в `phones/` если actually работает.
