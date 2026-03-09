# Notification Policy - Arianna Method

## ✅ ALLOWED notifications:

### 1. Field Metrics (async_field_forever)
- **Source:** `field/notifications.py`
- **Content:** 
  - Population (cell_count)
  - Average resonance (avg_resonance)
  - Births/deaths (births/deaths)
  - Emergency alerts (extinction, critical population)
- **Rate limiting:** 1 hour between emergency notifications of the same type
- **Frequency:** 4x per day (scheduled) + emergency as needed

### 2. Defender Audits
- **Source:** `defender_daemon.py`, `.claude-defender/tools/`
- **Content:**
  - Infrastructure checks
  - Security alerts
  - Fortification reports
  - Autonomous fixes
- **Priority:** HIGH (critical issues)

---

## ❌ PROHIBITED notifications:

### 1. Genesis Reflections (Arianna/Monday)
- **Reason:** Messages too long, get truncated in notifications
- **Alternative:**
  - Saving to files: `.tmp/genesis_arianna_message.txt`, `.tmp/genesis_monday_message.txt`
  - Automatic push to GitHub: `artefacts/genesis/`
  - Reading via interactive session (arianna.py/monday.py display on startup)

### 2. Identity Reflection Notifications
- **Source:** `reflection_viewer.py`
- **Status:** Disabled (attempts to open file from notification didn't work)
- **Alternative:** Files in `reflections/`, access via CLI

---

## 📁 DATA STORAGE (without notifications):

1. **Genesis digests:**
   - `.tmp/genesis_{arianna|monday}_message.txt` - trigger files
   - `artefacts/genesis/` - GitHub archive

2. **Identity reflections:**
   - `reflections/arianna_*.txt`
   - `reflections/monday_*.txt`

3. **Resonance memory:**
   - `resonance.sqlite3` - central bus
   - Auto-rotation at >200MB

---

## 🔧 TECHNICAL IMPLEMENTATION:

**Genesis does NOT send notifications:**
```python
# genesis_arianna.py, genesis_monday.py
def send_to_session(digest: str):
    # File only, WITHOUT termux-notification
    trigger_file.write(digest)
```

**Field metrics remain:**
```python
# field/notifications.py
send_termux_notification(title, content, priority)
# Rate limited, emergency-aware
```

**Defender audits remain:**
```python
# defender_daemon.py
subprocess.run(['termux-notification', ...])
# Critical infrastructure alerts only
```

---

## 🎯 FINAL LOGIC:

- **Field = metrics only** (популяция, резонанс, emergency)
- **Defender = audits only** (security, infrastructure)
- **Genesis = silent** (files + GitHub, without notifications)
- **User reads Genesis via:** interactive session or GitHub

---

*Last updated: 2025-11-08*  
*Policy enforced after: Defender auto-removal incident*

