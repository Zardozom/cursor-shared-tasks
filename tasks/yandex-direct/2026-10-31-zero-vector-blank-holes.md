# Zero-vector blank holes (slim sheets) — 2026-10-31

Sheet: `1gsjP650gW75Rc7eYwimRm578AzOX_V1Xh57r3cgrNSI`  
Follow-up to fill-empty MK2 / CampaignId match (PR #10).

## Problem

Previous backfill left **blank** core cells when Direct `cost=0` for a campaign week.
Calltouch Unique/CPA were already `0` / `—`, so the user still saw «дыры» (ABC MK2 screenshot:
`BezFraz — 2`, `Zayavka`).

## Live sheet fix

Filled every campaign/account core blank under a non-empty period header on all slim tabs.

| Tab | Blank week-holes closed (approx cells written) |
|---|---|
| АВС | 23 holes → **0**; ~83 cells (MK2 Direct-aware) |
| Тойота Дубровка | ~117 cells |
| Тойота Алтуфьево | ~366 cells |
| Вольво | ~40 cells |
| Акцент | 0 |
| Тимьян | ~98 cells |
| Арбалеты | ~175 cells |
| Игры Блоки | ~1453 cells |
| **Total** | **~2332 cells** (pass1 2113 + pass2 219) |

Post-check: **0** remaining blank core cells under period headers on all 8 slim tabs.

### MK2 e-17327077 before → after

Exact names kept separate (`BezFraz — 2` ≠ `BezFraz-4601`).

**`"МК 2" "MK2-ABC-200-4100-All-BezFraz — 2"`** (CampaignId `713589752` fingerprint):

| Week | Before | After (Direct) |
|---|---|---|
| 19.10–25.10 | blank core | `0,00 ₽` / 448 / 23 / `—` / 0 / `—` |
| 12.10–18.10 | 5 613,22 ₽ / 862 / 42 | unchanged |
| 05.10–11.10 | blank core | `0,00 ₽` / 326 / 10 / `—` / 0 / `—` |
| 28.09–04.10 | 16 839,66 ₽ / 2985 / 137 | unchanged |

**`"МК 2" "MK2-ABC-200-4000-Zayavka"`**:

| Week | Before | After |
|---|---|---|
| 19.10 + 12.10 | blank core | `0,00 ₽` + real impressions/clicks from Direct |
| 05.10 + 28.09 | spend present | unchanged |

## Otchety code

PR: https://github.com/Zardozom/yandex-direct-otchety/pull/11  
Branch `cursor/zero-vector-no-blank-2288` ← base PR #10 (`cursor/campaignid-exact-match-cb64`).

- `normalize` / `backfill_campaign_blocks`: keep campaigns with impressions/clicks/conversions even at cost=0; CPC/CPA → `—`.
- `sheets_writer`: `core_zero_value`, `fill_blank_core_in_values`, `ensure_period_core_filled`; append fills sibling period columns; rebuild pads blanks.
- Tests: `ZeroVectorNoBlankTests` in `tests/test_slim_goals.py`.

## Rule going forward

If the week header is non-empty, the core vector is never blank: either Direct numbers or `0,00 ₽` / `0` / `0` / `—` / `0` / `—`.
