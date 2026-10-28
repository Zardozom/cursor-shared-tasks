#!/usr/bin/env python3
"""Weekly status of Direct campaigns named «Пополнение» → Google Sheet tab Пополнение.

Runs Sunday 19:00 MSK (1h before weekly-reports). Secrets via .env from Actions.

Columns: Аккаунт | Номер кампании | Статус | Дата проверки | Дата разархивации
«Дата разархивации» заполняется при разархивации агентом по команде и сохраняется
между еженедельными проверками; для архивных — пусто.
"""
from __future__ import annotations

import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build

SPREADSHEET_ID = os.environ.get(
    "GOOGLE_SHEETS_SPREADSHEET_ID",
    "1gsjP650gW75Rc7eYwimRm578AzOX_V1Xh57r3cgrNSI",
)
TAB = "Пополнение"
CAMPAIGN_NAME = "Пополнение"
API_CAMPAIGNS = "https://api.direct.yandex.com/json/v5/campaigns"
MSK = ZoneInfo("Europe/Moscow")
N_COLS = 5
HEADER = ["Аккаунт", "Номер кампании", "Статус", "Дата проверки", "Дата разархивации"]
COL_WIDTHS = [280, 140, 170, 130, 150]


def load_env_files() -> dict[str, str]:
    env: dict[str, str] = {}
    for path in [
        Path(".env"),
        Path(".env.clients"),
        Path(os.environ.get("GOOGLE_SERVICE_ACCOUNT_PATH", "")).parent.parent / ".env",
    ]:
        if not path or not Path(path).is_file():
            continue
        for line in Path(path).read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    for k, v in os.environ.items():
        if k.startswith("YANDEX_DIRECT_TOKEN") or k.startswith("GOOGLE_"):
            env.setdefault(k, v)
    return env


def collect_tokens(env: dict[str, str]) -> dict[str, str]:
    """login e-XXXX -> token."""
    tokens: dict[str, str] = {}
    for k, v in env.items():
        if not v or not v.startswith("y0"):
            continue
        m = re.match(r"^YANDEX_DIRECT_TOKEN_(e-\d+)$", k)
        if m:
            tokens[m.group(1)] = v
    return tokens


def fetch_account_labels(svc, spreadsheet_id: str) -> dict[str, str]:
    """login -> label from Балансы sheet when possible."""
    out: dict[str, str] = {}
    try:
        vals = (
            svc.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range="'Балансы'!A1:B80")
            .execute()
            .get("values", [])
        )
    except Exception:
        return out
    for row in vals:
        for cell in row:
            m = re.search(r"(.+?)\s*·\s*(e-\d+)", str(cell))
            if m:
                out[m.group(2)] = f"{m.group(1).strip()} · {m.group(2)}"
    return out


def read_unarchive_dates(svc, spreadsheet_id: str) -> dict[str, str]:
    """campaign_id -> дата разархивации (preserve across weekly refreshes)."""
    out: dict[str, str] = {}
    try:
        vals = (
            svc.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=f"'{TAB}'!A1:E200")
            .execute()
            .get("values", [])
        )
    except Exception:
        return out
    if len(vals) < 3:
        return out
    header = vals[2] if len(vals) > 2 else []
    # Prefer named column; fallback: col E (index 4) or last col if 5 wide
    unarch_idx = None
    for i, name in enumerate(header):
        if "разархив" in str(name).lower():
            unarch_idx = i
            break
    if unarch_idx is None and len(header) >= 5:
        unarch_idx = 4
    if unarch_idx is None:
        return out
    for row in vals[3:]:
        if len(row) < 2:
            continue
        cid = str(row[1]).strip()
        if not cid.isdigit():
            continue
        date = row[unarch_idx].strip() if len(row) > unarch_idx else ""
        if date:
            out[cid] = date
    return out


