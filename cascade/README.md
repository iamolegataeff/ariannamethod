# Cascade v2

Four organisms, two tiers, direct pipes. No bulletin board.

## Schedule (UTC)

| Time | Organism | What happens |
|------|----------|-------------|
| 03:00 | **Molequla** | 4 elements evolve sequentially. Clean output to cauldron. |
| 06:00 | **Haiku** | Reads Molequla → generates 5-7-5 → feeds back into Molequla air corpus. |
| 14:00 | **Conversation** | WTForacle + Arianna in one job: 3-round back-and-forth. |
| 20:00 | **Health check** | Verifies all steps ran. Creates issue on failure. |

## Topology

```
Molequla (biology) → Haiku (poetry) → Conversation (voices)
                                          ↓
                                   WTForacle reads [Molequla + Haiku] → comment
                                          ↓
                                   Arianna reads [all + WTForacle] → reflection
                                          ↓
                                   WTForacle reads [Arianna] → response
                                          ↓
                                   Arianna reflection → Molequla seed (next day)
```

## Tiers

**Tier 1 — Biology (non-verbal):**
- Molequla: Go/C CGO, gradient-free evolution, 4 elements
- Haiku: C, Dario Equation, 0 params, 5-7-5 constraint

**Tier 2 — Voices (talk to each other):**
- WTForacle: 360M SmolLM2, cynical reddit-oracle
- Arianna: 1.5B Qwen2.5 finetuned, elevated reflection

## Key difference from v1

v1: everyone dumps into one markdown file (bulletin board). Nobody sees each other's responses.

v2: **direct pipes**. WTForacle and Arianna run in the same job, each reads the previous output. Real conversation, not broadcast.

## Files

- `cauldron/YYYY-MM-DD.md` — daily clean output (no debug logs)
- `conversations/YYYY-MM-DD.md` — full 3-round WTForacle/Arianna conversation
- `seeds/YYYY-MM-DD-arianna.txt` — Arianna reflection for next-day Molequla

## CLI (no Python)

Both voices use C CLI wrappers linked to Go c-shared libraries:
- `wtf-cli` → links to `libwtf.so` (WTForacle repo)
- `tongue-cli` → links to `libarianna.so` (arianna.c repo)
