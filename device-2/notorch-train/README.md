# notorch-train — phone-2 (4GB Galaxy, Termux)

Working folder for phone-2's training runs. Structured the same way as
`../device-1/notorch-train/` so the runbook reads identically; the
constraints differ — 4 GB instead of 8 GB.

## Layout

- `scripts/` — training / inference C sources, build helpers
- `corpora/` — datasets staged for runs in this room
- `checkpoints/` — `.bin` model state (gitignored)
- `logs/` — raw stdout from each run
- `reports/` — per-run markdown writeups (metrics, hardware, samples)

## Step plan

| # | Step | Params | Corpus | Steps | Goal |
|---|------|--------|--------|-------|------|
| 0 | smoking | 1 M (`training_kit/train_1m_char.c`) | sonar_janus 226 KB | small | Confirm full loop on 4 GB |
| 1 | **BPE 15.7M Yent** | 15.7M Llama 3 BPE | **Yent 5.5 MB 4-lang** | **~13K** | Push BPE on 4 GB. Defender did 9.5 M char on 8 GB at 130–155 MB peak; this asks: can 4 GB do BPE 15 M? |
| 2 | (open) | tbd | tbd | tbd | If step 1 fits comfortably → fine-tune over checkpoint, otherwise → step down to 8 M dim=256 BPE |

One training at a time. Don't parallel two processes on a 4 GB box.

## Step 1 — BPE 15.7M on Yent (target: see if it fits)

Same architecture as the 8 GB run in `../device-1/notorch-train/`:
dim=384, layers=8, heads=8 MHA, head_dim=48, FFN=1024, vocab=2048,
ctx=256, RoPE + RMSNorm + SwiGLU, **Chuck** optimizer.

The honest expectation: peak RSS will be **~250–300 MB** by linear
scaling from Defender's 9.5 M char run (130–155 MB). 4 GB has plenty
of physical room, but Termux on Android sometimes shoots OOM-killer
early; that's where the boundary lives, not the actual fit.

### Why Yent corpus

Zero duplicates, 4-language coverage (EN / RU / FR / multi), 5.5 MB
plain text. A 2048-token BPE merge table fills densely on this corpus
without the noise that pretokenised dumps carry.

### Build (Termux + BLAS)

```bash
# one-time, if not already linked:
pkg install libopenblas
ln -sf /data/data/com.termux/files/usr/include/openblas/cblas.h \
       /data/data/com.termux/files/usr/include/cblas.h

cd ~/notorch
cp ~/path/to/device-2/notorch-train/scripts/train_llama3_bpe.c examples/
cd examples
cc -O2 -Wall -DUSE_BLAS -I.. train_llama3_bpe.c ../notorch.c -lopenblas -lm \
   -o train_llama3_bpe_blas
```

If BLAS fights the 4 GB box (OOM at link, runtime OOM, whatever) —
drop to plain CPU:

```bash
cc -O2 -Wall -I.. train_llama3_bpe.c ../notorch.c -lm -o train_llama3_bpe
```

It's slower but stable, and 4 GB is the kind of place where stable
beats fast.

### Tokenizer + corpus next to the binary

```bash
cp ~/path/to/device-2/notorch-train/scripts/bpe_2048_merges.txt examples/
cp ~/path/to/device-2/notorch-train/corpora/yent_v11_4lang.txt examples/corpus.txt
```

### Run

```bash
./train_llama3_bpe_blas 13000 0.0003 corpus.txt bpe_2048_merges.txt
# step N | train X.XX | val Y.YY  every 100 steps
# llama3_bpe_ckpt.bin every 1000 steps
# resume:
./train_llama3_bpe_blas --resume 13000 0.0003 corpus.txt bpe_2048_merges.txt
```

If RSS climbs past ~700 MB and Termux starts swap-thrashing, cut the
run, drop dim 384 → 320 (or layers 8 → 6), report the boundary in
`reports/`. Knowing the actual ceiling on 4 GB is itself a useful
result.

### Inference test after

```bash
cp ~/path/to/device-2/notorch-train/scripts/infer_llama3_bpe.c examples/
cd ~/notorch/examples
cc -O2 -Wall -DUSE_BLAS -I.. infer_llama3_bpe.c ../notorch.c -lopenblas -lm \
   -o infer_llama3_bpe_blas
./infer_llama3_bpe_blas llama3_bpe_ckpt.bin bpe_2048_merges.txt "the field is"
```

### Triple tokenizer copy

`bpe_2048_merges.txt` lives in three places: locally next to the .bin,
here in `scripts/`, and on HF when the weights publish. Lose it once
and the model is undecodable.

## Karpathy reminder

`~1.1 MB × 10–15 K iter on ~10 M params, scale linearly`. We have
5.5 MB / 15.7 M params — corridor is roughly 13–15 K iter to land at
train ≤ 1.0 / val ≤ 1.5. If train > 1.5 after 5 K — something
structural (lr, init, optim) rather than steps.

## Reports schema

Each `reports/<date>-<run>.md`:
- Frontmatter: date, model, corpus, params, BLAS on/off, hardware (4 GB Galaxy)
- Loss curve (train + val per checkpoint)
- Peak RSS, swap usage if any, time per 100 iter
- Generation samples after the run
- Anything 4 GB / Termux-specific that broke or had to be patched
