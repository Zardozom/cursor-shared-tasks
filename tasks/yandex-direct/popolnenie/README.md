# Пополнение — еженедельный статус

## Расписание (МСК, без DST)

| Что | Когда | Где |
|---|---|---|
| **Пополнение статус** | вс **19:00** | GitHub Actions `popolnenie-status.yml` cron `0 16 * * 0` UTC + cron-job.org job **8739752** «Пополнение статус» |
| Воскресный отчёт | вс **20:00** | `weekly-reports.yml` cron `0 17 * * 0` UTC + cron-job.org **8680907** |

Пополнение специально на **час раньше** отчёта.

## Файлы для репо `Zardozom/yandex-direct-otchety`

Скопировать и запушить в `main` (VAJRAPANI: `D:\GolgleDrivePK\Cursor\yandex-direct-otchety`):

- `scripts/popolnenie_status.py` ← `popolnenie_status.py`
- `.github/workflows/popolnenie-status.yml` ← `popolnenie-status.yml`

Drive (рядом с weekly-reports):
`popolnenie-status.yml` id `1lqh2rQew2EAhuvyaJ7iJzX0hT3cJxtKG`,
`popolnenie_status.py` id `1QUN-iaoArmt8rwU8C_7TAxsPnw7_tFff`.

## Cloud fallback (уже работает)

```bash
python tasks/yandex-direct/popolnenie/cloud_run_popolnenie.py
```

Нужны SA `~/.config/google-sheets/service-account.json` и `/tmp/direct-secrets/.env` (скачать с Drive по playbook).
