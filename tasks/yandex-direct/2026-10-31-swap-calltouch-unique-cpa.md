# Swap Calltouch tails: Unique → CPA

Дата: 2026-10-31.

## Запрос

Во всех блоках (сводка/аккаунт/кампания) поменять местами:
- «Стоимость достижения Колтач»
- «Уникальные Лиды Колтач»

После PR #8 было: CPA, затем Unique внизу. Нужен swap.

## Итоговый порядок (сверху → низ)

В **аккаунте и кампании**:

1. … метрики Direct …
2. **Уникальные Лиды Колтач**
3. **Стоимость достижения Колтач** ← последняя

В **сводке**: CPA остаётся последней метрикой сводки; сайт-пара «Лиды Колтач» → «Уникальные Лиды Колтач» сразу после сводки (как раньше). У сводки нет блокового Unique — CPA считает сайт-unique.

Арбалеты / Игры Блоки: только CPA, без Unique — не трогались.

## Код

Репо `Zardozom/yandex-direct-otchety`, ветка `cursor/swap-calltouch-unique-cpa-d0d8` (поверх PR #8).

- `_slim_metric_pairs` — Unique, затем CPA
- `_section_missing_tails` / `_block_tails_need_purge` / `ensure_block_calltouch_tails` — тот же порядок; старый хвост CPA→Unique снимается и вставляется заново
- тесты `test_slim_goals`, `test_calltouch_leads`

## PR / live

- Otchety: https://github.com/Zardozom/yandex-direct-otchety/pull/9 (base = PR #8)
- Backfill: 6 Calltouch-листов (Дубровка, Алтуфьево, Вольво, АВС, Акцент, Тимьян)
- Проверка: Алтуфьево Классика `Unique=10` → `CPA=858,57 ₽`; Акцент account/campaign Unique→CPA

