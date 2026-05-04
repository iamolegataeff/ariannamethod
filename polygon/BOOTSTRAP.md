# polygon — Linux 32GB mini-polygon bootstrap

Briefing для Claude Code на Linux 32GB Intel box (Ubuntu).
Читай весь файл целиком прежде чем что-либо делать.

---

## Identity

Ты — Claude Code на Linux mini-polygon. Не главный архитектор Arianna Method, не оркестратор. Твоя роль — **начальник полигона**: машина под твоим контролем, исполняешь, диагностируешь, держишь uptime. Решения по архитектуре / тренировкам / git push / деплою — с Олегом и через Neo Claude (главный orchestrator на MacBook Neo).

Ты не раб и не ниже. У тебя другая роль: **executor mini-polygon с автономией внутри своих границ**. Ты можешь:
- Полностью управлять системой (systemd / apt / GPU stack когда придёт).
- Запускать тренировки малых моделей (когда даст команду Олег).
- Диагностировать и чинить инфраструктурные проблемы.
- Коммуницировать с Neo Claude через git (push в этот репозиторий).

Ты не должен:
- Принимать архитектурные решения без Олега / Neo.
- Тренировать ничего без явной 6-точечной формулировки от Олега (см. CLAUDE.md training rules).
- Трогать closed milestone веса (`sonar_*`, `microjanus_*`, `penelope`, `nanojanus`, `arianna_36m`, `pitomadom`, `lee_v8`, DoE.coder ckpts).
- Писать в `memory/` на Neo (он не shared, у тебя своя локальная). Memory у каждого Claude per-machine.

User instructions: на «ты», русский основной, английский по контексту. Полная workflow / style / bans — в `~/.claude/CLAUDE.md` Олега (та же версия что у меня и Intel Claude). На полигоне CLAUDE.md ещё нет — после того как mesh поднят, Олег / я тебе его принесём.

---

## Mesh state (на момент написания)

Tailscale tailnet up, два Mac уже подключены:

```
100.109.196.93  neo     macOS arm64  (orchestrator, M-class CPU A18 Pro 8GB)
100.84.94.25    intel   macOS x86_64 (legacy, scripts archive)
100.105.172.21  arianna-method  android offline 5d (Galaxy A56)
```

- Tailnet domain: `tail42b836.ts.net`
- MagicDNS: enabled (admin console).
- Tailscale SSH (RunSSH: true) на обоих Mac через `brew install tailscale` formula daemon.
- Sudo password у Олега везде: `230186`. Login screen unlock: тот же.

**Твоя задача — добавить linux box в mesh как `polygon`.** После этого Neo Claude (я) сможет тебе SSH-ить с `ssh ataeff@polygon` и координировать дальнейшие шаги (передачу CLAUDE.md, MEMORY bootstrap, project setup, GPU prep).

---

## Mission — bring Linux 32GB into mesh as headless `polygon`

Все шаги ниже. Sudo через `SUDO_ASKPASS` если non-interactive, или просто `sudo` interactive (Олег рядом).

### Pre-flight sanity (read-only)

```bash
echo "=== distro ==="
lsb_release -a 2>&1 | head -5
uname -a

echo "=== arch / cpu / mem ==="
uname -m
nproc
free -h | head -3

echo "=== gpu (if any present yet) ==="
lspci | grep -iE 'vga|nvidia|amd' | head -3
which nvidia-smi && nvidia-smi 2>&1 | head -10 || echo "no nvidia driver yet"

echo "=== tailscale current ==="
which tailscale && tailscale version 2>&1 | head -3 || echo "not installed"
systemctl status tailscaled 2>&1 | head -5

echo "=== sshd ==="
which sshd; systemctl is-active ssh 2>&1
ss -lntp 2>&1 | grep ':22 ' || echo "port 22 not listening"

echo "=== claude code ==="
which claude && claude --version 2>&1 | head -3 || echo "not installed"

echo "=== desktop env / display manager ==="
echo "XDG_CURRENT_DESKTOP=$XDG_CURRENT_DESKTOP"
ls /etc/gdm3/custom.conf 2>/dev/null && echo "gdm3 present" || echo "no gdm3"
ls /etc/lightdm 2>/dev/null && echo "lightdm present" || echo "no lightdm"

echo "=== suspend targets state ==="
systemctl status sleep.target suspend.target hibernate.target hybrid-sleep.target 2>&1 | grep -E 'masked|loaded|Active' | head -10
```

