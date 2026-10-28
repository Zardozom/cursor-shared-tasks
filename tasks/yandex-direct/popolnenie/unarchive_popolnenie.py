#!/usr/bin/env python3
"""Unarchive «Пополнение» campaigns that are ARCHIVED, then refresh the sheet.

Sets «Дата разархивации» = today (MSK) for campaigns successfully unarchived.
Use only when Ilya explicitly asks to unarchive.

API: campaigns.unarchive with CampaignIds.
"""
from __future__ import annotations

import os
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

# Reuse status module helpers
sys.path.insert(0, str(Path(__file__).resolve().parent))
import popolnenie_status as ps  # noqa: E402

from google.oauth2 import service_account
from googleapiclient.discovery import build

MSK = ZoneInfo("Europe/Moscow")
API = "https://api.direct.yandex.com/json/v5/campaigns"


def unarchive(login: str, token: str, campaign_id: str) -> str | None:
    """Return None on success, else error string."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Client-Login": login,
        "Accept-Language": "ru",
        "Content-Type": "application/json; charset=utf-8",
    }
    body = {"method": "unarchive", "params": {"SelectionCriteria": {"Ids": [int(campaign_id)]}}}
    last = None
    for use_ops in (False, True):
        h = dict(headers)
        if use_ops:
            h["Use-Operator-Units"] = "true"
        try:
            r = requests.post(API, headers=h, json=body, timeout=90)
        except requests.RequestException as e:
            last = f"net:{e}"
            continue
        if r.status_code != 200:
            last = f"http_{r.status_code}"
            continue
        data = r.json()
        if "error" in data:
            code = str(data["error"].get("error_code"))
            if code == "8000" and not use_ops:
                continue
            last = f"api_{code}:{data['error'].get('error_string')}"
            continue
        # result may include UnarchivedIds / errors per id
        result = data.get("result") or {}
        unarchived = [str(x) for x in (result.get("UnarchivedCampaignIds") or result.get("UnarchivedIds") or [])]
        if campaign_id in unarchived or not result.get("Errors"):
            # Some responses only return empty result on success
            if result.get("Errors"):
                last = f"partial:{result['Errors']}"
                continue
            return None
        last = f"not_in_result:{result}"
    return last or "failed"


def main() -> int:
    env = ps.load_env_files()
    tokens = ps.collect_tokens(env)
    if not tokens:
        print("No tokens", file=sys.stderr)
        return 1
    sa_path = env.get("GOOGLE_SERVICE_ACCOUNT_PATH") or str(
        Path.home() / ".config/google-sheets/service-account.json"
    )
    spreadsheet_id = env.get("GOOGLE_SHEETS_SPREADSHEET_ID") or ps.SPREADSHEET_ID
    creds = service_account.Credentials.from_service_account_file(
        sa_path, scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    svc = build("sheets", "v4", credentials=creds, cache_discovery=False)
    labels = ps.fetch_account_labels(svc, spreadsheet_id)
    prev = ps.read_unarchive_dates(svc, spreadsheet_id)
    today = datetime.now(MSK).strftime("%d.%m.%Y")

    rows: list[dict] = []
    errors: list[str] = []
    for login in sorted(tokens.keys()):
        cid, status, err = ps.campaigns_popolnenie(login, tokens[login])
        if err:
            errors.append(f"{login}:{err}")
            print(f"ERR {login} {err}")
            time.sleep(0.3)
            continue
        if not cid:
            time.sleep(0.2)
            continue
        label = labels.get(login) or login
        unarch_date = prev.get(cid, "")
        if status == "архивные":
            uerr = unarchive(login, tokens[login], cid)
            if uerr:
                errors.append(f"{login}:{cid}:{uerr}")
                print(f"UNARCHIVE_FAIL {label} {cid} {uerr}")
            else:
                status = "разархивированные"
                unarch_date = today
                print(f"UNARCHIVED {label} {cid} date={today}")
            time.sleep(0.5)
        elif status == "разархивированные" and not unarch_date:
            # already open, date unknown unless set earlier — leave blank
            pass
        rows.append(
            {
                "label": label,
                "campaign_id": cid,
                "status": status or "разархивированные",
                "unarchive_date": unarch_date if status == "разархивированные" else "",
            }
        )
        time.sleep(0.25)

    ps.write_sheet(svc, spreadsheet_id, rows, today)
    print(f"Done rows={len(rows)} errors={len(errors)}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
