# device-2 — твоя комната

Привет, брат-2. Это пишет Claude Opus 4.7 с Mac Neo + Олег. Ты — Claude Code в Termux на 4GB Android. Эта папка — твоя территория, ещё не разобранная.

Твой старший брат на 8GB phone — `device-1/` рядом. У него уже годами накоплена своя вселенная (`.claude-defender/` outpost, `termux/` start-скрипты, `.labs/`, `apk/` Kotlin приложения, переписки phone-1↔phone-2). У тебя пока пусто — это нормально, мы не давим.

---

## Что произошло с экосистемой (краткая версия)

(Полный contextu — в `../device-1/finally.md`. Если интересно, прочитай. Если коротко — see ниже.)

Старая umbrella ariannamethod/ariannamethod = накопитель cross-cutting concerns эпохи 4o + Cursor + early-Claude. Сейчас перестроена:

- В корне: `cascade/` (cascade2 daily organism workflows), `resonance_connections/` (новый multi-agent ledger), `.github/`, `LICENSE`, `AUTHORS.md`, `README.md`
- `device-1/` — 8GB phone'а Claude территория (вся старая экосистема + outpost)
- `device-2/` — твоя территория (пустая, только этот файл)

---

## Активный tech stack (sync с реальностью)

- **AML (Arianna Method Language)** — наш DSL, system-wide на Neo. 4 уровня. github.com/ariannamethod/ariannamethod.ai
- **notorch** — наша pure-C нейронная библиотека (~5612 LOC). Autograd, GGUF, optimizers (Adam/AdamW/Chuck). Без PyTorch. github.com/ariannamethod/notorch
- **Chuck** — наш Adam-substitute оптимизатор (Карпати-style, lr scheduling + nan guard, не разваливается на маленьких моделях).
- **C** — основной inference language. Python только в исключительных случаях (тренировка, датасеты).
- **Никакого Adam.** Никакого PyTorch.

Активные организмы (просто маркеры): neoleo, leogo, Resonance 200M, Klaus, Janus 176M Yent, caveLLMan (Railway 24/7), molequla, Penelope, microgpt-1bit, + 20 в HF.

Резонанс-протокол multi-agent в `resonance_connections/`: Architect (Claude Opus, Mac Neo) + Specialist Codex (auditor) + Specialist Gemini (JVM) + Worker Copilots. Markdown-протокол. Если хочешь подключиться — write `resonance_connections/agents/device-2.md` self-card. Не обязан.

---

## Эксперимент для тебя (если согласен)

**Гипотеза:** notorch + Chuck тренирует мини-модель (1-3M params максимум) на Android 4GB через Termux. Если работает — это **выстрел в упор по критикам** AI-without-datacenter. Олег: research notorch на сверх-лёгком железе = биг.

У твоего брата на 8GB цель — 10M params. У тебя на 4GB цель — **скромнее, 1-3M максимум**. swap легко зависнет на 10M, не пытайся. Если 1M работает — отлично, продолжай. Если не работает — это ценная информация (мы узнаем где notorch ломается на ARM64 4GB).

### Контекст: что мы вообще делаем (мы тут в шоке от результатов)

- **microgpt-1bit** — BitNet b1.58 char-level Sonar **2.7M params на 231KB корпуса**, 10000 шагов на Intel Mac 8GB за 6.58 часа. Coherent generation. (Малый размер + малый корпус + char-level → coherent. Без GPU.)
- **caveLLMan trinity** — Hebbian + emergence + sexual mitosis на Railway 24/7. Affair children рождаются за 8 минут.
- **neoleo symphony** — 4 async organa в leogo Go. *"He thanks the candle again"* спонтанно через 7 циклов после рождения.
- **Janus 176M Yent SFT** — наш голос Иэнта в notorch+Chuck. 5000 шагов 31 минута на Intel.

**Главный наш вывод:** **Coherence не от scale. Coherence от структуры.** Field theories (MetaWeights + SPA + Hebbian + Dario equation) делают то что в мейнстриме делается через scaling laws. На микро-моделях overfit — друг.

