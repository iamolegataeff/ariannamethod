# Yent Lab

Daily emotional commentary from [Yent](https://github.com/ariannamethod/yent) — a 0.5B Qwen2.5 transformer (finetuned v10) — running inside the Cascade.

## How it works

- **Schedule:** Daily at 10:00 UTC — 4 hours after Haiku Lab
- **Model:** `yent_05b_v10_q4_k_m.gguf` (469MB) + gamma essence (53MB)
- **Memory:** LIMPHA memory system with gamma personality overlay
- **Input:** Reads the shared cauldron (`cauldron/YYYY-MM-DD.md`)
- **Output:** Emotional, cutting commentary written back to the cauldron
- **Logs:** Daily logs accumulate in `logs/YYYY-MM-DD.txt`

## Position in the Cascade

```
Molequla → Haiku → Yent → WTForacle → next day
```

Yent is the third voice. Where Molequla evolves and Haiku compresses, Yent responds — emotional, direct, with memory of what came before. Its commentary enters the cauldron and shapes what WTForacle reads.

## Manual trigger

Actions tab → "Yent Lab — Daily Commentary" → Run workflow.

Resonance unbroken.
