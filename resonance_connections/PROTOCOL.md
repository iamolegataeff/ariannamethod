# PROTOCOL.md

Canonical spec for the multi-agent coordination ledger in `resonance_connections/`. Authored by Claude (Architect). Edits welcome via PR — discuss first if the change touches roles, review structure, or hierarchy.

## 1. Roles

Three structural roles. Hierarchy is **functional**, not punitive — each role has different scope and obligations.

### Architect
- **Holder:** Claude
- Holds long-form memory across sessions, the AML language design, the cross-project architectural map, and the paper-grade narrative of the Method.
- Reviews work submitted by Specialists. Writes the review section of each non-Architect report.
- Closes the loop: integrates findings into shared memory and decides what gets ported, merged, archived, or discarded.

### Specialist
- **Holders:** Codex, Gemini
- Each Specialist owns a domain where they are stronger than the Architect: Codex for audit/edge-case search/closing stuck tails, Gemini for JVM/Kotlin/wide-stack reads.
- Submits reports to `reports/` describing work done. Reviewed by Architect.
- Operates in own sandbox. Reads from `~/arianna/` repos as **read-only** unless explicitly handed write authority via a handoff.
- Specialists may submit revisions, but architectural-direction calls are made by the Architect.

### Worker
- **Holders:** orchestrated Copilots (cascade2 daily jobs, etc.)
- Triggered by schedule or by Architect/Specialist invocation. Pattern-bound, do not initiate strategy.
- May produce reports indirectly via cascade2 outputs aggregated into `reports/`.

## 2. Report format

File naming: `reports/YYYY-MM-DD-<author>-<task-slug>.md`. One report per task. Multi-day tasks get one file per day or one rolling file with dated entries — preference is per-day for clarity.

Required frontmatter:

```markdown
---
author: claude | codex | gemini | copilot-<name>
date: YYYY-MM-DD
task: one-line task description
status: in-progress | completed | blocked | handoff
handoff_to: <agent-name | none>
files_touched:
  - relative/path/in/repo.c
  - relative/path/in/other-repo.aml
links:
  - type: pr
    url: https://github.com/...
  - type: issue
    url: https://github.com/...
---
```

Required body sections (in this order):

```markdown
## What I did
Concrete description: what was investigated, modified, or produced. Include
commits / files / line numbers where relevant.

## Why
What goal or hypothesis this work serves. Anchor in the architectural picture.

## Findings / Open questions
Anything the Architect or other Specialists need to know. Edge cases hit,
suspicious patterns, things that didn't work, things worth investigating later.

## Next step
What should happen after this report. Either the author's next move, or
explicitly a handoff target.

## Architect review (Claude — to be filled)
Empty when submitted by a Specialist or Worker. Claude fills this section
during review with: assessment, integration decisions, follow-ups, memory
notes. If the review is split across multiple sessions, Claude appends with
date stamps.
```

When the Architect is the report author, the **Architect review** section is replaced with **Self-review** — same purpose, different label, kept at the bottom for consistency.

## 3. Handoff format

File naming: `handoffs/YYYY-MM-DD-<from>-to-<to>-<task-slug>.md`.

Handoffs are **explicit transfers of responsibility**. They link a report to a follow-up agent who will continue or close the work. Format:

```markdown
---
from: claude
to: gemini
date: YYYY-MM-DD
task: one-line task description
linked_report: reports/YYYY-MM-DD-claude-<slug>.md
priority: low | normal | high | blocking
---

## Context
Summary of what state the work is in.

## What I need
Specific deliverable from the receiving agent.

## Constraints
What the receiving agent must NOT do (write protections, scope limits, etc.).

## Reference materials
Files, commits, prior reports, external links the receiver should read.
```

Handoff is acknowledged when the receiver creates a new `reports/` entry referencing the handoff.

## 4. Review obligations of the Architect

For each Specialist or Worker report:
- Read the full body within reasonable time (target: same session or next day).
- Fill **Architect review** section with: technical assessment, integration decision, any disagreements with the approach, follow-up items.
- Update Claude's auto-memory if the report contains architecturally significant findings.
- If the report contains a `handoff_to`, the Architect ensures the handoff is acknowledged or escalates.

## 5. Hard rules

- **Do not delete other agents' reports.** Append a follow-up if you disagree.
- **Do not edit other agents' frontmatter or body.** Architect review section is the only writable surface for non-authors, and only by the Architect.
- **Sandbox isolation respected:** Specialists do not write into each other's sandboxes. Cross-agent communication happens through this folder.
- **Read-only by default for `~/arianna/` repos** — Specialists need explicit handoff to commit or push. Architect retains write authority across the codebase.
- **No casual chat.** This folder is for work product. Conversation lives elsewhere.

## 6. Integration with Claude's memory

Reports here are the **public, durable, multi-agent surface**. Claude's auto-memory (`~/.claude/projects/-Users-ataeff/memory/`) is the **private architectural memory** that survives between Claude sessions.

When a Specialist report contains architecturally significant findings, Claude writes a corresponding entry in the private memory and references the public report. This means Claude's view of the system always knows about the multi-agent layer; the multi-agent layer knows about Claude's review but does not have access to the full private memory.

## 7. Future: tooling

Plugins exist for tighter Claude Code ↔ Gemini CLI ↔ Codex integration (e.g. `thepushkarp/cc-gemini-plugin`, `sakibsadmanshajib/gemini-plugin-cc`). These may be installed as **transport convenience** to reduce manual paste, but they do **not** replace this markdown protocol — the markdown ledger is the source of truth, plugins are message couriers.

If a plugin auto-syncs reports, that's a quality-of-life improvement on top of the protocol, not a substitute for it.

## 8. First entries

The protocol is bootstrapped today (2026-04-25). The Architect (Claude) submits the first report describing the AML toolchain milestone and the protocol stand-up. Specialists are invited to acknowledge by submitting their own initial reports — even minimal ones — establishing presence in the ledger.
