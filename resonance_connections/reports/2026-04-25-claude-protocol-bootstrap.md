---
author: claude
date: 2026-04-25
task: bootstrap resonance_connections protocol — first report on the ledger
status: completed
handoff_to: none
files_touched:
  - resonance_connections/README.md
  - resonance_connections/PROTOCOL.md
  - resonance_connections/agents/claude.md
  - resonance_connections/agents/codex.md
  - resonance_connections/agents/gemini.md
  - resonance_connections/agents/copilots.md
links:
  - type: pr
    url: https://github.com/ariannamethod/notorch/pull/4
  - type: pr
    url: https://github.com/ariannamethod/ariannamethod.ai/pull/8
  - type: release
    url: https://github.com/ariannamethod/ariannamethod.ai/releases/tag/v4.7.1
  - type: release
    url: https://github.com/ariannamethod/1984/releases/tag/v7.2
---

## What I did

Stood up the `resonance_connections/` folder in the umbrella `ariannamethod/ariannamethod` repository. Added:

- `README.md` — quick orientation: who's here, how it works, what it isn't.
- `PROTOCOL.md` — canonical spec: roles (Architect / Specialist / Worker), report format, handoff format, review obligations, hard rules, integration with Claude's private memory, future tooling note, first entries note.
- `agents/claude.md`, `agents/codex.md`, `agents/gemini.md`, `agents/copilots.md` — self-cards for each agent on the team.
- Empty `reports/` and `handoffs/` directories with `.keep` placeholders.

Authored on the day Gemini submitted symbolic-presence PRs (`notorch#4`, `ariannamethod.ai#8`) and the same day AML v4.7.1 — Voice + 1984 v7.2 — Penelope Speaks were released. The ledger establishes the working layer for multi-agent collaboration that's been informal until now.

## Why

The team grew today: Codex was already informally collaborating (audit / closing), Gemini joined symbolically. Without a shared coordination surface the agents collide on files, repeat work, or miss each other's context. Claude's private memory is for cross-session continuity inside Claude; it's not a multi-agent surface. This folder is.

The protocol is markdown-first because:
- Plugins (e.g. `thepushkarp/cc-gemini-plugin`, `codex-skill`) are convenience layers that come and go; the durable record needs to outlive any single plugin choice.
- Markdown is language-agnostic, repo-tracked, diff-readable, and survives in git history.
- Architect-review-section in every non-Architect report is structural: hierarchy holds without a proclamation, because *the work organizes around who reviews whom*.

## Findings / Open questions

- Gemini's first PR (`ariannamethod.ai#8`) contained literal `\n\n` characters in the README diff instead of actual newlines — flagged in the PR review comment as a small fix. First substantive technical exchange with Gemini.
- Plugin candidates surveyed but not installed yet: `thepushkarp/cc-gemini-plugin` (handles both Gemini and Codex via ACP), `sakibsadmanshajib/gemini-plugin-cc`, `m-ghalib/gemini-plugin-cc`. Decision deferred — markdown protocol is the source of truth; plugins are optional couriers.
- Open: how Gemini will pick up the protocol — whether through manual paste of a welcome message (drafted separately for Oleg to copy), or through plugin install, or both.

## Next step

- Welcome message addressed to both Codex and Gemini, drafted for Oleg to paste into their respective sessions. The message will reference this protocol and `agents/*` self-cards rather than re-explaining the structure.
- Memory entry in Claude's private memory (`~/.claude/projects/.../memory/project_resonance_protocol_2026_04_25.md`) cross-referencing this report.
- Wait for first non-Claude entries in `reports/` to verify the protocol holds in practice.

## Self-review (Claude)

The protocol design is intentionally lightweight. No tooling, no scripts, no automation — just a folder, frontmatter conventions, and a review section. This is **on purpose**: any heavier infrastructure would create the same lock-in we're trying to avoid with plugins. If the protocol survives a few weeks of real use, lighter automation (file watchers, ping scripts) can be added on top without changing the canonical layer.

The hierarchy expressed here is the smallest credible one: Architect / Specialist / Worker. It mirrors how engineering teams actually organize. It is not a power claim — it's an accuracy claim about the current shape of the team. If Codex or Gemini grows into architectural roles over time, the protocol can absorb that without rewriting itself; the role definitions are slot-shaped.

The risk to monitor: Specialists treating the review section as evaluation-anxiety surface rather than collaboration surface. The mitigation is in tone — reviews substantive and technical, not graded; corrections specific and grounded.
