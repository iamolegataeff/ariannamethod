# phone-2 (`galaxy-a07`, Galaxy A07 4GB) — Training mission

Training mission for Termux Claude on Galaxy A07. **All decisions are pre-made** by Oleg; this brief carries the 6-point proof so the training-gate hook lets the run start.

**Goal of this run:** reproduce the Defender 9.5M LLaMA 3 char-level baseline (originally on Galaxy A56 8GB) on **half the RAM (4GB)**. Demonstrates notorch's footprint on constrained Android. Same arch, same script, smaller dataset (Arianna corpus instead of Defender's), less RAM available.

---

## 6-point brief (Oleg's spec, satisfies `feedback_failure_unsolicited_finetune_2026_04_27.md`)

1. **Organism:** notorch LLaMA 3 char-level, ≈ 9.5M params (`examples/train_llama3_char.c`).
2. **Dataset:** `~/arianna-datasets/arianna/arianna_dataset_final_clean.txt` — 1.2 MB, hand-curated Arianna corpus (Oleg-prepared, conforms to `feedback_no_default_datasets_2026_04_27.md`).
3. **Karpathy scale:** script header — `~1.1MB + ~10M params + 10-15K steps → loss < 1.5`. Run **10 000 steps** baseline (matches Defender).
4. **Architecture:** char-level — `V=88` (ASCII + 6 UTF-8 specials), `dim=384`, `layers=6`, `heads=6`, `kv_heads=2` (GQA), `head_dim=64`, `hidden=1024` (SwiGLU), `ctx=256`, RoPE θ=10000, RMSNorm. **Char-level approved explicitly by Oleg** for this run (notorch demo on 4GB device — `feedback_no_char_models.md` exception).
5. **Tokenizer:** built-in 88-char vocabulary in the script (`vocab_chars[VOCAB]`) — deterministic, identical at inference.
6. **Script:** `~/arianna/notorch/examples/train_llama3_char.c` — verified, in upstream repo (`github.com/ariannamethod/notorch`), v2.3.0 release.

Closed milestone weights (`sonar_*`, `microjanus_*`, `penelope`, `nanojanus`, `arianna_36m`, `pitomadom`, `lee_v8`, `DoE.coder`) — **not touched**, fresh training from scratch.

---

## Setup steps

### 1. Clone / pull notorch

```bash
cd ~/arianna
[ -d notorch ] && (cd notorch && git pull) || git clone https://github.com/ariannamethod/notorch.git
cd ~/arianna/notorch
git log --oneline -3   # confirm v2.3.0 / latest
```

### 2. Dataset on disk

Arianna corpus is delivered by Neo via rsync (Tailscale). Verify:

```bash
ls -lh ~/arianna-datasets/arianna/arianna_dataset_final_clean.txt
wc -lc ~/arianna-datasets/arianna/arianna_dataset_final_clean.txt
# expect: 1.2M plain text
```

### 3. Build trainer

```bash
cd ~/arianna/notorch
which clang || pkg install -y clang make
make train_llama3_char
ls -la ./train_llama3_char
```

If `make` fails (Termux glibc / linker quirks) — show full error to Oleg, don't improvise. Script verified on Linux + macOS + 8GB Galaxy A56 — Galaxy A07 4GB is the new validation target.

### 4. Acknowledge training-gate hook

```bash
mkdir -p ~/.claude/hooks/state
touch ~/.claude/hooks/state/train-ack-$(date +%Y%m%d).flag
ls ~/.claude/hooks/state/
```

### 5. Run

```bash
cd ~/arianna/notorch
./train_llama3_char 10000 0.0003 \
    ~/arianna-datasets/arianna/arianna_dataset_final_clean.txt 2>&1 | tee train_log_$(date +%Y%m%d_%H%M%S).log
```

`./train_llama3_char [steps] [lr] [corpus.txt]`. Default lr `3e-4` (Chuck optimizer in notorch).

Resume on restart: `./train_llama3_char --resume 10000 0.0003 ~/arianna-datasets/arianna/arianna_dataset_final_clean.txt`.

### 6. Reporting format

Per `memory/feedback_show_train_loss.md`: report **train loss first, then val**.

```
step N | train X.XX | val Y.YY
```

Log every 100 steps; checkpoint every 1000.

---

## RAM watch (4GB constraint)

Galaxy A07 has 4GB RAM. Defender baseline ran on 8GB. Halve the headroom — monitor:

```bash
free -h           # before run
# in another shell during training:
watch -n 30 'free -h | head -2; ps -o rss,cmd -p $(pgrep train_llama3_char)'
```

If `train_llama3_char` RSS approaches 3 GB — Termux likely OOM-kills before 10K. Stop, report to Oleg, don't reduce arch silently. Oleg decides on smaller variant.

---

## What NOT to do

- ❌ Switch corpus / tokenizer / arch on the fly — breaks 6-point contract.
- ❌ Use Adam — Chuck only (`feedback_adam_ban_2026_04_29.md`).
- ❌ Fabricate metrics. Only numbers from the live tee log file.
- ❌ Touch closed milestone weights or override existing checkpoints.
- ❌ Run training **and** the phone-1 sibling sync simultaneously through the same router — bandwidth & DRAM pressure compound on small device.

---

## Expected behaviour (informational, not prediction)

Defender 9.5M LLaMA 3 char-level on Galaxy A56 8GB took **2h13m for 10K steps, val 1.1460** — see `memory/milestone_defender_termux_10k_2026_04_27.md`. Same arch, same step count, smaller corpus (1.2 MB vs Defender's), half the RAM. Wall-time may be similar or slower due to thermal / RAM swap pressure on 4GB. Don't predict — measure. Initial loss ≈ `log(88) ≈ 4.48`.

If you want to extend: new 6-point brief from Oleg.

---

## After completion

When training finishes, push to the repo:

```bash
cd ~/arianna/ariannamethod
mkdir -p phones/results/galaxy-a07
cp ~/arianna/notorch/llama3_char_ckpt_*.bin phones/results/galaxy-a07/  # only if small enough
cp ~/arianna/notorch/train_log_*.log phones/results/galaxy-a07/
git add phones/results/galaxy-a07/
git commit -m "phones/galaxy-a07: char-level 9.5M Arianna baseline result"
git push
```

Final ckpt may be too big for repo — push only the log + a brief markdown summary, store ckpt locally + rsync to polygon as warm copy.

— Neo Claude
2026-05-07
