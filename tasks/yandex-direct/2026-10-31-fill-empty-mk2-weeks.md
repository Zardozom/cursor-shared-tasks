# Fill empty campaign week cells (ABC MK2) — 2026-10-31

Sheet: `1gsjP650gW75Rc7eYwimRm578AzOX_V1Xh57r3cgrNSI`  
Agent: Fill empty campaign week cells  
Parallel: [Swap Calltouch CPA/unique](https://cursor.com/agents/bc-c1ec0ed8-ffd3-5ea2-8494-cab94cf5d0d8) (sheet already post-swap Unique→CPA on account/campaign blocks).

## Root cause

Bottom-campaign / `MATCH_EXISTING` / section-align backfill (otchety PR #5–#8) matched **fuzzy campaign stems** and wrote into the wrong block:

- `MK2-ABC-200-4100-All-BezFraz — 2` absorbed metrics from `…-BezFraz-4601` (and vice versa).
- Result: **duplicate metric bands** in one block, `Потрачено` mid-block, week headers polluted into the campaign title row, and red-box “holes” (spent in one band, shows/clicks in another).
- Plain `BezFraz-4601` (no `— 2`) had **no own block**; its Direct weeks lived only inside the corrupted block.

## Diagnosis (slim tabs)

| Tab | Core holes (spent>0, empty Показы/Клики/CPC) | Split/dup blocks | Calltouch order |
|---|---|---|---|
| АВС | **2 misaligned weeks** on BezFraz — 2 → **0 after** | 1 → **0** | Unique→CPA (14) |
| Others | 0 real core holes | Dubrovka “Звонки и заявки” = goal label false-positive | Mostly Unique→CPA; site summary keeps CPA / Лиды / Unique |

“Стоимость достижения = —” with conversions 0 is **not** a hole.

## Fix applied (live sheet)

1. Rebuilt `"МК 2" "MK2-ABC-200-4100-All-BezFraz — 2"` from Direct `CAMPAIGN_PERFORMANCE_REPORT` (cost>0), canonical rows:  
   Потрачено → Показы → Клики → CPC → Конверсии → Стоимость достижения → **Уникальные Лиды Колтач** → **Стоимость достижения Колтач**.
2. Deleted 5 surplus duplicate rows.
3. **Inserted** missing `"МК 2" "MK2-ABC-200-4100-All-BezFraz-4601"` from Direct.
4. Re-aligned other MK2 campaigns on ABC to Direct (impressions/clicks/cost/CPA).
5. Preserved Calltouch unique where attributable; recomputed Calltouch CPA = spent/unique.
6. Did **not** overwrite valid history on unrelated cabinets.

## MK2 BezFraz — 2 before → after

**Before (rows 69–82):** Показы… first; `Потрачено` mid-block; weeks 19.10 / 05.10 held **4601** spend with empty cells in the upper band.

**After (rows 69–77):**

| Week | Потрачено | Показы | Клики | Conv |
|---|---|---|---|---|
| 19.10–25.10 | (empty) | | | |
| 12.10–18.10 | 5 613,22 ₽ | 862 | 42 | 1 |
| 05.10–11.10 | (empty) | | | |
| 28.09–04.10 | 16 839,66 ₽ | 2985 | 137 | 2 |

New block `BezFraz-4601`: 5 613,34 / 22 453,37 / 5 613,34 ₽ on the three Direct weeks.

## Pipeline follow-up (otchety)

Private repo `Zardozom/yandex-direct-otchety` not writable from this Cloud token. Recommended code fix on next otchety PR:

- Match campaigns by **CampaignId** (or exact name including `\xa0—\xa0N`), never by stem without suffix.
- When upserting a bottom block, **replace the whole metric vector** for that week; do not append a second Показы/Клики band.
- Clear week labels from campaign header row (weeks only in row 1).

## Artifacts

- `/opt/cursor/artifacts/mk2_before.json`, `mk2_after.json`
- `/opt/cursor/artifacts/slim_diag.json` (before), `slim_diag_after.json`
- `/opt/cursor/artifacts/mk2_direct_full.json`
