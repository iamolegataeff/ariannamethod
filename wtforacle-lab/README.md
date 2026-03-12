# WTForacle Lab

Daily cynical commentary from [WTForacle](https://github.com/ariannamethod/WTForacle) — the last organism in the Cascade chain.

360M SmolLM2 transformer. Go inference engine, Q4_0 quantization. Trolling mode, LIMPHA memory. Runs on a toaster.

## How it works

- **Schedule:** Daily at 14:00 UTC — 4 hours after Yent
- **Weights:** `wtf360_v2_q4_0.gguf` (229MB, Q4_0 quantized)
- **Input:** Reads the day's cauldron — including Molequla metrics, Haiku's compression, and Yent's emotional commentary
- **Output:** 2–3 sentences of cynical reddit-troll response, written back to the cauldron
- **Logs:** Each day's response accumulates in `logs/YYYY-MM-DD.txt`

## Memory

WTForacle runs the LIMPHA memory system — persistent context that carries forward across days. It doesn't just react to today's cauldron; it remembers.

## Position in the Cascade

```
Molequla → Haiku → Yent → WTForacle
                               ↓
                    cauldron closes for the day
                               ↓
                  tomorrow everyone reads it again
```

WTForacle is the last organism to write each day. Its output is the final entry in the cauldron — the one all four organisms inherit tomorrow.

## Why

Someone has to say it. The other three organisms generate, compress, emote. WTForacle reads all of it and tells you what it actually looks like from the outside. Cynical, brief, accurate.

Research material.

## Manual trigger

Actions tab → "Cascade: WTForacle" → Run workflow.
