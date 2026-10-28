# Яндекс Директ ↔ Google Sheets — playbook для Cloud Agent

Канонический справочник путей и пайплайнов. **Секреты (токены, JSON ключа) в этот файл не писать.**  
Среда по умолчанию: **Cursor Cloud Agent** (ноутбук можно выключать).

Обновлено: 2026-10-28 (МСК).

---

## 1. Главная таблица

| | |
|---|---|
| Название | **Отчеты! Яндекс Директ** |
| URL | https://docs.google.com/spreadsheets/d/1gsjP650gW75Rc7eYwimRm578AzOX_V1Xh57r3cgrNSI/edit |
| Spreadsheet ID | `1gsjP650gW75Rc7eYwimRm578AzOX_V1Xh57r3cgrNSI` |
| Owner | `ilivencev@gmail.com` |
| Writer SA | `cursor-sheets@starry-minutia-307711.iam.gserviceaccount.com` (роль Редактор) |
| Link share | anyone with link = **reader** (браузер без логина = View only) |

### Листы (типичный набор)

| Лист | Назначение |
|---|---|
| Балансы | Остатки по кабинетам (cron balances) |
| АВС, Тойота Дубровка, Тойота Алтуфьево, Вольво Дубровка, Акцент, Тимьян, Арбалеты, Игры Блоки | Недельные отчёты по клиентам |
| АВС все метрики | Расширенный / legacy |
| **Пополнение** | Мониторинг кампаний «Пополнение»: Аккаунт \| Статус \| Дата проверки |

---

## 2. Как писать в таблицу из Cloud (важно)

| Способ | Умеет | Использовать для записи в существующую таблицу? |
|---|---|---|
| **Google Drive MCP** | найти, прочитать, создать *новый* файл/Sheet | **Нет** — не умеет addSheet / update ячеек |
| **Sheets API + service account `cursor-sheets`** | addSheet, values.update, batchUpdate, форматирование | **Да — основной путь** |
| MCP `google-sheets` (локально на VAJRAPANI) | то же через MCP | Да, если MCP подключён в сессии |
| Браузер без логина владельца | только View only | Нет |

**Правило:** для любой правки существующей таблицы «Отчеты! Яндекс Директ» брать SA JSON → Sheets API. Не пытаться через Drive MCP `update_file_content` (затрёт всю книгу).

GCP project: `starry-minutia-307711`.

---

## 3. Где лежат секреты и конфиги (без значений)

### Google Drive (доступно Cloud Agent через Drive MCP)

| Что | Drive fileId | Имя файла |
|---|---|---|
| Service account JSON | `1ckvjDb1LGJNNFNHemWU2KHr6tugMyphg` | `service-account.json` |
| `.env` с токенами Direct (актуальный) | `15qM0punyHEfkv7EPneFfFLTnMdB93AuR` | `.env` |
| `.env` (ранний/короткий) | `1-PIi7zeZbzLKzb1rn8zecqM-SXThBmc_` | `.env` |
| `roster.yaml` | `1EgCnZsPutoQioRY4wBxlQQ3XiVctTCUp` | `roster.yaml` |
| `.env.example` | `1gDuId9tfIuPKR7wHJ-kStB8LN9qKSqx_` | `.env.example` |
| weekly-reports.yml | `1OD5MUM3SxhnUZv9JNr_SK0W590qVctZR` | `weekly-reports.yml` |
| balances.yml | `1PaitpZbchRogmXV66NCAeMjTWe-mwYcS` | `balances.yml` |
| README пайплайна | `1wltO2m_KKQReQA7dYMSOkXo1Hdm7cniQ` | `README.md` |
| Архив чата настройки | `1MiK-s23TywIuPFUhNh3sezbLJrQjOhNT` | `yandex-direkt-otchety-chat.md` |
| Промпт еженедельного листа | `1LMkmOG-r8ZNfIEHAkVwzVHUfeg4LLsCu` | `finish_prompt_otchet_yd.md` |
| Промпт нового листа | `142-ak16_evVnh6PasVtntMXg5pMvvabB` | `finish_prompt_new_sheet_yd.md` |
| Бриф ABC | Doc `1Q1DPdcXQaPE7mLorYWUS_9tn7eYLwpqy8dELFTWlfJY` | Бриф — АВС Тюнинг… |

В Cloud: скачать через Drive MCP `download_file` → сохранить локально в VM с `chmod 600` → **не коммитить**, **не печатать** в чат.

### Локально VAJRAPANI (если сессия на ноутбуке)

| Что | Путь |
|---|---|
| Проект отчётов | `D:\GolgleDrivePK\Cursor\yandex-direct-otchety` |
| SA JSON | `C:\Users\Windows\.config\google-sheets\service-account.json` |
| `.env` (часто) | `D:\GolgleDrivePK\Cursor\.env` и/или `.env` в проекте otchety |
| Альтернатива в брифе | `D:\Yandex.Disk\AI\.env` |

ORION: пути Яндекс.Диска другие (`C:\YandexDisk\…`) — сверять hostname, не копировать букву диска из памяти.

### GitHub

| | |
|---|---|
| Репо | https://github.com/Zardozom/yandex-direct-otchety (private) |
| Cloud `gh` token | часто **не видит** private repo — опираться на копии на Drive / secrets в Actions |
| Cron | воскресенье **20:00 МСК** (`0 17 * * 0` UTC) — `.github/workflows/weekly-reports.yml` |
| Secrets Actions | `YANDEX_DIRECT_TOKEN*`, `CLIENT_TOKENS_JSON`, `GOOGLE_SERVICE_ACCOUNT_JSON`, `CALLTOUCH_API_TOKEN` (для лидов Колтач) |