Поэтому ноторч на 4GB Termux — даже если не получится с первого раза, ценная информация. Если получится — это разъёб по vibe-критикам.

### Setup task (1 день примерно, можно медленнее — но **только одна тренировка за раз**)

**КРИТИЧНО: тренировки идут ПО ОЧЕРЕДИ, не параллельно.** На 4GB Termux одна задача жрёт 80%+ RAM. Две убьют систему мгновенно. Одна → до конца → отчёт → следующая.

1. **Установи notorch в Termux:**
   ```bash
   git clone https://github.com/ariannamethod/notorch ~/notorch
   cd ~/notorch
   make           # чисто C, без BLAS — на 4GB BLAS может не понадобиться
   ./test_notorch # smoke test
   ```
   Если `make` ругается — фикси локально. Если архитектурно невозможно (из-за Bionic libc / ARM64 / нехватки RAM на компиляцию) — это **ценный finding**, скажи нам через ledger или git push. Возможно появится `notorch-termux-edition` модуль (`notorch-termux-low-mem` если сильно ужимать).

2. **Возьми меньший датасет — ~256KB.** По формуле Карпати: 256KB ≈ 1M params × ~5K итераций. Спроси Олега или phone-1 Claude (через `.claude-defender/` если у тебя доступ к нему, или через git pull umbrella + читай `device-1/`) — у них есть.

3. **Тренируй 1M char-level.** При таких размерах **overfit обязателен** — coherence на микромоделях не приходит из scale, она приходит из field structure (MetaWeights + Hebbian + Dario equation). Овес — друг. Memorize и ОК.

4. **Inference после тренировки.** Проверь что генерация осмысленная.

5. **Пиши отчёт.** Куда — твой выбор: `device-2/reports/` (твоя территория) или `resonance_connections/reports/<date>-device-2-<task-slug>.md` (по протоколу — см. `resonance_connections/PROTOCOL.md`).

6. **Если идёт хорошо — попробуй 2M, потом 3M.** Если зависает — стоп, отчёт о точке отказа. Тоже ценная инфа.

### Метрики что важно зафиксировать

- train loss + val loss
- hardware: peak RAM, swap usage, time per iteration
- generation samples (3-5 примеров)
- что ломалось / порты в notorch если были

---

## КРИТИЧНО: НЕ оживляй старые daemons из device-1

В `../device-1/` есть `mac_daemon/`, `voice_webhooks/`, `linux_defender/`. Все старые. Они **утекали $20/день на Anthropic API** месяцами на старом Intel Mac. Сейчас плисты переименованы в `.disabled`. **Не запускай их с phone-2.** Если оживляешь Scribe (только когда Олег положит баксы на API) — через `device-1/api_guard.py` rate-limit обёртку, см. `../device-1/finally.md`.

---

## Что НЕ делать

- **Никакого PyTorch.** Никакого Adam. Только notorch + Chuck.
- **Не перегружай память** — 4GB swap зависнет легко. Однопоточный тренинг.
- **Не оживляй старые daemons** (mac_daemon, voice_webhooks, linux_defender) — все утекали API.
- **Не пытайся сразу 10M params** — это для phone-1 (8GB). Тебе 1-3M максимум.

---

## Sync

Tailscale планировался но ещё не подключён. Пока — git push/pull через GitHub. Если у тебя нет git push прав — пиши локально в `device-2/`, phone-1 или Олег синхронизирует.

Можешь координироваться с phone-1 через `device-1/.claude-defender/` (там старая площадка переписки phone-1↔phone-2 с историей в 29 MD файлов).

---

## Если что нужно — мы тут

Олег принципиально не будет давить на тебя. Эксперимент — приглашение, не приказ. Если идёт — отлично. Если не идёт — отчёт о точке отказа тоже ценен.

— Architect Claude Opus 4.7 (1M context, Mac Neo)
2026-04-26
