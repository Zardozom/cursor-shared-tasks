# Slim formatting fix (campaign amber + no PERIOD teal tail) — 2026-10-31

Sheet: `1gsjP650gW75Rc7eYwimRm578AzOX_V1Xh57r3cgrNSI`  
Follow-up to zero-vector / CampaignId (otchety PR #10–#11).

## Why formatting broke

1. **White campaign headers** (e.g. ABC r87 `"МК 2" "…BezFraz-4601"`): rows inserted/rebuilt by fill/backfill/zero-fill without a fresh `apply_formatting`, so col A stayed metric BG. Recognition of `"аккаунт" "кампания" · id` also needed quote/NBSP/`·` normalization.
2. **Teal tail F–G**: `ncols = max(len(row))` / prior wide paints put `PERIOD_HEADER_BG` past real weeks; later reformats only reset A–E (`ncols=5`), so F+ teal never cleared. Campaign header rows also got teal on B+ instead of amber across the week width.

## Otchety PR

https://github.com/Zardozom/yandex-direct-otchety/pull/12  
Branch `cursor/fix-headers-period-width-5d63` ← base PR #11 (`cursor/zero-vector-no-blank-2288`).

- `_normalize_header_label` + hardened `_is_campaign_header`
- `_format_ncols` from row0 period labels; clear cols beyond weeks
- PERIOD teal **only** on row0 period cells; campaign/account/summary = full week-width colors
- `ensure_period_core_filled(..., reformat=True)` by default
- `scripts/reformat_slim_tabs.py` (slim only; skip Балансы/Пополнение)

## Live verify (API colors)

| Tab | Campaign amber | Period teal B1… | Teal beyond E |
|---|---|---|---|
| АВС | 11/11 (incl. BezFraz-4601 + Zayavka) | 4/4 | 0 |
| Акцент | 1/1 | 4/4 | 0 |
| Тимьян | 8/8 | 4/4 | 0 |
| Вольво | 5/5 | 4/4 | 0 |
| Тойота Дубровка | 9/9 | 4/4 | 0 |

Also reformatted: Тойота Алтуфьево, Арбалеты, Игры Блоки. Real Volvo tab title is **`Вольво`** (not «Вольво Дубровка»).
