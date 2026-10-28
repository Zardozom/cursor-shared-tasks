# Пополнение — добить на ORION

## Что уже готово
- Лист Пополнение: 12 кампаний, 0 архивных, у 5 дата разархивации 28.10.2026
- Воскресенье 19:00 МСК: проверка + авто-разархивация + дата; 20:00 — отчёт
- cron-job.org **8739752** «Пополнение статус» (ждёт workflow в otchety)
- Cloud timer + скрипты в `tasks/yandex-direct/popolnenie/`
- Файлы уже в Drive-зеркале otchety:
  - `scripts/popolnenie_status.py`
  - `.github/workflows/popolnenie-status.yml`
  - `scripts/commit_popolnenie_to_github.ps1`

## Что осталось (блокер)
Cloud PAT без **Contents: Write** на `Zardozom/yandex-direct-otchety` → нельзя запушить workflow.

## На ORION — один из путей

### A (предпочтительно для Cloud)
1. Войти в GitHub как Zardozom
2. https://github.com/settings/tokens?type=beta
3. Токен для otchety → Repository permissions → **Contents = Read and write** → Save
4. Написать агенту «готово» (или вставить PAT в секрет `GH_PAT_OTCHETY`)
5. Агент сам: push `popolnenie-status.yml` + `scripts/popolnenie_status.py` в `main`

### B (без настроек токена, с диска)
```powershell
cd D:\GolgleDrive\Cursor\yandex-direct-otchety
powershell -File scripts\commit_popolnenie_to_github.ps1
```
(Путь на ORION может быть через Яндекс.Диск — сверить hostname; зеркало Drive то же.)

## Проверка после push
- В Actions otchety есть workflow «Пополнение campaign status»
- Ручной `workflow_dispatch` или ждать вс 19:00 МСК
- cron-job 8739752 перестаёт 404/fail на dispatch

PR handoff: https://github.com/Zardozom/cursor-shared-tasks/pull/4  
Playbook: `tasks/yandex-direct-sheets-playbook.md` §C
