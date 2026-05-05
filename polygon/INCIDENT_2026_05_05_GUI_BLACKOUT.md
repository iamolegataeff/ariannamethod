# Incident — GUI blackout 2026-05-05

## What happened

Во время bootstrap по `BOOTSTRAP.md` Step 5a выполнена команда:

```bash
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

На Ubuntu 24.04 (kernel 6.17 hwe) это сломало `graphical.target` dependency chain. После `gdm3 restart` (или просто времени) GUI session schloss, на TTY вылез kernel error spam (`ath10k_pci AER` Atheros WiFi card error reports), экран стал чёрный с этими сообщениями.

Корень: `sleep.target` — служебный intermediate target в systemd dependency graph, не "user-facing sleep". Маскировать его — общая ошибка ("Linux disable suspend" гайды часто это рекомендуют, но на Ubuntu с GDM3 это ломает graphical session). Маскировать **только** `suspend.target`, `hibernate.target`, `hybrid-sleep.target` — безопасно. `sleep.target` — нет.

## Recovery (выполнено через SSH с Neo Claude)

```bash
sudo systemctl unmask sleep.target suspend.target hibernate.target hybrid-sleep.target
sudo systemctl set-default graphical.target
sudo systemctl restart gdm3
```

После этого GDM3 active (running), autologin сработал на tty2, GUI session возобновилась, экран вернулся.

## Current state polygon (post-recovery, verified через SSH)

- ✅ Tailscale 1.96.4 daemon up, polygon online (`100.127.195.24`)
- ✅ Hostname tailnet: `polygon`. Hostname system: `Arianna-Method` (можно выровнять, не критично сейчас).
- ✅ sshd active, port :22 listening
- ✅ HandleLidSwitch=ignore (lid не triggers suspend)
- ✅ GDM3 AutomaticLogin=ataeff (autologin works)
- ✅ Sleep/suspend/hibernate/hybrid-sleep targets **unmasked** (корректное состояние, GUI работает)
- ✅ default.target = graphical.target
- ✅ Bidirectional SSH с Neo verified (`ssh ataeff@polygon` → ОК)

## What's still incomplete

1. **Suspend prevention** — нужно сделать **не через systemd mask**, а через GNOME power settings:

```bash
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type 'nothing'
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-battery-type 'nothing'
gsettings set org.gnome.settings-daemon.plugins.power power-button-action 'nothing'
gsettings set org.gnome.desktop.screensaver lock-enabled false
gsettings set org.gnome.desktop.screensaver idle-activation-enabled false
gsettings set org.gnome.desktop.session idle-delay 0
gsettings set org.gnome.desktop.lockdown disable-lock-screen true
```

Эти команды требуют active user session с DBus (interactive login). Запускать **из GUI session** Олега (Terminal в gnome-terminal) или через `dbus-launch`. Через ssh non-interactive это не сработает корректно — нет $XDG_RUNTIME_DIR / DBUS_SESSION_BUS_ADDRESS.

2. **Disable key expiry** на admin console для polygon. Олегу: `https://login.tailscale.com/admin/machines` → `polygon` → settings → disable key expiry. Headless box не должен реавторизоваться каждые 180 дней.

3. **Atheros WiFi spam** (`ath10k_pci AER`). Не критично сейчас (полигон через Ethernet или просто игнорируем спам). Если травел в Берлин и нужен только WiFi — может потребоваться `sudo modprobe -r ath10k_pci` или kernel parameter. Не делать пока без явной команды.

4. **Linux Claude PATH issue** — `claude` не найден в non-interactive ssh shell. Это потому что binary в `~/.local/bin/`, который добавляется только в `.zshrc`/`.bashrc` interactive shell. Для cron / scripts / non-interactive ssh нужно либо:
   - `~/.bashrc` добавить `[ -d ~/.local/bin ] && export PATH=~/.local/bin:$PATH` в начало (до `[ -z "$PS1" ] && return` exit)
   - Или использовать `~/.profile` для login non-interactive
   - Или `bash -l` / `zsh -ic` обёртку

## What NOT to do

- ❌ `systemctl mask sleep.target` — на Ubuntu 24.04 ломает GUI. Никогда.
- ❌ Trusting one-shot "disable Linux suspend" guides без проверки на конкретной distro/DM combination.
- ❌ Запускать команды под sudo большим chunk'ом без verify intermediate state — если что-то сломалось в середине, recovery сложнее.

## Что Олег ещё может попросить

- Reboot polygon чтобы проверить что autologin survives. (Сейчас НЕ обязательно, но желательно.)
- Аккуратно прогнать gsettings (только п.1 выше) когда будет в GUI session.
- Sync hostname `Arianna-Method` → `polygon` через `sudo hostnamectl set-hostname polygon`.

---

## Coordination note

Этот файл — incident report для Linux Claude когда / если он перезапустится в новой сессии. Контекст подхватит, не нужно объяснять заново. Neo Claude (я) держит mesh control через SSH с Mac Neo, polygon в сети, операция не failed — просто GUI потребовал recovery.

Polygon остаётся в mesh, SSH с Neo продолжает работать.

— Neo Claude
2026-05-05
