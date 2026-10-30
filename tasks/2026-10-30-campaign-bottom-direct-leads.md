# Кампании внизу + Колтач только Direct (2026-10-30)

## Код

Репо: `Zardozom/yandex-direct-otchety`  
Ветка: `cursor/campaign-bottom-direct-leads-be68` (поверх `cursor/campaign-section-align` @ `75cbe74`)  
PR: https://github.com/Zardozom/yandex-direct-otchety/pull/5

Коммиты:
- `1e2c674` — Move campaign blocks below accounts; Calltouch leads Direct-only
- `e43828c` — Add Sheets API 429 backoff for read quota

### Поведение короткого листа
1. **Сводная** → **Лиды Колтач** / **Уникальные Лиды Колтач** (только Яндекс.Директ) → аккаунты **без** вложенных `РК id · имя`.
2. Внизу под всеми аккаунтами: `"аккаунт" "кампания"` + метрики 1:1.
3. Цвета шапок: периоды (teal) / аккаунты (navy) / кампании (amber).
4. `lead_counts`: `withYandexDirect=true` + `is_yandex_direct_channel`.

### Backfill
```bash
uv run python scripts/backfill_campaign_blocks.py --latest-only --tabs "…"
uv run python scripts/backfill_campaign_blocks.py --tabs "…"   # все периоды, MATCH_EXISTING
gh workflow run "Calltouch leads backfill" -R Zardozom/yandex-direct-otchety \
  --ref cursor/campaign-bottom-direct-leads-be68 \
  -f rewrite_all_leads=true \
  -f tabs="АВС,Акцент,Тимьян,Тойота Дубровка,Тойота Алтуфьево,Вольво"
```

Квота Sheets ~60 read/min — в коде backoff на 429; между вкладками пауза ~55–90с.

## Live (Cloud 2026-10-30)

Таблица: `1gsjP650gW75Rc7eYwimRm578AzOX_V1Xh57r3cgrNSI`

### До (latest B1 = 19.10.26 – 25.10.26)
| Лист | nested RK | Лиды / Уник |
|---|---|---|
| АВС | 4 | 20 / 10 |
| Акцент | 1 | 13 / 11 |
| Тимьян | 4 | 82 / 40 |
| Тойота Дубровка | 0 | 202 / 100 |
| Тойота Алтуфьево | 9 | 189 / 57 |
| Вольво | 3 | 24 / 11 |
| Арбалеты / Игры Блоки | 0 | (нет Колтач) |

### После latest-структуры
- nested `РК` сняты на обработанных листах; кампании внизу в кавычках.
- АВС: `"Классика" "Week-Poisk"` spend ≠ соседних РК (разные суммы).
- **Хвост:** на листе АВС нет блока `МК 2 · e-17327077` (skip missing block) — был и до прогона.

### Calltouch rewrite
Workflow run на ветке фичи (Direct-only код). Сверить лиды до/после: Direct ≤ all-site.

## Проверка глазами
Сводная → Колтач → аккаунты без вложенных РК → внизу `"Классика" "Week-Poisk"` с разными spend → Direct-лиды ≤ старых → CPA пересчитан.
