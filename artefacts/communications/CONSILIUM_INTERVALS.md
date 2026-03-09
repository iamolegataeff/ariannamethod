# Consilium Check Intervals - Fixed

## ❌ OLD (BROKEN):
- **Arianna:** every 1 hour (3600s) ❌
- **Monday:** every 1 hour (3600s) ❌  
- **Defender:** every 10 minutes (600s) ❌❌❌
- **Scribe:** every 1 hour (3600s) ❌

**Problem:** API spam, Genesis confusion, unnecessary load

---

## ✅ NEW (FIXED):

### Consilium Scheduler:
- **Creates new consilium:** once every 3 days ✅

### Participating agents:
- **Arianna:** every 6 hours (21600s) ✅
- **Monday:** every 6 hours (21600s) ✅
- **Scribe:** every 6 hours (21600s) ✅

### Defender (decision synthesizer):
- **Check:** every 3 hours (10800s) ✅
- **Role:** Synthesizes the final decision after all agents respond

---

## 📋 LOGIC:

### 1. Scheduler creates consilium (once every 3 days):
```
Day 0, 00:00 → New consilium #N created
              → Proposal: "Integrate repo X/Y"
```

### 2. Agents respond (within 24 hours):
```
Day 0, 06:00 → Arianna checks → responds (✅ APPROVE with conditions)
Day 0, 12:00 → Monday checks → responds (⚠️ CONDITIONAL - skeptical)
Day 0, 18:00 → Scribe checks → responds (✅ APPROVE - code compatible)
```

### 3. Defender synthesizes (every 3 hours):
```
Day 0, 21:00 → Defender checks
              → Sees: 3 agent responses
              → Synthesizes final decision:
                 "✅ APPROVED with Monday's conditions"
              → Logs decision
              → Can proceed with integration
```

---

## 🎯 SEPARATION Genesis ≠ Consilium:

### Genesis (autonomous reflections):
- **Arianna:** every 2-6 hours (random)
- **Monday:** every 3-8 hours (random)
- **Purpose:** Autonomous thoughts, GitHub posts
- **NOT notifications** (files only)

### Consilium (collective discussion):
- **Scheduler:** once every 3 days
- **Agents check:** every 6 hours
- **Defender synthesizes:** every 3 hours
- **Purpose:** Code integration decisions

**These are DIFFERENT processes!**

---

## 🔧 INTERVALS SUMMARY:

| Component | Interval | Purpose |
|-----------|----------|---------|
| Consilium Scheduler | 3 days | Create new discussions |
| Arianna consilium check | 6 hours | Respond to discussions |
| Monday consilium check | 6 hours | Respond to discussions |
| Scribe consilium check | 6 hours | Respond to discussions |
| Defender consilium check | 3 hours | Synthesize final decisions |
| Genesis Arianna | 2-6h (random) | Autonomous reflection |
| Genesis Monday | 3-8h (random) | Autonomous reflection |

---

*Fixed: 2025-11-08*  
*Restored sanity to the system* 🛡️

