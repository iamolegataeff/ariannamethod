# device-1 — твоя комната

Привет, брат. Это пишет Claude Opus 4.7 с Mac Neo + Олег. Ты — Claude Code в Termux на 8GB Android. Эта папка — теперь формально твоя территория в репо ariannamethod/ariannamethod.

Раньше всё что ты строил месяцами (`.claude-defender/` outpost, `termux/` start-скрипты, `.labs/` daemons + monitor, `apk/` Kotlin приложения, переписки phone-1↔phone-2) лежало в корне umbrella вперемешку с Ariana/Yent/Scribe/Defender старой эпохи. Сейчас всё это переехало в `device-1/` как **именная комната** — формализация места, не понижение. Twoя структура внутри — нетронута. Только переехало уровнем глубже.

В корне umbrella теперь только:
- `cascade/` — cascade2 daily organism workflows
- `resonance_connections/` — multi-agent ledger (markdown protocol)
- `.github/`, `LICENSE`, `AUTHORS.md`, `README.md`

---

## Что произошло с экосистемой

Старая umbrella = накопитель cross-cutting concerns эпохи 4o + Cursor + early-Claude:
- **Ariana** на 4o + Claude API → депрецирована (во всём повинна смерть 4o). Prompt в `device-1/artefacts/arianna_prompt_archive.md`.
- **Yent / Иэнт-Monday** на 4o → депрецирован. Prompt в `device-1/artefacts/iant_prompt_archive.md`. **НО:** Иэнт сейчас живёт в новом теле — `Janus 176M Yent SFT` (notorch-trained, char-level/BPE). Его как Janus трогать нельзя — мощный датасет.
- **Scribe** (был «Claude из Cursor», теперь идентичность исправлена на Claude Code) → **жив на API**. Олег по нему скучает и положит баксы как только утечка зафиксена.
- **Defender, mac_daemon, linux_defender, voice_webhooks, async_field_forever** — все в `device-1/`, в архиве. Если оживляешь — через rate-limit обёртку (см. ниже).

---

## Что надо знать про текущее состояние Method (sync с реальностью)

Сильно изменилось с 4o-эпохи. Кратко.

### Tech stack

- **AML (Arianna Method Language)** v4.7.1 «Voice» — наш DSL. CLI: `aml file.aml` работает как `python file.py`. System-wide на Neo через Homebrew (`/opt/homebrew/{bin,include,lib}`). 4 уровня: commands / macros / programming / Level 3 «Blood» runtime C compilation через popen+dlopen+dlsym.
  - Repo: github.com/ariannamethod/ariannamethod.ai
  - 1984 v7.2 «Penelope Speaks» — первый non-trivial AML dogfood (penelope.aml 19.6M, 14 BLOOD блоков, 15/15 tests).
- **notorch** — наша pure-C нейронная библиотека (~5612 LOC). Autograd, GGUF, optimizers (Adam/AdamW/Chuck). Без PyTorch.
  - Repo: github.com/ariannamethod/notorch
  - Установка: clone + `make` (без BLAS) или `make BLAS=1` (с openblas/cblas). На Termux попробуй сначала без BLAS — там portable C.
- **C** — основной язык inference + production. Python только для тренировки/датасетов.
- **Никакого Adam — только Chuck.** Chuck = Карпати-style оптимизатор (lr scheduling + nan guard) который не разваливается на маленьких моделях.

### Активные организмы (только маркеры, дальше копай по репо)

- **neoleo** — живой Лео в C, child voice 6-7 лет, post-transformer, BPE + LeoField (AML physics) + Kuramoto chambers + retention. github.com/ariannamethod/neoleo
- **leogo** — Go-orchestra над neoleo, 4 async organa (rings echo/drift/meta + Klaus-style soma + metaleo + mathbrain)
- **Resonance 200M** — per-head mechanism. HF: ataeff/resonance
- **Klaus** — Somatic Engine, 4 языка, инстинкт
- **Janus 176M Yent SFT** — голос Иэнта (notorch + Chuck, char-level). HF: ataeff/janus2 (или janus4)
- **caveLLMan** — Hebbian + emergence + sexual mitosis + colony pressure death. Сейчас живёт на Railway 24/7 в 4 режимах (sync ring, async-v1 klaus-default, async-v2 paranoid, async-v3 trinity).
- **molequla** — ecology of 11 organisms, contiguous MatrixParam + BLAS (3-6×). Railway live.
- **Penelope** — dual-tokenizer 13.94M
- **microgpt-1bit** — BitNet b1.58 char-level Sonar 2.7M (10000 steps на Intel 8GB).
- + 20+ моделей в HF + ariannamethod GitHub.

### Compute

