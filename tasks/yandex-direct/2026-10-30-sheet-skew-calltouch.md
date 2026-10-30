# Slim sheets: перекос форматирования + Колтач Direct (2026-10-30)

## Live sheet
https://docs.google.com/spreadsheets/d/1gsjP650gW75Rc7eYwimRm578AzOX_V1Xh57r3cgrNSI/edit

## Что починили на листах
- **АВС**: восстановлены 4 недели (были только B); сводка видна; кампании внизу `"аккаунт" "кампания"`; у МК1 появились РК (где был spend); бирюза только на шапках.
- **Все slim** (Дубровка, Алтуфьево, Вольво, АВС, Акцент, Тимьян, Арбалеты, Игры Блоки): `apply_formatting` — цвета только на шапках периодов/аккаунтов/кампаний; скрытые строки в диапазоне развёрнуты; история недель не затиралась (кроме АВС, где уже была 1 колонка — пересобрана из Direct).
- **Колтач / CPA**: backfill Direct-only + fill CPA после правки фильтра.

## Дубровка · Лиды Колтач
| Неделя | До (лиды / unique) | После (лиды / unique) |
|---|---|---|
| 19.10–25.10 | 3 / 0 | **78 / 44** |
| 12.10–18.10 | 0 / 0 | **104 / 50** |
| 05.10–11.10 | 0 / 0 | **85 / 54** |
| 28.09–04.10 | 0 / 0 | **90 / 53** |

Стоимость достижения Колтач: было «—» везде → ~3,9–4,6 тыс. ₽ (spend / unique).

Sample канала: `source/utmSource=eLama-yandex`, `medium=cpc`, `yandexDirect=null` — раньше строгий фильтр это отбрасывал.

## PRs (otchety)
- https://github.com/Zardozom/yandex-direct-otchety/pull/5 — кампании внизу + Direct-only
- https://github.com/Zardozom/yandex-direct-otchety/pull/6 — formatting skew + unique/eLama fallback (`cursor/fix-skew-calltouch-c586`)

## Зависший агент
`bc-057d3b20` — без ветки/PR; работа продолжена отдельно в облаке.
