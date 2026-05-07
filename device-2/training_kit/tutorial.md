# Training tutorial — phone-2 (4GB, цель 1M params)

Сжатая версия. У тебя 4GB — параметры скромнее, но принцип тот же.

## Что в комплекте

- `dataset.txt` — sonar_janus_trained corpus (231KB, char-level). Маленький — для overfit на 1M params достаточно.
- `train_1m_char.c` — адаптированный `train_llama3_char.c` под твой объём: dim=128/layers=4/heads=4, HIDDEN=384, CTX=128, vocab=88. ~1M params. RoPE + RMSNorm + SwiGLU + Chuck optimizer.

Оригинал на 9.5M (для phone-1) — `device-1/training_kit/train_10m_char.c`. Если интересно.

## Шаги

```bash
# 1. notorch
git clone https://github.com/ariannamethod/notorch ~/notorch
cd ~/notorch
make                # без BLAS — на 4GB BLAS даже мешает
./test_notorch

# 2. сборка
cp ~/path/to/device-2/training_kit/train_1m_char.c examples/
cd ~/notorch
make examples/train_1m_char
# или: cc -O2 -I src examples/train_1m_char.c src/notorch.a -lm -o train_1m_char

# 3. датасет
cp ~/path/to/device-2/training_kit/dataset.txt examples/corpus.txt

# 4. тренируй (меньше шагов потому что меньше corpus)
cd examples
./train_1m_char 5000 0.0005 corpus.txt
# 5K шагов, lr=5e-4 (чуть выше bcw меньше params), corpus.txt
# каждые 100 шагов лог
# каждые 1000 шагов чекпоинт llama3_1m_ckpt.bin
# resume: ./train_1m_char --resume 5000 0.0005 corpus.txt

# 5. inference
./infer_llama llama3_1m_ckpt.bin "the field"
```

## Realistic ожидания на 4GB

- **Peak RAM**: ~700MB-1GB. Должно лезть.
- **Time per 100 iter**: 30-60 секунд (Cortex-A78, ARM64). 5K шагов ~30-50 минут.
- **Train loss target**: ≤ 1.5 после 3K шагов на 231KB. Overfit — друг, не fight'ься с ним.
- **Если ARM64 Cortex быстрее ожиданий** — попытайся 2M или 3M (правь DIM/NLAYERS в train_1m_char.c — но **сначала отчёт по 1M, потом следующая**).

## Если ломается на 4GB

- OOM при загрузке: mmap корпуса (скрипт mmap'ит уже)
- OOM при тренировке → DIM 128→96, layers 4→3
- Swap зависает Termux → KILL training, swap settings overhauled, repost
- nan loss → Chuck guard миссит на ARM64? Если да — это **критический finding**, скажи в отчёте, отдельный bug в notorch-termux.

## Только Chuck. Никакого Adam.

Скрипт уже настроен. Не переключай.

## После

1. **Inference test** — несколько сэмплов.
2. **Отчёт** в `device-2/reports/` или `resonance_connections/reports/<date>-device-2-train-1m.md`. Метрики: train loss, val loss, peak RAM, time per iter, samples, что ломалось.
3. **Если идёт** → 2M (DIM 128→160, NLAYERS 4→5). Снова **одна за раз**.
4. **Если не идёт** — отчёт о точке отказа тоже разъёб, мы хоть узнаем границу.
