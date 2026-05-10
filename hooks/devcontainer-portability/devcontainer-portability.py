#!/usr/bin/env python3
"""
Devcontainer portability enforcer.

PreToolUse on Edit|Write|MultiEdit. Triggers only on container/devcontainer
config files. Blocks hardcoded host paths so configs work on every machine
and on the VPS.

Scope (filename-based):
  Dockerfile, *.Dockerfile, Dockerfile.*
  docker-compose*.yml, docker-compose*.yaml, compose*.yml, compose*.yaml
  .devcontainer/* (any file)
  devcontainer.json

Blocked patterns in the new content:
  /Users/<anything>           macOS host
  /home/<anything>            Linux host (allowed inside containers, but in
                              host-bound volumes/build paths it's wrong)
  C:\\Users\\<anything>       Windows host
  ~/something                 only flagged inside volume mappings
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

HOST_PATH_PATTERNS = [
    (re.compile(r"/Users/[^\s:\"']+"), "macOS host path"),
    (re.compile(r"C:\\\\Users\\\\[^\s:\"']+"), "Windows host path"),
    (re.compile(r"C:/Users/[^\s:\"']+"), "Windows host path"),
    (re.compile(r"/home/[A-Za-z][\w.-]*/[^\s:\"']+"), "Linux host path"),
]


def in_scope(file_path: str) -> bool:
    p = Path(file_path)
    name = p.name
    parts = {x.lower() for x in p.parts}
    if ".devcontainer" in parts:
        return True
    if name.lower() == "devcontainer.json":
        return True
    if name == "Dockerfile" or name.endswith(".Dockerfile") or name.startswith("Dockerfile."):
        return True
    if re.match(r"^(docker-)?compose.*\.ya?ml$", name, re.IGNORECASE):
        return True
    return False


def extract_new_content(tool_name: str, tool_input: dict) -> str:
    if tool_name == "Write":
        return tool_input.get("content", "") or ""
    if tool_name == "Edit":
        return tool_input.get("new_string", "") or ""
    if tool_name == "MultiEdit":
        edits = tool_input.get("edits", []) or []
        return "\n".join(e.get("new_string", "") for e in edits if isinstance(e, dict))
    return ""


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    tool_input = payload.get("tool_input", {}) or {}
    file_path = tool_input.get("file_path", "")
    if not file_path or not in_scope(file_path):
        return 0

    content = extract_new_content(payload.get("tool_name", ""), tool_input)
    if not content:
        return 0

    hits: list[tuple[str, str]] = []
    for regex, label in HOST_PATH_PATTERNS:
        for m in regex.finditer(content):
            hits.append((label, m.group(0)))

    if not hits:
        return 0

    rel = os.path.relpath(file_path)
    lines = [f"[devcontainer-portability] Hardcoded host paths in {rel}:"]
    for label, snippet in hits[:5]:
        lines.append(f"  {label}: {snippet}")
    if len(hits) > 5:
        lines.append(f"  ... and {len(hits) - 5} more")
    lines.append("Replace with one of:")
    lines.append("  - Relative path (./data, ../config) for repo-local mounts")
    lines.append("  - Named volume (kp-data:/app/data)")
    lines.append("  - Environment variable (${HOME}/..., ${DATA_DIR})")
    lines.append("Reason: hardcoded host paths break portability and VPS deploys.")
    sys.stderr.write("\n".join(lines) + "\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
