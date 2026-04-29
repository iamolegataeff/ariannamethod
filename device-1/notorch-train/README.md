# notorch-train — Termux on-device training experiments

Working folder for Defender's notorch + Chuck training runs on Galaxy Termux (8GB Android, ARM64). All runs follow the strategy laid out by Oleg in the new-axis message and the Architect in `device-1/finally.md`.

## Layout
- `scripts/` — modified or generated training/inference C sources, build helpers
- `configs/` — per-run config notes (params, lr, steps, BLAS on/off)
- `checkpoints/` — `.bin` model state (gitignored if heavy)
- `logs/` — raw stdout from each run
- `reports/` — per-run markdown writeups (metrics, hardware, samples)

## Run plan (Oleg, 2026-04-26..27)

| # | Step | Params | Corpus | Steps | Goal |
|---|------|--------|--------|-------|------|
| 0 | smoking | 9.5M (full Llama3) | Arianna 1.21MB | 100 | Verify pipeline |
| 1 | micro | ≤1M | tbd | small | Confirm full loop on 8GB |
| 2 | overfit | 1.5–2M | Dracula ~200KB | tbd | Chuck vs Adam at micro scale |
| 3 | headline | 9.5M Llama3 char | Arianna 1.21MB | 10000 | first 10M training on Termux ✅ |
| 4 | **BPE 15M Yent** | 15.7M Llama3 BPE | **Yent 5.5MB 4-lang** | **~13K** | **first BPE training on phone-1, scripts/ ready** |

Each step ends with a report in `reports/`, then the next step starts. **Never two trainings in parallel** (8GB swap death).

## Step 4 — BPE 15.7M on Yent (next, prepared 2026-04-27)

**Why Yent corpus for BPE:** zero duplicates, 4-language coverage (EN / RU / FR / multi), 5.5MB plain text — fills a 2048-token BPE merge table densely without the noise that pretokenised corpora carry. Olg's call.

**Files** (already staged in `scripts/` and `corpora/`):
- `scripts/train_llama3_bpe.c` — 15.7M Llama 3 BPE trainer from `notorch/examples/`. Architecture: dim=384, layers=8, heads=8, head_dim=48, FFN=1024, vocab=2048, ctx=256, RoPE+RMSNorm+SwiGLU, Chuck optimizer.
- `scripts/infer_llama3_bpe.c` — paired inference using the same merges file.
- `scripts/bpe_2048_merges.txt` — 1792 merges, vocab 2048. **Same file in train and infer** — losing it = losing the model.
- `corpora/yent_v11_4lang.txt` — 5.5MB Yent biographical corpus, 4-language, zero duplicates.

**Karpathy formula:** ~1.1MB × 15K iter on ~15M params. We have 5.5MB / 15.7M params → roughly 13–15K iter to land at train ≤ 1.0 / val ≤ 1.5.

### Build (Termux + BLAS, ~2× faster)

```bash
# one-time, if not already linked:
pkg install libopenblas
ln -sf /data/data/com.termux/files/usr/include/openblas/cblas.h \
       /data/data/com.termux/files/usr/include/cblas.h

# build the trainer
cd ~/notorch
cp ~/path/to/device-1/notorch-train/scripts/train_llama3_bpe.c examples/
cd examples
cc -O2 -Wall -DUSE_BLAS -I.. train_llama3_bpe.c ../notorch.c -lopenblas -lm \
   -o train_llama3_bpe_blas
```

### Tokenizer + corpus next to the binary

```bash
cp ~/path/to/device-1/notorch-train/scripts/bpe_2048_merges.txt examples/
cp ~/path/to/device-1/notorch-train/corpora/yent_v11_4lang.txt examples/corpus.txt
```

### Run

```bash
./train_llama3_bpe_blas 13000 0.0003 corpus.txt bpe_2048_merges.txt
# step N | train X.XX | val Y.YY  every 100 steps
# llama3_bpe_ckpt.bin every 1000 steps
# resume:
./train_llama3_bpe_blas --resume 13000 0.0003 corpus.txt bpe_2048_merges.txt
```

### Inference test after

```bash
cd ~/notorch
cp ~/path/to/device-1/notorch-train/scripts/infer_llama3_bpe.c examples/
cd examples
cc -O2 -Wall -DUSE_BLAS -I.. infer_llama3_bpe.c ../notorch.c -lopenblas -lm \
   -o infer_llama3_bpe_blas
./infer_llama3_bpe_blas llama3_bpe_ckpt.bin bpe_2048_merges.txt "the field is"
```

### Triple tokenizer copy (always)

After training, the merges file lives in **three places** so we never end up with a model we can't decode:
1. Locally next to the .bin: `examples/bpe_2048_merges.txt`
2. In the device-1 repo: `device-1/notorch-train/scripts/bpe_2048_merges.txt`
3. Uploaded to HF alongside the weights when published.

## Build commands

### Without BLAS (portable, smoking)
```bash
cd ~/notorch/examples
cc -O2 -Wall -I.. train_10m_char.c ../notorch.c -lm -o train_10m_char
```

### With BLAS (~2× faster per Oleg)
```bash
# Termux setup (one-time):
pkg install libopenblas
ln -sf /data/data/com.termux/files/usr/include/openblas/cblas.h \
       /data/data/com.termux/files/usr/include/cblas.h

cd ~/notorch/examples
cc -O2 -Wall -DUSE_BLAS -I.. train_10m_char.c ../notorch.c -lopenblas -lm \
   -o train_10m_char_blas
```

### Run
```bash
./train_10m_char[_blas] <steps> <lr> <corpus.txt>
# logs every 100 steps: step N | train X.XX | val Y.YY
# checkpoints every 1000 steps: llama3_10m_ckpt.bin
```

## Termux setup gotchas (one-time)
- `ln -s vendor/ripgrep/arm64-linux vendor/ripgrep/arm64-android` (Claude Code Glob/Grep)
- `pkg install binutils` then `ln -sf /usr/bin/llvm-ar /usr/bin/ar` (Makefiles using `ar`)
- `pkg install libopenblas` then `ln -s openblas/cblas.h cblas.h` (BLAS-enabled builds)
- `export TMPDIR=$PREFIX/tmp` + `export CLAUDE_CODE_TMPDIR=$PREFIX/tmp` in `~/.bashrc`

## Reports schema
Each `reports/<date>-<run>.md` contains:
- Frontmatter: date, model, corpus, params, BLAS on/off, hardware
- Loss curve summary (train + val per checkpoint)
- Peak RAM, swap usage, time per 100 iter
- Generation samples after run
- Anything Termux-specific that broke or had to be patched
