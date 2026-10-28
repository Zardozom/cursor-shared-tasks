#!/usr/bin/env python3
"""Cloud Agent entrypoint: refresh «Пополнение» sheet.

Expects (already typical for this Cloud env):
  SA:  ~/.config/google-sheets/service-account.json
  .env: /tmp/direct-secrets/.env  (or set DIRECT_ENV_PATH)

Delegates to popolnenie_status.py after preparing env files.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "popolnenie_status.py"
SA_DEFAULT = Path.home() / ".config/google-sheets/service-account.json"
ENV_DEFAULT = Path("/tmp/direct-secrets/.env")


def main() -> int:
    sa = Path(os.environ.get("GOOGLE_SERVICE_ACCOUNT_PATH") or SA_DEFAULT)
    env_src = Path(os.environ.get("DIRECT_ENV_PATH") or ENV_DEFAULT)
    if not sa.is_file():
        print(f"Missing SA at {sa}", file=sys.stderr)
        return 1
    if not env_src.is_file():
        print(f"Missing .env at {env_src}", file=sys.stderr)
        return 1
    if not SCRIPT.is_file():
        print(f"Missing {SCRIPT}", file=sys.stderr)
        return 1

    work = Path("/tmp/popolnenie-run")
    work.mkdir(parents=True, exist_ok=True)
    shutil.copy2(env_src, work / ".env")
    # Ensure path vars for the child script
    text = (work / ".env").read_text(encoding="utf-8", errors="ignore")
    lines = [
        ln
        for ln in text.splitlines()
        if not ln.startswith("GOOGLE_SERVICE_ACCOUNT_PATH=")
        and not ln.startswith("GOOGLE_SHEETS_SPREADSHEET_ID=")
    ]
    lines.append(f"GOOGLE_SERVICE_ACCOUNT_PATH={sa}")
    lines.append("GOOGLE_SHEETS_SPREADSHEET_ID=1gsjP650gW75Rc7eYwimRm578AzOX_V1Xh57r3cgrNSI")
    (work / ".env").write_text("\n".join(lines) + "\n", encoding="utf-8")

    env = os.environ.copy()
    env["GOOGLE_SERVICE_ACCOUNT_PATH"] = str(sa)
    env["GOOGLE_SHEETS_SPREADSHEET_ID"] = "1gsjP650gW75Rc7eYwimRm578AzOX_V1Xh57r3cgrNSI"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    env["TZ"] = "Europe/Moscow"
    env.setdefault("AUTO_UNARCHIVE", "1")

    # Run with cwd=work so load_env_files finds .env
    cmd = [sys.executable, str(SCRIPT)]
    print(f"Running {SCRIPT.name} from {work}")
    return subprocess.call(cmd, cwd=str(work), env=env)


if __name__ == "__main__":
    raise SystemExit(main())
