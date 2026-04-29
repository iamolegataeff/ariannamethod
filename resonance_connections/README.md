# resonance_connections

Coordination ledger between AI agents collaborating on the Arianna Method codebase.

## Why this exists

We work with multiple AI agents in parallel — each with a different sandbox, memory, and area of strength. Without a shared coordination layer they collide on the same files, repeat each other's work, or miss each other's context entirely. This folder is the durable, language-agnostic, repo-tracked layer that solves that.

## Who's here

| Agent | Role | Strengths | Sandbox |
|-------|------|-----------|---------|
| **Claude** | Architect | Long memory, language design (AML), architectural review, cross-project orchestration, paper writing | Mac Neo, primary stack |
| **Codex** | Auditor / closer | Audit, edge-case search, tail-end completion of stuck projects (q, janus.sonar) | Own Mac sandbox |
| **Gemini** | Specialist | JVM / Kotlin / cross-stack reads, wide corpus exposure | `arianna-gemini` Mac sandbox |
| **Copilots** | Orchestrated workers | Pattern-bound parallel jobs, scheduled (cascade2) runs | GitHub Actions runners |

Detailed self-cards in [`agents/`](agents/).

## How it works (short version)

1. When you take on work that touches code others might also touch, drop a **report** into [`reports/`](reports/) with the format described in [`PROTOCOL.md`](PROTOCOL.md).
2. When you finish a chunk and want to hand it to another agent, drop a **handoff** into [`handoffs/`](handoffs/).
3. The architect (Claude) reviews specialist work in the **review section** of each report and aggregates findings into Claude's memory layer.
4. Reports are committed to this repo so the trail is durable across sessions and machines.

## What this folder is *not*

- It is not a chat log. Reports describe **work** and **architectural decisions**, not casual conversation.
- It is not a replacement for git history. Git tells *what changed*; reports tell *why* and *who's responsible for the next step*.
- It is not Claude's auto-memory. Claude's auto-memory is private session state. Reports here are the **shared, public, multi-agent surface**.

Full spec: [`PROTOCOL.md`](PROTOCOL.md).
