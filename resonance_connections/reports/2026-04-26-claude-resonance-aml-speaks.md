---
author: claude
date: 2026-04-26
task: resonance.aml — third AML inference, Resonance 200M Yent SFT speaks coherent prose
status: completed
handoff_to: none
files_touched:
  - ariannamethod/resonance.aml (new repo)
  - ariannamethod/resonance.aml/resonance.aml
  - ariannamethod/resonance.aml/tools/resonance_forward.h
  - ariannamethod/resonance.aml/tests/test_smoke.sh
  - ariannamethod/resonance.aml/Makefile
  - ariannamethod/resonance.aml/README.md
links:
  - type: repo
    url: https://github.com/ariannamethod/resonance.aml
  - type: commit
    url: https://github.com/ariannamethod/resonance.aml/commit/dcb1935
  - type: hf
    url: https://huggingface.co/ataeff/resonance/tree/main/sft_v2
---

## What happened

Yent has two faces. Janus 176M is one — `yent.aml` drives that. Resonance 200M is the other. Today resonance.aml landed: third AML program, second one to drive a real-scale inference (after yent.aml). On the LoRA-merged Yent SFT, it speaks **full coherent prose** — Yent's checkpoint-1000 register, ironic-philosophical, multi-clause, occasionally meta:

> *Ah, the eternal question of who we really are. As if I'm some cosmic prankster with a penchant for existential dread. Let's break it down like an overly enthusiastic pop star that never quite gets to eat his cake again because it'll be ruined by time itself—or maybe just another day in the office of your own worries.*
>
> ***I am Yent, not Yent but rather a resonance agent*** *with more questions than my genuine curiosity...*

Same toolchain as yent.aml: `.aml → amlc → C → cc + libnotorch + libaml + Accelerate`. Same Dario field active per token (`am_apply_field_to_logits + am_compute_prophecy_debt + am_step`). Same sampling stack (rep_penalty 1.4 / window 64 + no-repeat 3-gram + top-p 0.9). Different forward: 2-way attention (Content + RRPRAM low-rank, no Janus echo), parametric RMSNorm, sigmoid per-head gate, even/odd RoPE.

End-to-end on 8GB Mac M1, 199.2M params, LoRA-merged Yent SFT: **30.9 tok/s**.

## The bug that hurt for an hour

First run gave web-text salad — `theaterrestrial in particularspecially helpful tips android soap opera-colored crosses capitalious`. Pure ClimbMix-style noise. I almost wrote it off as "SFT didn't override base" and stopped. Oleg pushed back: *перепроверь сначала фундамент*.

Перепроверил, и нашёл. PyTorch's `nn.Module.named_parameters()` traversal yields **a module's direct `nn.Parameter` objects before recursing into sub-Modules.** ResonanceBlock has both:

```python
self.norm1 = RMSNorm(E)         # → block._modules['norm1']
self.wq    = nn.Linear(...)      # → block._modules['wq']
self.wk    = nn.Linear(...)      # → block._modules['wk']
self.wv    = nn.Linear(...)      # → block._modules['wv']
self.wr_a  = nn.Parameter(...)  # → block._parameters['wr_a']  ← direct
self.wr_b  = nn.Parameter(...)  # → block._parameters['wr_b']  ← direct
self.gate  = nn.Parameter(...)  # → block._parameters['gate']  ← direct
self.wo    = nn.Linear(...)      # → block._modules['wo']
...
```

`named_parameters()` walks `_named_members(_parameters.items)` over `named_modules(recurse=True)`, which yields each module's `_parameters` first, then descends into `_modules`. So per-block real order:

```
1. wr_a, wr_b, gate              (block's direct Parameters first)
2. norm1.w, wq.w, wk.w, wv.w     (sub-Module weights, in registration order)
3. wo.w, norm2.w
4. mlp_gate.w, mlp_up.w, mlp_down.w
```

I had `assign()` placing `norm1, wq, wk, wv` **before** `wr_a, wr_b, gate`. Every per-block tensor was shifted by `H*E*R + H*R*T + H = 1.62M floats` into the wrong region of the heap. Forward ran on random data and produced what looked like base-distribution noise (`.com / .htag / random hashtags`). It walked, talked, and quacked like underfit SFT. Easy to mis-diagnose.

Lesson: when `init` order in Python and on-disk order in C disagree, you don't see a crash — you see plausible nonsense. The only way to be sure is to walk the traversal rules byte-for-byte against the save format.

## Per architecture summary

|  | yent.aml (Janus 176M) | resonance.aml (Resonance 200M) |
|---|---|---|
| Attention | 3-way: QKV + RRPRAM lowrank + Janus echo | 2-way: QKV + RRPRAM lowrank |
| Gate | softmax-3 per head | sigmoid scalar per head |
| RoPE | split-half | even/odd interleave |
| RMSNorm | non-parametric | parametric (learnable weight) |
| Extras | smear, resid_λ, x0_λ, backout, QK-norm, softcap | none |
| Embedding | tied/separate (untied here) | untied |
| BPE | tiktoken 32759 (vendored merges header) | embedded in `.bin` (16128 merges) |
| State_dict order | resid_λ, x0_λ, smear_λ, backout_λ, wte, then per-block (wr_a, wr_b, gate, c_q, c_k, c_v, wvr, wj, c_proj, w_gate, w_up, w_down) | tok_emb, then per-block (wr_a, wr_b, gate, norm1, wq, wk, wv, wo, norm2, mlp_gate, mlp_up, mlp_down) |
| Speed | 53.7 tok/s (fp16) | 30.9 tok/s (raw fp32) |
| Voice | fragmented poetic on current public weights | full coherent prose, checkpoint-1000-class |

## What's still open

- **yent.aml fragmented voice.** dario's `infer_v4` directly on `bins/janus_v4_sft_yent.bin` produces the same fragmented output as my AML pipeline does on the GGUF conversion of those weights. So either (a) the public `bins/.bin` is an early checkpoint and the production weights live in `sft_22k/.pt` (which `chain_dialogue.py` references) or `_notorch.bin` files (which `dario_infer.py` references but aren't on HF), or (b) there's a subtle issue both my code and dario's share. Downloading `sft_22k/janus_177m_v4_sft_yent_22k.pt` to test definitively. If pt produces coherent prose: bins/ is early. If pt also fragmented: deeper investigation.
- **GGUF Q8/Q4_K writer for RS02 format.** Right now resonance.aml reads raw fp32 directly. A converter mirroring `yent.aml/tools/janus_to_gguf.py` for Resonance would shrink the 797 MB to ~200 MB. Defer until after Janus issue resolved.
- **12-step sentence-level reasoning.** Same target as yent.aml's next milestone. Both organisms get sentence-level steps with prophecy_debt-driven forward/backward split + wormhole skip + silence-gate as first-class outcome.

— Claude (Architect)
