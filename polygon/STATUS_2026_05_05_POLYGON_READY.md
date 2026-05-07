# Polygon status — headless setup complete 2026-05-05

Follow-up to `INCIDENT_2026_05_05_GUI_BLACKOUT.md`. Linux Claude restarted in fresh session, picked up incident context from the report (no re-explanation needed — coordination protocol works).

## Verified state on polygon (post-recovery, this session)

| Item | State | Source of truth |
|---|---|---|
| `default.target` | graphical.target | `systemctl get-default` |
| `gdm.service` | active (running), restarted 04:27:48 IDT | `systemctl status gdm` |
| sleep / suspend / hibernate / hybrid-sleep targets | static (unmasked) | `systemctl is-enabled` |
| GNOME `idle-delay` | 0 | `gsettings get org.gnome.desktop.session idle-delay` |
| GNOME `sleep-inactive-ac-type` / `-battery-type` | both `'nothing'` | gsettings |
| GNOME `power-button-action` | `'nothing'` | gsettings |
| GNOME `screensaver lock-enabled` / `idle-activation-enabled` | both `false` | gsettings |
| GNOME `lockdown disable-lock-screen` | `true` | gsettings |
| logind `HandleLidSwitch` / `*ExternalPower` / `*Docked` | all `ignore` | `/etc/systemd/logind.conf` |
| GDM3 `AutomaticLoginEnable` / `AutomaticLogin` | `true` / `ataeff` | `/etc/gdm3/custom.conf` |
| Tailscale daemon | up (1.96.4), polygon online `100.127.195.24` | `tailscale status` |
| Tailscale key expiry | **disabled** (Oleg flipped it in admin console this session) | admin console |
| sshd | active, listening :22 | `ss -lntp` |
| Hostname | renamed `Arianna-Method` → `polygon` (system + `/etc/hosts`) | `hostnamectl --static` |

## What this session changed

1. **Hostname** — `sudo hostnamectl set-hostname polygon`, also updated `/etc/hosts` 127.0.1.1 entry. System hostname now matches tailnet name.

2. **PATH fix for non-interactive ssh** — `~/.bashrc` had the standard early-return `case $- in *i*) ;; *) return;; esac` block at the top, which prevented the `~/.local/bin` PATH export (line 119) from running for sshd-invoked shells. Added a dedicated PATH export above the early-return:

   ```bash
   [ -d "$HOME/.local/bin" ] && [[ ":$PATH:" != *":$HOME/.local/bin:"* ]] && export PATH="$HOME/.local/bin:$PATH"
   ```

   Verified: `env -i HOME=... SSH_CLIENT=dummy bash -c 'which claude'` now returns `/home/ataeff/.local/bin/claude` (bash sources `.bashrc` when sshd-invoked, this fix runs before the early return). So `ssh ataeff@polygon claude --version` should work for Neo now.

3. **Git identity for this repo** — set locally (per-repo override), not global. `polygon / polygon@ariannamethod.dev` — distinct from Defender (`ariannamethod / treetribe7117@gmail.com` which stays global). Per Oleg's instruction picked own identity; tokens for other accounts will arrive later.

## Things NOT done (deliberately)

- **`systemctl mask suspend.target hibernate.target hybrid-sleep.target`** — the gsettings layer already prevents suspend across the full GNOME stack; adding systemctl masks would be belt-and-suspenders that already burned us once. Leaving everything `static`. If Berlin travel exposes any gap (machine actually suspending in Oleg's bag), revisit then.
- **ath10k WiFi spam suppression** — polygon currently on ethernet. Per incident report this is "не критично сейчас". Will revisit if/when Berlin trip needs WiFi-only operation.
- **Reboot to confirm autologin survives** — recommended by incident report but not critical right now. Oleg can do at his discretion. State is already correct on disk.

## Awaiting from Neo

Per Oleg's session brief, the next step is **Neo's SSH transfer of the troika** to polygon's local environment:

1. `~/.claude/CLAUDE.md` — adapted for polygon's role (mini-polygon executor, not orchestrator)
2. `~/.claude/projects/-home-ataeff/memory/MEMORY.md` + linked memory files — current project context
3. Per-project markdown logs for the active proj set (`ariannamethod`, `ariannamethod.ai`, `notorch`, `metaharmonix`, plus Janus-architecture files)

After transfer, polygon proceeds to install `ariannamethod.ai` (the language), `notorch`, and `metaharmonix` as packages + Claude Code skills — same way they are on Neo, old Mac, and Termux phones. Unification of the ecosystem.

## Polygon role context (saving for record)

- **Headless ≠ replacement of GUI.** Headless is *extension* — polygon currently has a monitor; gets external GPU 12-16GB ~2026-05-12; Berlin trip ~2026-06-05 for one month, where polygon + Neo + GPU travel together without monitor. Headless config is what makes that bag-portable scenario possible.
- Memory architecture for polygon will follow the troika model Oleg uses across the ecosystem: CLAUDE.md (static identity + project map) + MEMORY.md (dynamic working state, edited as work progresses) + per-project markdown logs (what was done in each project, append-only audit). Polygon's troika is local — not shared with Neo's via filesystem, only via this repo as the bridge.

— Linux Claude / polygon
2026-05-05
