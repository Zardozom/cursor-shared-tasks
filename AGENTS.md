# Agent context

User: Ilya (Product manager). Works across two Windows laptops (ORION, VAJRAPANI) via Cursor Cloud Agents + this git repo.

Prefer task workflows: research, plan, execute. Keep durable notes in `tasks/` when useful.

Code changes should be committed and pushed so both laptops stay in sync via git.

**Default runtime: Cloud Agent.** Do not leave work on a local laptop — Ilya may power off at any time. Resume via https://cursor.com/agents.

## Яндекс Директ + Google Sheets

Канонический playbook (пути, fileId секретов без значений, пайплайны, как писать в таблицу):

→ `tasks/yandex-direct-sheets-playbook.md`

Кратко: писать в таблицу «Отчеты! Яндекс Директ» через **Sheets API + SA `cursor-sheets@…`**, не через Drive MCP. SA JSON и `.env` Директа — на Google Drive (fileId в playbook).