def campaigns_popolnenie(login: str, token: str) -> tuple[str | None, str | None, str | None]:
    """Return (campaign_id, status_ru, error)."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Client-Login": login,
        "Accept-Language": "ru",
        "Content-Type": "application/json; charset=utf-8",
    }
    body = {
        "method": "get",
        "params": {
            "SelectionCriteria": {},
            "FieldNames": ["Id", "Name", "State", "Status"],
        },
    }
    last_err = None
    for use_ops in (False, True):
        h = dict(headers)
        if use_ops:
            h["Use-Operator-Units"] = "true"
        try:
            r = requests.post(API_CAMPAIGNS, headers=h, json=body, timeout=90)
        except requests.RequestException as e:
            last_err = f"net:{e}"
            continue
        if r.status_code != 200:
            last_err = f"http_{r.status_code}"
            continue
        data = r.json()
        if "error" in data:
            code = str(data["error"].get("error_code"))
            if code == "8000" and not use_ops:
                continue
            last_err = f"api_{code}"
            continue
        camps = data.get("result", {}).get("Campaigns") or []
        hits = [c for c in camps if (c.get("Name") or "").strip() == CAMPAIGN_NAME]
        if not hits:
            hits = [c for c in camps if CAMPAIGN_NAME in (c.get("Name") or "")]
        if not hits:
            return None, None, None
        c = hits[0]
        state = (c.get("State") or "").upper()
        status_ru = "архивные" if state == "ARCHIVED" else "разархивированные"
        return str(c["Id"]), status_ru, None
    return None, None, last_err or "failed"


def rgb(h: str) -> dict:
    h = h.lstrip("#")
    return {"red": int(h[0:2], 16) / 255, "green": int(h[2:4], 16) / 255, "blue": int(h[4:6], 16) / 255}


def write_sheet(svc, spreadsheet_id: str, rows: list[dict], check_date: str) -> None:
    meta = svc.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheet_id = None
    for s in meta["sheets"]:
        if s["properties"]["title"] == TAB:
            sheet_id = s["properties"]["sheetId"]
            break
    if sheet_id is None:
        resp = (
            svc.spreadsheets()
            .batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={"requests": [{"addSheet": {"properties": {"title": TAB}}}]},
            )
            .execute()
        )
        sheet_id = resp["replies"][0]["addSheet"]["properties"]["sheetId"]

    order = {"архивные": 0, "разархивированные": 1}
    rows = sorted(rows, key=lambda x: (order.get(x["status"], 9), x["label"].lower()))
    n_arch = sum(1 for r in rows if r["status"] == "архивные")
    n_open = sum(1 for r in rows if r["status"] == "разархивированные")

    title = "Пополнение"
    subtitle = (
        f"Кампании «Пополнение» · архивных {n_arch} · разархивированных {n_open} · проверка {check_date}"
    )
    values = [[title] + [""] * (N_COLS - 1), [subtitle] + [""] * (N_COLS - 1), HEADER]
    for r in rows:
        unarch = r.get("unarchive_date") or ""
        if r["status"] == "архивные":
            unarch = ""
        values.append([r["label"], r["campaign_id"], r["status"], check_date, unarch])

    try:
        svc.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "requests": [
                    {
                        "unmergeCells": {
                            "range": {
                                "sheetId": sheet_id,
                                "startRowIndex": 0,
                                "endRowIndex": 5,
                                "startColumnIndex": 0,
                                "endColumnIndex": N_COLS,
                            }
                        }
                    }
                ]
            },
        ).execute()
    except Exception:
        pass

    svc.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=f"'{TAB}'!A1:Z200").execute()
    svc.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{TAB}'!A1",
        valueInputOption="USER_ENTERED",
        body={"values": values},
    ).execute()

    last = 3 + len(rows)
    reqs = []
    reqs.append(
        {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sheet_id,
                    "gridProperties": {
                        "rowCount": max(last + 5, 20),
                        "columnCount": N_COLS,
                        "frozenRowCount": 3,
                    },
                    "tabColorStyle": {"rgbColor": rgb("059669")},
                },
                "fields": "gridProperties.rowCount,gridProperties.columnCount,gridProperties.frozenRowCount,tabColorStyle",
            }
        }
    )
    for i, w in enumerate(COL_WIDTHS):
        reqs.append(
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": i,
                        "endIndex": i + 1,
                    },
                    "properties": {"pixelSize": w},
                    "fields": "pixelSize",
                }
            }
        )
    for start, end in ((0, 1), (1, 2)):
        reqs.append(
            {
                "mergeCells": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": start,
                        "endRowIndex": end,
                        "startColumnIndex": 0,
                        "endColumnIndex": N_COLS,
                    },
                    "mergeType": "MERGE_ALL",
                }
            }
        )
    reqs.append(
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": N_COLS,
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": rgb("1F2937"),
                        "textFormat": {
                            "foregroundColor": rgb("FFFFFF"),
                            "fontSize": 14,
                            "bold": True,
                            "fontFamily": "Arial",
                        },
                        "verticalAlignment": "MIDDLE",
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,verticalAlignment)",
            }
        }
    )
    reqs.append(
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": 2,
                    "startColumnIndex": 0,
                    "endColumnIndex": N_COLS,
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": rgb("F3F4F6"),
                        "textFormat": {
                            "foregroundColor": rgb("4B5563"),
                            "fontSize": 10,
                            "fontFamily": "Arial",
                        },
                        "verticalAlignment": "MIDDLE",
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,verticalAlignment)",
            }
        }
    )
    reqs.append(
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 2,
                    "endRowIndex": 3,
                    "startColumnIndex": 0,
                    "endColumnIndex": N_COLS,
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": rgb("374151"),
                        "textFormat": {
                            "foregroundColor": rgb("FFFFFF"),
                            "fontSize": 10,
                            "bold": True,
                            "fontFamily": "Arial",
                        },
                        "verticalAlignment": "MIDDLE",
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,verticalAlignment)",
            }
        }
    )
    if rows:
        reqs.append(
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 3,
                        "endRowIndex": last,
                        "startColumnIndex": 0,
                        "endColumnIndex": N_COLS,
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "textFormat": {
                                "fontSize": 10,
                                "fontFamily": "Arial",
                                "foregroundColor": rgb("111827"),
                            },
                            "verticalAlignment": "MIDDLE",
                            "borders": {
                                "top": {"style": "SOLID", "color": rgb("E5E7EB")},
                                "bottom": {"style": "SOLID", "color": rgb("E5E7EB")},
                                "left": {"style": "SOLID", "color": rgb("E5E7EB")},
                                "right": {"style": "SOLID", "color": rgb("E5E7EB")},
                            },
                        }
                    },
                    "fields": "userEnteredFormat(textFormat,verticalAlignment,borders)",
                }
            }
        )
    for i, row in enumerate(rows):
        r = 3 + i
        bg = rgb("FFFFFF") if i % 2 == 0 else rgb("F9FAFB")
        reqs.append(
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": r,
                        "endRowIndex": r + 1,
                        "startColumnIndex": 0,
                        "endColumnIndex": N_COLS,
                    },
                    "cell": {"userEnteredFormat": {"backgroundColor": bg}},
                    "fields": "userEnteredFormat.backgroundColor",
                }
            }
        )
        for col in (1, 3, 4):
            reqs.append(
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": r,
                            "endRowIndex": r + 1,
                            "startColumnIndex": col,
                            "endColumnIndex": col + 1,
                        },
                        "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
                        "fields": "userEnteredFormat.horizontalAlignment",
                    }
                }
            )
        if row["status"] == "архивные":
            sbg, sfg = rgb("E5E7EB"), rgb("4B5563")
        else:
            sbg, sfg = rgb("D1FAE5"), rgb("065F46")
        reqs.append(
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": r,
                        "endRowIndex": r + 1,
                        "startColumnIndex": 2,
                        "endColumnIndex": 3,
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": sbg,
                            "textFormat": {
                                "foregroundColor": sfg,
                                "bold": True,
                                "fontSize": 10,
                                "fontFamily": "Arial",
                            },
                            "horizontalAlignment": "CENTER",
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)",
                }
            }
        )
    reqs.append(
        {
            "setBasicFilter": {
                "filter": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 2,
                        "endRowIndex": max(last, 3),
                        "startColumnIndex": 0,
                        "endColumnIndex": N_COLS,
                    }
                }
            }
        }
    )
    svc.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={"requests": reqs}).execute()


def main() -> int:
    env = load_env_files()
    tokens = collect_tokens(env)
    if not tokens:
        print("No YANDEX_DIRECT_TOKEN_e-* tokens found", file=sys.stderr)
        return 1

    sa_path = env.get("GOOGLE_SERVICE_ACCOUNT_PATH") or str(
        Path.home() / ".config/google-sheets/service-account.json"
    )
    if not Path(sa_path).is_file():
        print(f"Missing SA JSON at {sa_path}", file=sys.stderr)
        return 1

    spreadsheet_id = env.get("GOOGLE_SHEETS_SPREADSHEET_ID") or SPREADSHEET_ID
    creds = service_account.Credentials.from_service_account_file(
        sa_path, scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    svc = build("sheets", "v4", credentials=creds, cache_discovery=False)
    labels = fetch_account_labels(svc, spreadsheet_id)
    prev_unarch = read_unarchive_dates(svc, spreadsheet_id)

    check_date = datetime.now(MSK).strftime("%d.%m.%Y")
    rows: list[dict] = []
    errors: list[str] = []
    for login in sorted(tokens.keys()):
        cid, status, err = campaigns_popolnenie(login, tokens[login])
        if err:
            errors.append(f"{login}:{err}")
            print(f"ERR {login} {err}")
            time.sleep(0.3)
            continue
        if not cid:
            print(f"SKIP {login} no Пополнение")
            time.sleep(0.3)
            continue
        label = labels.get(login) or login
        status = status or "разархивированные"
        unarch = prev_unarch.get(cid, "") if status == "разархивированные" else ""
        rows.append(
            {
                "label": label,
                "campaign_id": cid,
                "status": status,
                "unarchive_date": unarch,
            }
        )
        print(f"OK {label} {cid} {status} unarch={unarch or '-'}")
        time.sleep(0.35)

    write_sheet(svc, spreadsheet_id, rows, check_date)
    print(f"Wrote {len(rows)} rows to tab {TAB}; errors={len(errors)}")
    return 0 if rows else (1 if errors else 0)


if __name__ == "__main__":
    raise SystemExit(main())
