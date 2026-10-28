# Run once on VAJRAPANI after Google Drive syncs otchety.
# Pushes Пополнение workflow into origin/main so cron-job.org 8739752 works.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$root = 'D:\GolgleDrivePK\Cursor\yandex-direct-otchety'
Set-Location $root
if (-not (Test-Path 'scripts\popolnenie_status.py')) { throw 'scripts\popolnenie_status.py missing — wait for Drive sync' }
if (-not (Test-Path '.github\workflows\popolnenie-status.yml')) { throw '.github\workflows\popolnenie-status.yml missing — wait for Drive sync' }
git add scripts/popolnenie_status.py .github/workflows/popolnenie-status.yml
git status
git commit -m "Add Пополнение Sunday status workflow (19:00 MSK, auto-unarchive)"
git push origin main
Write-Host "OK: workflow on GitHub; cron-job.org 8739752 will dispatch Sundays 19:00 MSK"
