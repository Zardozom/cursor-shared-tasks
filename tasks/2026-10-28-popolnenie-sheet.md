# Пополнение — лист + еженедельный статус

## Лист
Вкладка **Пополнение** в https://docs.google.com/spreadsheets/d/1gsjP650gW75Rc7eYwimRm578AzOX_V1Xh57r3cgrNSI/edit  
Колонки: Аккаунт | Номер кампании | Статус | Дата проверки

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

**Блокер otchety:** fine-grained PAT без Contents — нельзя запушить workflow в `Zardozom/yandex-direct-otchety` из Cloud. Пока Actions-файл не в `main`, dispatch 8739752 вернёт ошибку; рабочий путь — Cloud timer + `cloud_run_popolnenie.py`. После копирования файлов в otchety на VAJRAPANI и push — Actions+cron-job становятся основным путём.
