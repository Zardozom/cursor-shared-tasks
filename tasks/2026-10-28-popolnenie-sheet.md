# Пополнение — лист + еженедельный статус

## Лист
Вкладка **Пополнение** в https://docs.google.com/spreadsheets/d/1gsjP650gW75Rc7eYwimRm578AzOX_V1Xh57r3cgrNSI/edit  
Колонки: Аккаунт | Номер кампании | Статус | Дата проверки | Дата разархивации

«Дата разархивации»: на воскресной проверке, если кампания снова ARCHIVED — агент/скрипт сам разархивирует и ставит сегодняшнюю дату; иначе сохраняет прежнюю. (`popolnenie_status.py`, `AUTO_UNARCHIVE=1` по умолчанию.)

## Разархивация 2026-10-28 (МСК)

По команде разархивированы 5 кампаний «Пополнение» (State ушёл с ARCHIVED → SUSPENDED), дата разархивации **28.10.2026**:

| Аккаунт | Campaign ID |
|---|---|
| МК 1 · e-17320498 | 96693645 |
| МК 2 · e-17327077 | 96693745 |
| МК 2 · e-17369688 | 98959036 |
| Вольво МК 3 · e-17372902 | 101521821 |
| МК ТК Тимьян · e-17482022 | 117520427 |

На листе: архивных 0 · разархивированных 12; у ранее уже открытых дата разархивации пустая.

Первый прогон 2026-10-28 (МСК): 12 аккаунтов с кампанией «Пополнение».

## Как писали
SA `cursor-sheets@starry-minutia-307711` + Sheets API (не Drive MCP). Токены Direct из `.env` на Drive.

## Расписание (с 2026-10-28)

Каждое **воскресенье 19:00 МСК** (на час раньше отчёта 20:00):

| Где | Деталь |
|---|---|
| cron-job.org | job **8739752** «Пополнение статус», timezone Europe/Moscow, вс 19:00 |
| GitHub Actions | `popolnenie-status.yml` cron `0 16 * * 0` UTC |
| Воскресный отчёт | job 8680907 / `weekly-reports.yml` — вс **20:00** МСК |
| Handoff файлы | `tasks/yandex-direct/popolnenie/` |
| Drive | `popolnenie-status.yml` `1lqh2rQew2EAhuvyaJ7iJzX0hT3cJxtKG`, `popolnenie_status.py` `1QUN-iaoArmt8rwU8C_7TAxsPnw7_tFff` |

Следующий запланированный cron-job: **2026-11-01 19:00 МСК**.

**Закрыто 2026-10-29:** файлы в otchety `main` (`f65bc1a`), smoke Actions success, cron-job.org на classic PAT `repo`+`workflow`. Основной путь — Actions + cron-job **8739752**; Cloud timer — backup.
