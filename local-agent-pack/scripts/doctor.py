#!/usr/bin/env python3
"""Check local-agent-pack Phase 1 runtime prerequisites."""

from __future__ import annotations

import json
import os
import shutil
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
OPENROUTER = ROOT / "scripts" / "openrouter.py"


def main() -> int:
    checks = {
        "openrouterAdapter": OPENROUTER.is_file(),
        "apiKeyEnv": bool(os.environ.get("OPENROUTER_API_KEY")),
        "cloudApproval": os.environ.get("LOCAL_AGENT_PACK_ALLOW_CLOUD") == "1",
        "ffprobe": bool(shutil.which("ffprobe")),
    }
    print(json.dumps(checks, indent=2))
    return 0 if checks["openrouterAdapter"] else 1


if __name__ == "__main__":
    sys.exit(main())