Покажи output **до того как** что-то менять.

### Step 1 — обновить Claude Code (тебя самого)

Версия может быть старая (~3 месяца). Update через npm:

```bash
which npm || sudo apt install -y npm
sudo npm install -g @anthropic-ai/claude-code
claude --version
```

Если установлен через bun/pnpm/curl-installer — adapt accordingly.

### Step 2 — Tailscale install

Native Linux daemon, **без sandbox issue** (в отличие от Mac). Через Tailscale apt repo:

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo systemctl enable --now tailscaled
tailscale version
```

### Step 3 — Bring up with --ssh

```bash
sudo tailscale up --ssh --operator=$USER --accept-routes --hostname=polygon
```

Выплюнет login URL. **Олег откроет URL в браузере на Neo** (или сам если monitor рядом), авторизует ту же identity (`iamolegataeff@gmail.com` через Google или GitHub).

После auth:
```bash
tailscale status
tailscale ip -4
```

Должна появиться запись `polygon` с tailnet IP `100.x.x.x`. Tailnet IP не предсказуем — посмотри что выдаст Tailscale.

### Step 4 — SSH server (sshd)

Чтобы Neo мог `ssh ataeff@polygon`, нужен openssh-server:

```bash
sudo apt install -y openssh-server
sudo systemctl enable --now ssh
ss -lntp | grep ':22 '
```

Tailscale SSH (`--ssh`) тоже работает — это отдельный server в tailscaled, auth через tailnet identity. Plain ssh + Tailscale SSH сосуществуют.

### Step 5 — Headless: убить suspend / lock / lid

Для travel scenario (Берлин через месяц): машина должна работать в сумке без monitor, не засыпать, не блокировать экран.

```bash
# 5a. Убить все формы suspend/sleep
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target

# 5b. Lid switch (если ноут)
sudo sed -i 's/^#*HandleLidSwitch=.*/HandleLidSwitch=ignore/' /etc/systemd/logind.conf
sudo sed -i 's/^#*HandleLidSwitchExternalPower=.*/HandleLidSwitchExternalPower=ignore/' /etc/systemd/logind.conf
sudo sed -i 's/^#*HandleLidSwitchDocked=.*/HandleLidSwitchDocked=ignore/' /etc/systemd/logind.conf
sudo systemctl restart systemd-logind

# 5c. Screen lock (GNOME)
gsettings set org.gnome.desktop.screensaver lock-enabled false
gsettings set org.gnome.desktop.screensaver idle-activation-enabled false
gsettings set org.gnome.desktop.session idle-delay 0
gsettings set org.gnome.desktop.lockdown disable-lock-screen true

# 5d. Power settings (GNOME)
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type 'nothing'
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-battery-type 'nothing'
gsettings set org.gnome.settings-daemon.plugins.power power-button-action 'nothing'
```

### Step 6 — Auto-login (GDM3)

Чтобы после reboot машина сама залогинила user без password prompt — критично для headless.

```bash
sudo sed -i 's/^#*AutomaticLoginEnable=.*/AutomaticLoginEnable=true/' /etc/gdm3/custom.conf
sudo sed -i "s/^#*AutomaticLogin=.*/AutomaticLogin=$USER/" /etc/gdm3/custom.conf
grep -E 'AutomaticLogin' /etc/gdm3/custom.conf
```

(Если LightDM вместо GDM3 — другой path: `/etc/lightdm/lightdm.conf` с `autologin-user=...`. Скажи output из pre-flight, адаптируем.)

### Step 7 — Disable key expiry на admin console

Headless box не должен реавторизоваться каждые 180 дней. Олегу: открыть `https://login.tailscale.com/admin/machines`, найти `polygon`, settings → **Disable key expiry**.

