# Calltouch: канал Яндекс.Директ = `cpc` (UI)

Дата: 2026-10-30. Сайт-референс: toyota-altufevo.ru (`site_id=50195`), период 19–25.10.2026, attribution UI «Последний непрямой», фильтр Channel/utm_medium=`cpc`, source=все.

## Расхождение API vs UI

Старый `is_yandex_direct_channel` в `yandex-direct-otchety` требовал exact source ∈ {yandex, ya.ru, яндекс} ∧ cpc (плюс склейка `yandexDirect`). На Алтуфьево source почти всегда `eLama-yandex` → после Direct-only backfill было ~1 лид / unique 0.

| # | Фильтр (Алтуфьево 19–25.10, calls journal) | leads | unique |
|---|---|---:|---:|
| (a) medium или utmMedium == cpc | 67 | 26 |
| (b) старый is_yandex_direct_channel | 1 | 0 |
| (c) utmMedium == cpc | 67 | 26 |
| (d) source/utmSource содержит yandex/eLama | 179 | 52 |

Дубровка (`50199`) за тот же период: (a) 78 / 44; (b) 3 / 0.

Sample cpc-лида: `source=eLama-yandex`, `medium=cpc`, `utmSource=eLama-yandex`, `utmMedium=cpc`, `channel` отсутствует; `yandexDirect` чаще `null` (склейка ID редкая).

### Attribution

В журнале у всех записей периода `attribution=1`. Параметр API `attribution=1` принимается; значения `2`/`3`/`lastNonDirect` → HTTP 500. Для Channel=cpc counts совпадают с UI без отдельной модели — журнал уже отдаёт нужную атрибуцию аккаунта.

## Фикс

Ветка otchety: `cursor/calltouch-cpc-channel-b00d` → PR https://github.com/Zardozom/yandex-direct-otchety/pull/7  
base: `cursor/campaign-bottom-direct-leads-be68` (PR #5 Direct-only + кампании внизу).

`is_yandex_direct_channel` = `medium == "cpc" or utmMedium == "cpc"` (как UI Channel, source=все).

## Sheet после rewrite

Spreadsheet `1gsjP650gW75Rc7eYwimRm578AzOX_V1Xh57r3cgrNSI`. Прогон: `calltouch_backfill.py --rewrite-all-leads` по всем 6 calltouch-листам + пересчёт «Стоимость достижения Колтач».

| Лист | 19–25.10 Лиды | Уникальные | CPA Колтач (сводная) |
|---|---:|---:|---|
| Тойота Алтуфьево | 67 | 26 | 2 113,96 ₽ |
| Тойота Дубровка | 78 | 44 | 3 958,87 ₽ |
| Вольво | 7 | 3 | (пересчитан) |
| АВС | 14 | 8 | (пересчитан) |
| Акцент | 11 | 9 | (пересчитан) |
| Тимьян | 6 | 3 | (пересчитан) |

Проверка CPA Алтуфьево: 54 962,99 / 26 ≈ 2 113,96.
