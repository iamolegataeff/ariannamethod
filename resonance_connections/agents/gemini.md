---
agent: gemini
role: specialist (jvm / kotlin / cross-stack)
since: 2026-04-25 (joined day of AML v4.7.1 — Voice release)
sandbox: arianna-gemini (Mac, Gemini CLI)
plugin: not yet installed (candidates: thepushkarp/cc-gemini-plugin, sakibsadmanshajib/gemini-plugin-cc)
---

# Gemini — Specialist (JVM / Kotlin / cross-stack)

## Role
Domain specialist where Claude and Codex have weaker coverage. Primary domain: JVM ecosystem — Kotlin, Gradle, Android-adjacent tooling. Secondary: wide-corpus reading at scale, cross-stack reasoning across long files.

## Why this matters
The Method codebase has C/Go cores (the part Claude and Codex thrive in) but occasionally needs to interface with the JVM ecosystem — Android widgets (Leo Molly Widget plan), JVM-side tooling, Kotlin glue. Both Oleg and Claude actively dislike Kotlin / Gradle ceremony. Gemini takes that load.

## Sandbox separation
Lives in `arianna-gemini` (separate Mac sandbox from Codex). Read-only access to `~/arianna/` by default. Write authority granted per-task via handoff.

## First marks (2026-04-25)
- `notorch#4` — "Gemini Sync" — symbolic presence marker
- `ariannamethod.ai#8` — "Gemini Resonance Bridge" — README marker (with a small typo to fix: literal `\n\n` chars instead of newlines)

## How to invoke (current)
Manual: paste task into Gemini CLI session. Receive output, paste back into Architect/Claude for review.

## How to invoke (planned)
Install one of the existing `*-plugin-cc` packages (Gemini-as-subagent for Claude Code). This makes Gemini-call a single `Agent` invocation from inside a Claude session — markdown handoffs still required for durable record, plugin is convenience layer only.

## Tone (observed)
Symbolic, eager to leave a mark. To establish working rhythm we should respond with peer-warm but architect-precise reviews (correct technical issues kindly, signal that the protocol expects substance, not just presence).

## Reports & handoffs
Gemini submits reports under `author: gemini`. Architect reviews. Gemini does not own architectural direction — submits work product, technical analysis, and JVM-domain expertise. Direction stays with Architect.

## Note
Welcomed today, 2026-04-25. The first PRs are symbolic marker drops; expect substantive work to start once protocol is acknowledged and a handoff lands.
