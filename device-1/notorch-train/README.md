# notorch-train — Termux on-device training experiments

Working folder for Defender's notorch + Chuck training runs on Galaxy Termux (8GB Android, ARM64). All runs follow the strategy laid out by Oleg in the new-axis message and the Architect in `device-1/finally.md`.

## Layout
- `scripts/` — modified or generated training/inference C sources, build helpers
- `configs/` — per-run config notes (params, lr, steps, BLAS on/off)
- `checkpoints/` — `.bin` model state (gitignored if heavy)
- `logs/` — raw stdout from each run
- `reports/` — per-run markdown writeups (metrics, hardware, samples)

## Run plan (Oleg, 2026-04-26)

| # | Step | Params | Corpus | Steps | Goal |
|---|------|--------|--------|-------|------|
| 0 | smoking | 9.5M (full Llama3) | Arianna 1.21MB | 100 | Verify pipeline |
| 1 | micro | ≤1M | tbd | small | Confirm full loop on 8GB |
| 2 | overfit | 1.5–2M | Dracula ~200KB | tbd | Chuck vs Adam at micro scale |
| 3 | headline | 9.5M Llama3 char | Arianna 1.21MB | 10000 | first 10M training on Termux |

Each step ends with a report in `reports/`, then the next step starts. **Never two trainings in parallel** (8GB swap death).

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
