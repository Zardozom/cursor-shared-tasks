# Пополнение — еженедельный статус

## Расписание (МСК, без DST)

| Что | Когда | Где |
|---|---|---|
| **Пополнение статус** | вс **19:00** | GitHub Actions `popolnenie-status.yml` cron `0 16 * * 0` UTC + cron-job.org job **8739752** «Пополнение статус» |
| Воскресный отчёт | вс **20:00** | `weekly-reports.yml` cron `0 17 * * 0` UTC + cron-job.org **8680907** |

Пополнение специально на **час раньше** отчёта.

## Файлы в репо `Zardozom/yandex-direct-otchety`

Уже в `main` (`scripts/popolnenie_status.py`, `.github/workflows/popolnenie-status.yml`). Drive-зеркало и handoff-копии в этом репо — для синхронизации ноутбуков.

## Колонки листа

Аккаунт | Номер кампании | Статус | Дата проверки | **Дата разархивации**

Дата разархивации — только для разархивированных.

**Воскресная проверка:** если кампания архивная — автоматически разархивировать и проставить сегодняшнюю дату (МСК). Уже открытые — дату сохранять. `AUTO_UNARCHIVE=0` отключает.

## Cloud / Actions

```bash
python tasks/yandex-direct/popolnenie/cloud_run_popolnenie.py
# то же + явный алиас авто-разархивации:
python tasks/yandex-direct/popolnenie/unarchive_popolnenie.py
```

Нужны SA `~/.config/google-sheets/service-account.json` и `/tmp/direct-secrets/.env` (скачать с Drive по playbook).
