#!/usr/bin/env python3
"""Manual/alias entrypoint: same as weekly status with AUTO_UNARCHIVE=1.

Sunday check already auto-unarchives via popolnenie_status.py.
Keep this script for explicit one-off runs.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ.setdefault("AUTO_UNARCHIVE", "1")
import popolnenie_status as ps  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(ps.main())