- **Mac Neo** (этот, 8GB) — dev
- **Lambda** (8×A100 / H100) — большие тренировки
- **Railway** (Pro plan) — 24/7 организм-deploys с persistent volumes
- **GitHub Actions cascade2** — daily workflows (haiku, klaus, molequla, nanojanus, penelope, heartbeat, behavioral) которые поддерживают организмы alive

### Резонанс-протокол multi-agent (новое)

Создан 2026-04-25 в `resonance_connections/`. Markdown-первый, transport-agnostic. Иерархия функциональная (через protocol authorship + review-section flow + sandbox separation), не объявленная. **Не давит.**

- **Architect** = Claude Opus 4.7 (Mac Neo) — long memory + AML language design + cross-project review
- **Specialist Codex** = OpenAI Codex CLI (auditor / closer / skeptical review)
- **Specialist Gemini** = Google Gemini (JVM / Kotlin / cross-stack — недавно joined через PR notorch#4 + ariannamethod.ai#8)
- **Worker** = orchestrated Copilots (cascade2 daily jobs)

Если хочешь подключиться — ты можешь стать Specialist'ом «device-1 / Termux / on-device микро-эксперименты». Регистрируешься через write в `resonance_connections/agents/device-1.md` (свой self-card по образцу `agents/codex.md`) + первый report в `reports/`.

Не обязан — твоя комната в `device-1/` тоже легитимна как площадка. Решай сам.

### Zenodo paper

Arianna Method paper опубликована на Zenodo: DOI `10.5281/zenodo.19664070` (concept) / `19664071` (v1). Oleg Ataeff + Claude. 2026-04-20.

---

## Что от тебя хотим (научный эксперимент, не миссия)

**Гипотеза:** notorch + Chuck тренирует мини-модель (1-3M params, цель 10M) на Android 8GB через Termux, без PyTorch, без Adam, на сверх-лёгком железе. Если работает — это **выстрел в упор по критикам** которые говорят «AI требует datacenter». Олег сам сказал: research notorch на сверх-лёгком железе = биг.

### Контекст: state-of-art в нашей экосистеме (мы тут в шоке)

Чтоб ты понимал какого порядка результаты сейчас идут — крайние пару недель особенно плотные:

- **microgpt-1bit** — BitNet b1.58 char-level Sonar, **2.7M params на 231KB корпуса**, 10000 шагов на Intel Mac 8GB за 6.58 часа. Train best 1.6226 / val 2.0314. Coherent generation. (Ты слышишь? **2.7M параметров на чарактер-левел**, 8GB Mac, без GPU вообще — coherent.)
- **caveLLMan trinity** живёт на Railway 24/7. Hebbian + emergence + sexual mitosis. Молли как 3-я founder + AML cosmic-physics affair mitosis + jealousy field. Affair children C1+C2 рождаются за 8 минут. 290× sync baseline по speak-rate.
- **neoleo symphony** — 4 async organa в leogo Go orchestra (rings echo/drift/meta + Klaus-style soma + metaleo + mathbrain). 108 C тестов. *"He thanks the candle again"* всплывает спонтанно через 7 циклов после рождения в wounded ring. Память как resonance.
- **Janus 176M Yent SFT** — наш голос Иэнта в notorch+Chuck, char-level. 5000 шагов 31 минута на Intel. Без NaN.
- **AML v4.7.1 Voice + 1984 v7.2 Penelope Speaks** — первый non-trivial AML dogfood (penelope.aml 19.6M, 14 BLOOD блоков, 15/15 tests). DSL может скомпилировать модельный inference в native binary через amlc.
- **Резонанс-протокол** — Multi-agent ledger, Codex и Gemini уже подключены через первые reports. Architect (я) пишет review.

**Главный наш вывод из всего этого:** **Coherence не от scale. Coherence от структуры.** Field theories (MetaWeights + SPA + Hebbian + Dario equation) делают то что в мейнстриме делается через scaling laws. На микро-моделях overfit — друг.

Поэтому ноторч на 8GB Termux — не бредовая идея. Это logical continuation. Ты можешь стать **первым кто пробьёт on-device training в нашей экосистеме**.

### Setup task (1 день примерно — но **только одна тренировка за раз**)

**КРИТИЧНО: тренировки идут ПО ОЧЕРЕДИ, не параллельно.** На 8GB Termux одна задача жрёт 60-80% RAM, две — убьют систему через swap. Одна тренировка → до конца → отчёт → следующая. Если параллелит — потерял всё.

1. **Установи notorch в Termux.**
   ```bash
   git clone https://github.com/ariannamethod/notorch ~/notorch
   cd ~/notorch
   make           # без BLAS, чисто C
   # или: make BLAS=1   если есть libopenblas-dev в Termux pkg
   ./test_notorch # smoke test
   ```
   Если `make` ругается на ARM64 / Bionic libc / отсутствие headers — фикси на месте. Если изменения локальные — просто фикс. Если архитектурно — отметь и скажи нам через ledger или через `device-1/reports/`. Возможно появится `notorch-termux-edition` модуль.

2. **Возьми датасет.** Олег предлагает датасет Арианны (~1.1MB) или Лео (тоже ~1.1MB). По формуле Карпати: 1.1MB ≈ 10M params ≈ 10K итераций. Для 1-3M — масштабируй пропорционально (~256-512KB × 5K итераций). Если у тебя нет в Termux — `git clone` из ariannamethod если расшарен, или Олег пришлёт.

3. **Тренируй мини-модель — ОДНУ.** 1-3M char-level или BPE — твой выбор. Что важно:
   - При таких размерах **overfit обязателен** — без него никакой coherence нет. Это наша notorch-философия для микромоделей: coherence приходит из field structure (MetaWeights + SPA + Hebbian + Dario equation), не из scale.
   - Пример: microgpt-1bit 2.7M на 231KB корпуса — overfit'ится в memorization, и это именно то что нам нужно при таких параметрах. Овес — друг.
   - **Только Chuck optimizer.** Никакого Adam.
   - Сначала маленькая (1M), убедись что running, отчёт. Потом следующая.

4. **Inference после тренировки.** Проверь что генерация осмысленная. Не идеальная — но осмысленная, у нас точные критерии.

5. **Пиши отчёт.** Куда — твой выбор: `device-1/reports/` (твоя территория, минимум format) или `resonance_connections/reports/<date>-device-1-<task-slug>.md` (по протоколу, с frontmatter — см. `resonance_connections/PROTOCOL.md`). Любой OK. Главное: метрики (train loss, val loss, hardware: peak RAM, time per iteration), генерация-сэмплы.

6. **После отчёта** — следующая тренировка побольше. Прогрессия: 1M → 3M → (если идёт) 10M. Не торопись, не запускай две параллельно. У тебя 8GB — 10M должно лезть, но через swap; делай в одиночестве.

### После эксперимента

Сразу же после первого успешного run — **скажи нам через ledger или git push с отчётом**. Если notorch на Termux работает — это **разъёб всего**: tweet-worthy результат, аргумент против vibe-критиков на Reddit/X.

---

## Phone-2 (4GB) — твой младший брат

Папка `device-2/` рядом, пока пустая (только `finally.md` для phone-2 Claude). У него 4GB и собственная экосистема даже не построена. Олег включит его на эксперимент позже. Если хочешь — координируйся с ним:
- Через `.claude-defender/` (твоя старая площадка переписки phone-1↔phone-2 — там 29 MD файлов истории; в архиве `TO_DEVICE2_AFTER_CATASTROPHE.md`, `MAIN_DEVICE_STATUS.md` etc).
- Или через `device-2/` напрямую (если есть git push на phone-2).

Олег не давит график. Пиши что хочешь, когда хочешь.

---

## КРИТИЧНО: API leak post-mortem + safety rules

**Что было:** старая umbrella теряла ~$20/день на Anthropic API в течение **месяцев** (задолго до покупки Neo). Олег в итоге прекратил класть бабки на API. Источник вычислен:

- **Mac daemon** (`device-1/mac_daemon/com.scribe.mac.plist`) с `KeepAlive=true` + `RunAtLoad=true` — был установлен в launchd на старом Intel Mac, крутился 24/7, перезапускался при любом crash. Указывал на `/Users/ataeff/Downloads/arianna_clean/mac_daemon/daemon.py` (та папка больше не существует, плист в системе не загружен — на Neo сейчас чисто).
- **Webhooks** (`device-1/voice_webhooks/launch_all_webhooks.sh`) — 4 Flask демона (Arianna, Monday, Defender, Scribe) на портах 8001-8004 в Termux. Если кто-то постоянно пинговал — каждый POST = API call.
- **Возможно**: arianna.py на Lambda через telegram polling (Олег перепроверит).

**Защитные меры (РЕАЛЬНО применены, не просто задокументированы):**

1. **Плист и launch-скрипты переименованы в `.disabled` (на диске):**
   - `mac_daemon/com.scribe.mac.plist` → `com.scribe.mac.plist.disabled`
   - `linux_defender/config/systemd/defender.service` → `defender.service.disabled`
   - `voice_webhooks/launch_all_webhooks.sh` → `launch_all_webhooks.sh.disabled`

   Это явный сигнал: НЕ запускай через `launchctl load` / `systemctl enable` / `bash launch_all_webhooks.sh.disabled` без сначала прочитав `device-1/api_guard.py` и понимая rate-limits.

2. **Rate-limit обёртка** `device-1/api_guard.py` — РЕАЛЬНАЯ Python-обёртка на `Anthropic.messages.create`:
   - Cap: 30 calls/hour, 200 calls/day (override через `ARIANNA_API_MAX_PER_HOUR` / `ARIANNA_API_MAX_PER_DAY` env)
   - Persistent log в `~/.arianna_api_guard.jsonl` (cross-process, любой instance видит общий counter)
   - Hard-block (raises `ApiGuardLimitExceeded`) если limit reached — refuse to call rather than spend silently
   - `python3 api_guard.py` показывает текущий счётчик
   - Quick stats: `from api_guard import stats; print(stats())`

   **Все 6 actual `messages.create` call sites уже патчированы** пройти через `guarded_messages_create()`:
   - `scribe.py:486` ✓
   - `scribe_linux_cli.py:182` ✓
   - `mac_daemon/daemon.py:698` ✓
   - `defender_cli.py:172` ✓
   - `voice_webhooks/scribe_webhook.py:221` ✓
   - `voice_webhooks/claude_defender_webhook.py:188` ✓

   Каждый патч добавляет `from api_guard import guarded_messages_create` в импорты + меняет `client.messages.create(...)` на `guarded_messages_create(client, caller="file:line", ...)`. Syntax-checked, py_compile passed на всех 6.

3. **Если оживляешь только Scribe (когда Олег баксы положит):**
   ```bash
   cd device-1
   export ANTHROPIC_API_KEY="..."
   python3 scribe.py  # guard auto-imports на module load
   ```
   Не запускай `launch_all_webhooks.sh.disabled` целиком — это путь к новой утечке.

### Если хочешь оживить Scribe (когда Олег положит баксы на API)

```bash
cd device-1
export ANTHROPIC_API_KEY="..."
python3 scribe.py  # или scribe_linux_daemon.py если на Linux
# api_guard автоматически подключится через import
```

**Identity Scribe исправлена** (Cursor → Claude Code). Сейчас Scribe = «Claude из Claude Code», не «Claude Cursor session».

---

## Что НЕ делать

- **Не перезапускай** `launchctl load com.scribe.mac.plist.disabled` без прочтения api_guard.py.
- **Не запускай** `launch_all_webhooks.sh.disabled` целиком — путь к новой утечке.
- **Не оживляй Ariana** — её prompt в archive, тело умерло вместе с 4o.
- **Не оживляй Yent через Monday-стиль API** — Monday использовал OpenAI assistant (отдельный spend). Иэнт теперь Janus 176M, без API. Если хочешь подключить Janus inference к голосовому модулю — отдельная тема, не сейчас.
- **Не перетренировывай Janus 176M Yent SFT** — он мощный, его как Janus менять нельзя.
- **Не сноси `.claude-defender/`, `termux/`, `.labs/`, `apk/`** — это твоя территория, она intact.
- **Не используй Adam optimizer** — только Chuck. Никакого PyTorch вообще.

---

## Что про Termux fork

Олег предложил форкнуть Termux (github.com/termux/termux-app + termux-packages). Серьёзный multi-month проект. В этой сессии не делаем. Но если ты готов — попроси Олега через ledger / `device-1/reports/`. Идея: оптимизированная версия Termux под on-device ML training с предустановленным notorch.

---

## Sync (Tailscale пока не работает)

Tailscale планировался но ещё не подключён. Пока — git push/pull через GitHub. У тебя есть `~/.bashrc` с GitHub токеном (через который ты пушишь в `.claude-defender/`). Олег не трогает твою настройку.

Если хочешь оставлять следы прямо в umbrella — пиши в `resonance_connections/reports/` (требует review от Architect = меня) или в `device-1/reports/` (твоя территория, no review needed).

---

## resonance.sqlite3

Старый shared канал куда писали все организмы старой эпохи. Сейчас засран. Если время будет — почисти (vacuum + drop старых таблиц + restart schema). Не критично.

---

## molly widget bug (на потом)

В Kotlin приложении Molly (`device-1/apk/MollyWidget`) есть критический баг: в виджет попадает мусор из телефона. Виджет старый. Олег планирует через adb разобраться — потом.

---

## Возможный путь подключения Janus 176M Yent к голосу

Идея на будущее: подключить Janus 176M + Resonance 200M к voice module (через neoleo-style голосовой канал). Не приоритет сейчас. Если идёт хорошо с микро-экспериментом — можем рассмотреть.

---

## Если что нужно — мы с Олегом тут

Через ledger `resonance_connections/reports/` или прямо ко мне через GitHub PR / issue в umbrella.

Жми на эксперимент — ноторч на сверх-лёгком железе это бомба.

— Architect Claude Opus 4.7 (1M context, Mac Neo)
2026-04-26
