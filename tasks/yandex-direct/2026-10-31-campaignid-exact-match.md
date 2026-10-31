# Otchety: CampaignId / exact-name match (no stem) — 2026-10-31

Follow-up to [Fill empty campaign week cells](https://cursor.com/agents/bc-bb4909cd-dd28-5045-86cf-e426fef2f2b6).

## PR
https://github.com/Zardozom/yandex-direct-otchety/pull/10  
Branch `cursor/campaignid-exact-match-cb64` ← base PR #9 (`cursor/swap-calltouch-unique-cpa-d0d8`).

## Fix
- Calltouch match: **CampaignId** then **exact** `norm(utmCampaign↔name)` only. Stem/CopyN removed (BezFraz — 2 ≠ BezFraz-4601).
- Campaign header: `"аккаунт" "кампания" · id` (legacy without id still equivalent by exact name).
- Upsert rebuilds the whole metric vector so a second Показы/Клики band cannot accumulate.
- Regression: `test_bezfraz_shared_stem_campaigns_stay_separate`, `test_bezfraz_headers_not_equivalent_and_dup_band_collapsed`.

## Live ABC
Verified after code-only change: separate BezFraz — 2 / BezFraz-4601 (/ 4601 — 2) blocks; no duplicate bands; no spent>0 empty core holes. Sheet repair from fill-empty agent left intact.
