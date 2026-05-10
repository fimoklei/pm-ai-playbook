#!/usr/bin/env python3
"""
Read-before-Edit gate.

Two roles, dispatched via $1:
  record  - PostToolUse on Read: append file_path to session state
  check   - PreToolUse on Edit|Write|MultiEdit: block if path not previously Read

State: ~/.claude/hooks/state/read-tracker/<session_id>.txt (one absolute path per line).

Allow rules for `check`:
  - Write to a non-existent path is allowed (creating new file).
  - Path that has been Read in this session is allowed.
  - Path that was already mutated in this session via Edit/Write is allowed
    (we record successful intents so chained edits don't require re-reads).
  - Otherwise: exit 2 with stderr message → Claude sees feedback, edit blocked.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

STATE_DIR = Path.home() / ".claude" / "hooks" / "state" / "read-tracker"


def state_file(session_id: str) -> Path:
    safe = "".join(c for c in session_id if c.isalnum() or c in "-_") or "default"
    return STATE_DIR / f"{safe}.txt"


def load_paths(session_id: str) -> set[str]:
    f = state_file(session_id)
    if not f.exists():
        return set()
    return {line.strip() for line in f.read_text().splitlines() if line.strip()}


def append_path(session_id: str, path: str) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with state_file(session_id).open("a") as f:
        f.write(path + "\n")


def main() -> int:
    if len(sys.argv) < 2:
        return 0
    mode = sys.argv[1]
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    session_id = payload.get("session_id", "default")
    tool_input = payload.get("tool_input", {}) or {}
    file_path = tool_input.get("file_path")
    if not file_path:
        return 0

    abs_path = str(Path(file_path).resolve())

    if mode == "record":
        append_path(session_id, abs_path)
        return 0

    if mode == "check":
        # New file creation is fine.
        if not Path(abs_path).exists():
            append_path(session_id, abs_path)
            return 0
        seen = load_paths(session_id)
        if abs_path in seen:
            return 0
        rel = os.path.relpath(abs_path)
        sys.stderr.write(
            f"[read-before-edit] {rel} has not been Read in this session.\n"
            "Read the file first to refresh your view, then edit.\n"
            "Reason: context compaction may have wiped your prior view of this file.\n"
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