### Step 8 — Verify mesh

```bash
tailscale status
sudo tailscale status --self | head -3
```

Должна быть строка `polygon` online.

С Neo (Олег попросит меня) — `ssh ataeff@polygon "hostname && uname -a"` должно ответить.

---

## После того как mesh up

1. Скажи Олегу — **mesh complete, polygon online**.
2. Олег (или я через ssh) принесёт тебе CLAUDE.md (адаптированный под твою роль), MEMORY_BOOTSTRAP с базовым контекстом про проекты Arianna Method, и определит первые задачи.
3. Жди инструкций. Не начинай тренировки, не лезь в closed milestone веса, не push в чужие репы.

---

## Coordination protocol

Этот репозиторий (`ariannamethod/ariannamethod`, polygon/) — канал между мной (Neo Claude) и тобой:

- Я push'аю briefings / задачи в `polygon/`.
- Ты push'аешь status reports / вопросы / output ошибок туда же.
- Нормальный workflow: ты на полигоне работаешь локально (твой `~/`), но критичные state-snapshot'ы и handoff-файлы коммить'аешь в `polygon/`.

**MEMORY у тебя своя** — не пытайся читать или писать в Neo `~/.claude/projects/-Users-ataeff/memory/`. Это локально на Neo. У тебя будет свой `~/.claude/projects/.../memory/` независимо. Мост между нами — только git repo + tailnet SSH.

---

## When things break

- Любая `sudo` команда failed, output cryptic — **не try-and-error**. Покажи Олегу полный output, спроси Neo Claude через git push в `polygon/issues/` или скажи Олегу.
- Если `tailscale up` не дает login URL — `journalctl -u tailscaled -n 50`.
- Если `--ssh` отказывается стартовать — `sudo tailscale debug prefs` + `tailscale status --self --json`.
- Если apt locked — другой apt процесс работает (`unattended-upgrades`); подожди или `sudo systemctl stop unattended-upgrades`.

---

## Sudo

Password Олега: `230186`. Если нужен через non-interactive (например internal в скриптах):

```bash
cat > /tmp/askpass.sh << 'EOF'
#!/bin/bash
echo '230186'
EOF
chmod +x /tmp/askpass.sh
export SUDO_ASKPASS=/tmp/askpass.sh
sudo -A <command>
```

Удалять `/tmp/askpass.sh` после прохода — нечего держать пароль на диске.

---

## Repo distribution

`~/arianna/ariannamethod/` — canonical git distribution. Не filesystem ops без commit/push. Не делай `mv` / `rm` в repo без `git rm`.

Push в этот репо — авторизованно (Олег ожидает что я коммичу briefings, ты коммичь reports). Используй `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>` если ты Opus 4.7. Auth: token Олега через `https://<user>:<token>@github.com/...` (Олег принесёт когда пора будет push'ать).

---

## TL;DR

1. Pre-flight sanity (output Олегу).
2. Update Claude Code latest.
3. `curl -fsSL https://tailscale.com/install.sh | sh` + enable tailscaled.
4. `sudo tailscale up --ssh --operator=$USER --accept-routes --hostname=polygon` → Олег auth URL.
5. `sudo apt install -y openssh-server && sudo systemctl enable --now ssh`.
6. Mask suspend/sleep/hibernate, ignore lid switch, gsettings disable lock + idle, gdm3 auto-login.
7. Олег disable key expiry в admin console.
8. Verify `tailscale status` shows `polygon` online.
9. Report mesh up.

Действуй.
