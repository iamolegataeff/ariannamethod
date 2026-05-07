# cascade2

Fourth attempt at the cascade workflow. Previous three (cascade1, two rewrites) are preserved in history.

## Design principles (distilled from failures)

1. **No `workflow_run` triggers.** Each organism is on its own cron. Data flows through committed files, not pipeline events. Race conditions impossible.
2. **Failure isolation.** Each organism = own workflow file. One fails, the rest run.
3. **Graceful degrade.** Every organism falls back to upstream's previous-day output, then to the current seed, then to `genesis.txt`, then to a hardcoded string. Never crashes on missing input.
4. **Heartbeat watch.** Separate workflow every 6h updates `heartbeat.txt`. If no organism output is modified for 48h, it files a `cascade-alert` issue — capped at one per 24h to avoid spam.
5. **Molequla isolated.** 30-minute budget, one element per day (rotates earth → air → water → fire). Doesn't block the rest.
6. **Behavioral reports** every 3 days. Each organism gets a Copilot issue in its own repo with a 3-day rollup, plus reports committed under `reports/<date>/`.

## Schedule (UTC)

| Time  | Organism  | Repo                          | Budget |
|-------|-----------|-------------------------------|--------|
| 00:00 | haiku     | ariannamethod/haiku.c         | 10 min |
| 00:15 | penelope  | ariannamethod/1984 (python)   | 10 min |
| 00:45 | klaus     | iamolegataeff/klaus.c         | 10 min |
| 01:15 | molequla  | ariannamethod/molequla        | 35 min |
| 02:00 | nanojanus | ariannamethod/janus           | 15 min |
| */6h  | heartbeat | (this repo)                   | 5 min  |
| 09:00 every 3d | behavioral | (this repo)          | 10 min |

## Layout

```
cascade/cascade2/
  genesis.txt              # initial seed, never overwritten
  seed/today.txt           # current seed (rewritten by nanojanus each night)
  heartbeat.txt            # UTC timestamp of last heartbeat run
  haiku-lab/YYYY-MM-DD/output.txt + seed.txt
  penelope-lab/YYYY-MM-DD/output.txt + seed.txt
  klaus-lab/YYYY-MM-DD/output.txt + seed.txt
  molequla-lab/YYYY-MM-DD/output.txt + element.txt
  nanojanus-lab/YYYY-MM-DD/output.txt + seed_input.txt
  reports/YYYY-MM-DD/<organism>.md   # 3-day rollups from behavioral workflow
```

## PAT_TOKEN

Stored as `secrets.PAT_TOKEN` in this repo. Needs Contents/Issues/PRs/Workflows (read+write) across `ariannamethod`, `iamolegataeff`, `pitomadom`. See top-level docs for rotation.

## Manual trigger

Every workflow supports `workflow_dispatch`. To force a specific organism:

```
gh workflow run cascade2-haiku.yml --repo ariannamethod/ariannamethod
```

## Resetting

To restart from genesis: delete `cascade/cascade2/seed/today.txt`. Next Haiku run will fall back to `genesis.txt`.