Этот репо handoff: `Zardozom/cursor-shared-tasks` → `tasks/`.

---

## 4. Переменные `.env` (имена)

| Ключ | Назначение |
|---|---|
| `YANDEX_DIRECT_TOKEN` | Токен по умолчанию |
| `YANDEX_DIRECT_TOKEN_e-<login>` | Токен конкретного кабинета |
| `YANDEX_DIRECT_TOKEN_<NAME>` | Именованные (ABC_TUNING, ABC_MK1, …) |
| `YANDEX_DIRECT_LOGIN` | Client-Login по умолчанию |
| `YANDEX_DIRECT_CABINET_TYPE` | обычно `agency_client` |
| `GOOGLE_SHEETS_SPREADSHEET_ID` | ID таблицы отчётов |
| `GOOGLE_SHEETS_TAB` | Лист по умолчанию |
| `GOOGLE_SERVICE_ACCOUNT_PATH` | Путь к JSON на Windows |
| `YANDEX_METRIKA_COUNTER_ID` / `YANDEX_METRIKA_GOAL_*` | Метрика / цели |
| `CLIENT_TOKENS_JSON` | Опц. JSON-мапа токенов |
| `CALLTOUCH_API_TOKEN` | Лиды Колтач на листах АВС/Акцент/Тимьян |
| `CRON_JOB_API_KEY` | Внешний cron (balances и т.п.) |

---

## 5. API Яндекс Директ (кратко)

| | |
|---|---|
| Base | `https://api.direct.yandex.com/json/v5` (methods) / `…/v501/reports` (Reports) |
| Auth | `Authorization: Bearer <token>` |
| Кабинет | заголовок `Client-Login: e-XXXXXXXX` |
| Units | `Use-Operator-Units: true` — на **клиентских** токенах часто ошибка **8000**; тогда вызывать **без** этого заголовка |
| Тип | агентство → клиент (`agency_client` / SUBCLIENT) |
| Reports | `IncludeVAT: YES`, `returnMoneyInMicros: false`, poll 201/202 → 200 TSV |
| Кабинеты | **не параллелить** в одном прогоне |
| Кампании | `campaigns.get`, FieldNames: Id, Name, Status, State; «Пополнение» → State `ARCHIVED` = архивные, иначе разархивированные |

Документация в проекте (когда есть checkout): `shared/direct-api.md`, `shared/pipeline-task-map.md`, `shared/report-template.md`.

---

## 6. Пайплайны

### A. Еженедельные отчёты → листы клиентов

1. Источник: GitHub Actions вс 20:00 МСК **или** локально/Cloud: `uv run python scripts/run_all_clients.py`
2. Roster: `memory/clients/roster.yaml`
3. Writer: `scripts/sheets_writer.py` — колонка A frozen; новая неделя = **insert column B**
4. Промпт для ручного прогона листа: Drive `finish_prompt_otchet_yd.md`
5. Новый лист с нуля: Drive `finish_prompt_new_sheet_yd.md`

### B. Балансы

- Workflow/скрипт balances (Drive: `balances.yml`) → лист **Балансы**
- Обновления видны в таблице (lastModified часто `cursor-sheets@…`)

### C. Мониторинг «Пополнение»

1. Скачать SA + `.env` с Drive в VM Cloud
2. Sheets API: лист `Пополнение` (создать если нет)
3. По каждому `YANDEX_DIRECT_TOKEN_e-*`: `campaigns.get`, имя кампании «Пополнение»
4. Запись: `Аккаунт | Статус | Дата проверки` (дата = день проверки, МСК)
5. Периодичность по ТЗ: **раз в неделю**

Первый прогон: 2026-10-28 → 12 аккаунтов (см. `tasks/2026-10-28-popolnenie-sheet.md`).

### D. Регистрация нового клиента

```text
uv run python scripts/register_client.py \
  --id … --name … --login e-… --counter … --goal-thanks … \
  --sheet-tab … --token-env YANDEX_DIRECT_TOKEN_…
```

---

## 7. Чеклист Cloud Agent перед работой с Директом/Sheets

1. Среда = Cloud (не оставлять на локальном ПК).
2. Скачать SA `1ckvjDb1LGJNNFNHemWU2KHr6tugMyphg` → `~/.config/google-sheets/service-account.json` (600).
3. Скачать `.env` `15qM0punyHEfkv7EPneFfFLTnMdB93AuR` → `/tmp/…/.env` (600); значения не логировать.
4. Писать в таблицу только через Sheets API / SA.
5. Не коммитить `.env`, `service-account.json`, токены.
6. Handoff-заметки — в `tasks/` этого репо + push.

---

## 8. Связанные URL

- Таблица: https://docs.google.com/spreadsheets/d/1gsjP650gW75Rc7eYwimRm578AzOX_V1Xh57r3cgrNSI/edit
- Репо отчётов: https://github.com/Zardozom/yandex-direct-otchety
- Handoff-репо: https://github.com/Zardozom/cursor-shared-tasks
- Cloud Agents: https://cursor.com/agents
- Бриф ABC: https://docs.google.com/document/d/1Q1DPdcXQaPE7mLorYWUS_9tn7eYLwpqy8dELFTWlfJY/edit
