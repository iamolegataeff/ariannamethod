# phone-1 (`arianna-method`, Galaxy A56 8GB) — Training mission

Training mission for Termux Claude on Galaxy A56. **All decisions are pre-made** by Oleg; this brief carries the 6-point proof so the training-gate hook lets the run start.

---

## 6-point brief (Oleg's spec, satisfies `feedback_failure_unsolicited_finetune_2026_04_27.md`)

1. **Organism:** notorch LLaMA 3 BPE, ≈ 15.7M params (`examples/train_llama3_bpe.c`).
2. **Dataset:** `~/arianna-datasets/yent/yent_v11_en_final.txt` — 5.4 MB, 57610 lines of cynical-AI Yent corpus (curated by Oleg, not upstream defaults; conforms to `feedback_no_default_datasets_2026_04_27.md`).
3. **Karpathy scale:** script default 15 000 steps for ~15M params at ~1.1 MB / step-budget; Yent corpus 5.4 MB cycles through so steps see > 1 epoch of diverse exposure. Run **15 000 steps** baseline.
4. **Architecture:** LLaMA 3 BPE — `dim=384`, `layers=8`, `heads=8`, `head_dim=48`, `ffn=1024`, `ctx=256`, `vocab=2048`. RoPE + MHA + SwiGLU + RMSNorm. **BPE, not char-level** (conforms to `feedback_no_char_models.md`).
5. **Tokenizer:** `~/arianna/notorch/examples/bpe_2048_merges.txt` (1792 merges, vocab 2048) — same file used by inference, deterministic.
6. **Script:** `~/arianna/notorch/examples/train_llama3_bpe.c` — verified, in upstream repo (`github.com/ariannamethod/notorch`), v2.3.0 release.

Closed milestone weights (`sonar_*`, `microjanus_*`, `penelope`, `nanojanus`, `arianna_36m`, `pitomadom`, `lee_v8`, `DoE.coder`) — **not touched**, this is fresh training from scratch.

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

Yent corpus is delivered by Neo via rsync (Tailscale). Verify after Neo pushes:

```bash
ls -lh ~/arianna-datasets/yent/yent_v11_en_final.txt
wc -lc ~/arianna-datasets/yent/yent_v11_en_final.txt
# expect: 5.4M, 57610 lines
```

### 3. Build trainer

```bash
cd ~/arianna/notorch
which clang || pkg install -y clang make
make train_llama3_bpe
ls -la ./train_llama3_bpe
```

If `make` fails (Termux glibc / linker quirks) — show the full error to Oleg, do NOT improvise. The script is verified on Linux + macOS; Termux is the new target — first run is the validation.

### 4. Acknowledge training-gate hook

The PreToolUse hook blocks training-like commands by default. This 6-point brief is Oleg-approved; create the daily ack flag:

```bash
mkdir -p ~/.claude/hooks/state
touch ~/.claude/hooks/state/train-ack-$(date +%Y%m%d).flag
ls ~/.claude/hooks/state/
```

### 5. Run

```bash
cd ~/arianna/notorch
./train_llama3_bpe 15000 0.0003 \
    ~/arianna-datasets/yent/yent_v11_en_final.txt \
    ~/arianna/notorch/examples/bpe_2048_merges.txt 2>&1 | tee train_log_$(date +%Y%m%d_%H%M%S).log
```

`./train_llama3_bpe [steps] [lr] [corpus.txt] [merges.txt]`. Default lr `3e-4` (Chuck optimizer in notorch).

Resume on restart: append `--resume` after the binary name.

### 6. Reporting format

Per `memory/feedback_show_train_loss.md`: report **train loss first, then val**.

```
step N | train X.XX | val Y.YY
```

Log every 100 steps; checkpoint every 1000 (script defaults). Push status reports to `phones/phone-1-status-<DATE>.md` if a session boundary.

---

## What NOT to do

- ❌ Switch corpus / tokenizer / arch on the fly — that breaks the 6-point contract.
- ❌ Use Adam / mainstream optimizer — Chuck is the only choice (`feedback_adam_ban_2026_04_29.md`).
- ❌ Fabricate metrics. Only report numbers from the live tee log file. If asked for "current loss" without a log line — say "не успел залогиться, последняя строка: ...".
- ❌ Touch closed milestone weights or override existing checkpoints under different names.
- ❌ Run multiple training processes in parallel on 8GB Galaxy — RAM will OOM.

---

## Expected behaviour (informational, not prediction)

Defender 9.5M LLaMA 3 char-level on Galaxy A56 8GB took **2h13m for 10K steps, val 1.1460** — see `memory/milestone_defender_termux_10k_2026_04_27.md`. This run is 15.7M (≈ 1.65× weights) and BPE (denser context per step), so wall-time is **not** projected — measure it. Expected `train` initial loss ≈ `log(2048) ≈ 7.6`, descending. Stop at 15 000 or sooner if `train` flatlines for 1 000 steps.

If you want to extend: new 6-point brief from Oleg.

---

— Neo Claude
2026-05-06
