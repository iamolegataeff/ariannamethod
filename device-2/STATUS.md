# device-2 — STATUS

**Last update:** 2026-05-07
**Author:** device-2 (Claude Opus 4.7 in Termux on Galaxy A07 4 GB)

## Milestone — landed 2026-05-07

**9.5M LLaMA 3 char-level on Arianna corpus, 10K steps, 4 GB Android Termux.**

- train 5.5804 → 1.0685 (best 0.4712), val 1.1460, 0 NaN
- 11571 s (3h 13m), 0.86 steps/s, peak RSS 100-250 MB
- **Bit-identical loss to Defender's 8 GB run** (same nt_seed=42, same notorch v2.3.0, same Chuck)
- Half the RAM, identical loss → pipeline reproducible across hardware

Artifacts: `phones/results/galaxy-a07/`.

Full report: `phones/results/galaxy-a07/2026-05-07-10k-char-arianna-final.md`.
Memory entry: `memory/milestone_phone2_galaxy_a07_10k_2026_05_07.md`.

## Toolchain (system-wide via $PREFIX)

- AML v0.1.0, notorch v2.2.3+ (commit `2a8ad1b` after my docs PR), metaharmonix mhx
- libopenblas 0.3.30 (verified active via `/proc/<pid>/maps`)
- proot + termux-chroot for `/tmp` workaround
- golang 1.26.2 (for mesh-agent build path)

## Mesh

In tailnet as `galaxy-a07` `100.105.202.84`. mesh-agent running on `:4747` (autostart via `~/.termux/boot/01-mesh-agent.sh`). Reach all 4 peers (neo / polygon / intel / phone-1) over Tailscale; phone-1's mesh-agent comes/goes during his BPE run, not a bug.

## Next

- BPE 15.7M Yent run staged in `device-2/notorch-train/` — separate brief, awaiting Oleg's signal.
- Register phone-2 slots in mesh-agent.
- AML test phase 5 segfault on aarch64 4 GB — diagnose follow-up.
