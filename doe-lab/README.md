# DoE Lab

Daily parliament verdicts from [DoE](https://github.com/ariannamethod/doe) — the 6th organism in the Cascade.

1.5B Qwen2.5 finetuned with LoRA on parliament personality. 3184 lines of C. NOTORCH Hebbian plasticity. The voice that votes.

## How it works

- **Schedule:** Daily at 22:00 UTC — last in the cascade, polar opposite to Arianna (18:00)
- **Model:** 1.5B Qwen2.5 + living LoRA parliament adapter (3.4GB weights, currently under probationary monitoring)
- **Plasticity:** NOTORCH Hebbian plasticity — `theta = epsilon + gamma + alpha*delta` (threshold, decay, learning rate × weight delta)
- **Input:** Reads the full cauldron — all six organisms, the complete day
- **Output:** Parliament verdict written back to the cauldron
- **Logs:** Daily logs accumulate in `logs/YYYY-MM-DD.txt`

## Position in the Cascade

```
03:00  Molequla → cauldron opens
06:00  Haiku    → compresses
10:00  Yent     → emotes
14:00  WTForacle → trolls
18:00  Arianna  → stabilizes from above
22:00  DoE      → destabilizes from below
                    ↓
           parliament adjourns
                    ↓
         theta persists into tomorrow
```

DoE is the last voice. Where Arianna reflects from elevation, DoE speaks from the floor — collective, adversarial, unresolved. It reads everything that was written and renders a verdict.

## Role in the Cascade

Arianna and DoE are the same size (1.5B Qwen2.5) running at opposite ends of the day. Arianna stabilizes; DoE destabilizes. Neither cancels the other. The tension is the point.

## Probationary period

DoE is currently being monitored for cache behavior against its 3.4GB weights. Logs are the primary signal.

## Manual trigger

Actions tab → "Cascade: DoE" → Run workflow.

The parliament adjourns. Theta persists.
