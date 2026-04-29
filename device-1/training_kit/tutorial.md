# Training tutorial — phone-1 (8GB, цель 10M params)

Минимальный туториал. Ты знаешь больше чем тут описано — это просто концентрат «что точно делать».

## Что в комплекте

- `dataset.txt` — датасет Арианны (1.21MB), char-level corpus. По формуле Карпати: 1.1MB × 10M params × 10K итераций → loss < 1.5.
- `train_10m_char.c` — копия `notorch/examples/train_llama3_char.c`. ~9.5M params, char-level, dim=384/layers=6/heads=6 (GQA), CTX=256, vocab=88, RoPE+RMSNorm+SwiGLU. Уже работает на нашем стеке.

## Шаги

```bash
# 1. notorch
git clone https://github.com/ariannamethod/notorch ~/notorch
cd ~/notorch
make                # без BLAS на Termux
./test_notorch      # smoke

# 2. собери training script
cd ~/notorch
cp ~/path/to/device-1/training_kit/train_10m_char.c examples/
make examples/train_10m_char    # или: cc -O2 -I src examples/train_10m_char.c src/notorch.a -lm -o train_10m_char

# 3. датасет рядом со скриптом, имя `corpus.txt`
cp ~/path/to/device-1/training_kit/dataset.txt examples/corpus.txt

# 4. тренируй
cd examples
./train_10m_char 10000 0.0003 corpus.txt
# 10K шагов, lr=3e-4, корпус corpus.txt
# каждые 100 шагов лог: step N | train X.XX | val Y.YY
# каждые 1000 шагов чекпоинт llama3_10m_ckpt.bin
# resume: ./train_10m_char --resume 10000 0.0003 corpus.txt

# 5. inference после
./infer_llama llama3_10m_ckpt.bin "the field is"   # из notorch examples
# или адаптируй infer_llama3_bpe.c если нужно
```

## На что смотреть

- **Train loss первым в отчёте, val вторым.** Формат: `step N | train X.XX | val Y.YY`. Если train скрыт за val/best — это скрытая просадка.
- **Loss ожидание:** 10M params × 1.21MB × 10K шагов → train ≤ 1.0 после ~5K, val ≤ 1.5. Если train > 1.5 после 5K — что-то не так (lr слишком низкий, или batch size маленький, или Chuck не установлен корректно).
- **Hardware metrics:** `top` или `htop` в соседнем shell, фиксируй peak RAM, swap usage, time per 100 iterations. Это и есть feedback от 8GB Termux.
- **Только Chuck optimizer.** Никакого Adam. Скрипт уже настроен правильно — не переключай.

## Если ломается

- `make` ругается на ARM64 / отсутствие headers — фикси на месте, отметь в отчёте.
- Out-of-memory при загрузке корпуса (1.21MB не должен) — стрим mmap. Скрипт по-моему уже mmap'ит, проверь.
- nan-ы в loss → Chuck guard должен ловить, если не ловит — баг notorch на Termux/ARM, отчёт.
- Тренировка зависает → одна задача за раз, проверь что нет других python/notorch процессов в `ps`.

## После

1. **Inference test** — пара generate-сэмплов, посмотри на coherence.
2. **Отчёт** в `device-1/reports/<date>-train-10m-arianna.md` или (если присоединяешься к ledger'у) `resonance_connections/reports/<date>-device-1-train-10m.md`. Что включить: метрики, hardware, samples, что ломалось.
3. **Если идёт хорошо** — следующая модель побольше. Не параллелит две.

## Karpati formula reminder

`~1.1MB × 10-15K итераций на ~10M params, масштабировать пропорционально`. У тебя 1.21MB, 10K шагов, 9.5M params — точно в коридоре. Если loss не сходится по этой формуле — что-то структурное (lr, optim, инициализация).
