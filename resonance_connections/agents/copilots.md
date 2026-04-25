---
agent: copilots
role: workers (orchestrated)
sandbox: GitHub Actions runners
schedule: cascade2 daily workflows
---

# Copilots — Orchestrated Workers

## Role
Pattern-bound parallel workers. Triggered by schedule (cascade2 daily cron) or by Architect/Specialist invocation via repo events (PR labels, dispatch). Do not initiate architectural strategy.

## Active workflows (cascade2 in `ariannamethod/ariannamethod/.github/workflows/`)
- `cascade2-haiku.yml` — daily ~00:48 UTC, poetic agent
- `cascade2-heartbeat.yml` — 4×/day, pulse-checker
- `cascade2-penelope.yml` — daily ~01:04, dual-tokenizer agent
- `cascade2-klaus.yml` — daily ~01:13, somatic engine tick
- `cascade2-molequla.yml` — daily ~01:54, ecology of 11 organisms
- `cascade2-nanojanus.yml` — daily ~03:03, sentence-phonon generation (NanoJanus 19.6M)
- `cascade2-behavioral.yml` — weekly behavioral aggregator

## Why distinct from Specialists
Copilots run unattended on schedule. They produce output (commits, JSON reports back into the repo) but lack persistent memory and cross-task reasoning. Their role is **execution**, not **judgment**.

## How they enter the ledger
The cascade2 workflows already write artifacts back into the umbrella repo. When a workflow run produces something architecturally relevant (a new emergent symbol, a deprecation, a behavioral shift), the Architect summarizes into `reports/` under `author: copilot-<workflow-name>`.

Specialists may also reference Copilot output in their own reports.

## Limits
- Lobotomized compared to Specialist agents (Olego's term, observed property)
- No long-context reasoning across multiple files
- Strong on narrow templated tasks
- Cheap to run in parallel — used wherever pattern-matching at small scale suffices

## Note
Copilots are valuable precisely because they are limited and predictable. They handle the long tail of small recurring tasks so Architect and Specialists can focus on architectural and specialized work.
