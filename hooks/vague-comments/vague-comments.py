#!/usr/bin/env python3
"""
Vague-comment detector.

PreToolUse on Edit|Write|MultiEdit. Scans incoming content for vague markers in
code files only. Skips markdown/notes.

Allowed forms (must include a tracker reference):
  TODO(PROJ-123)         Plane, Jira, etc.
  TODO(#123)             GitHub issue in current repo
  TODO(owner/repo#123)   GitHub cross-repo
  FIXME(KP-42): ...      same rules
  HACK(GH-7): ...        same rules

Blocked:
  Bare TODO/FIXME/HACK/XXX
  Phrases: "implement later", "for now", "temporary", "placeholder",
           "implement this", "fix later", "to be implemented"
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

CODE_EXTS = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs",
    ".py", ".rb", ".go", ".rs", ".java", ".kt", ".scala",
    ".cs", ".cpp", ".cc", ".c", ".h", ".hpp",
    ".php", ".swift", ".m", ".mm",
    ".sh", ".bash", ".zsh", ".fish",
    ".sql", ".lua", ".vue", ".svelte",
}

TRACKER_REF = (
    r"(?:"
    r"#\d+"                                 # #123
    r"|[A-Za-z][\w-]*/[\w.-]+#\d+"           # owner/repo#123
    r"|[A-Z][A-Z0-9]+-\d+"                   # PROJ-123 (Plane/Jira)
    r")"
)

BARE_MARKER_RE = re.compile(
    rf"\b(TODO|FIXME|HACK|XXX)\b(?!\s*\(\s*{TRACKER_REF}\s*\))",
    re.IGNORECASE,
)

VAGUE_PHRASES = [
    r"\bimplement(?:ation)? later\b",
    r"\bfix later\b",
    r"\bto be implemented\b",
    r"\bplaceholder\b",
    r"\bfor now\b",
    r"\btemporary fix\b",
    r"\btemporary workaround\b",
]
VAGUE_PHRASE_RE = re.compile("|".join(VAGUE_PHRASES), re.IGNORECASE)


def extract_new_content(tool_name: str, tool_input: dict) -> str:
    if tool_name == "Write":
        return tool_input.get("content", "") or ""
    if tool_name == "Edit":
        return tool_input.get("new_string", "") or ""
    if tool_name == "MultiEdit":
        edits = tool_input.get("edits", []) or []
        return "\n".join(e.get("new_string", "") for e in edits if isinstance(e, dict))
    return ""


def is_code_file(path: str) -> bool:
    return Path(path).suffix.lower() in CODE_EXTS


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {}) or {}
    file_path = tool_input.get("file_path", "")
    if not file_path or not is_code_file(file_path):
        return 0

    content = extract_new_content(tool_name, tool_input)
    if not content:
        return 0

    bare_hits = [m.group(1) for m in BARE_MARKER_RE.finditer(content)]
    phrase_hits = [m.group(0) for m in VAGUE_PHRASE_RE.finditer(content)]

    if not bare_hits and not phrase_hits:
        return 0

    rel = os.path.relpath(file_path)
    msg = [f"[vague-comments] {rel} contains deferred-work markers without tracker refs."]
    if bare_hits:
        msg.append(f"  Bare markers: {', '.join(sorted(set(bare_hits)))}")
    if phrase_hits:
        msg.append(f"  Vague phrases: {', '.join(sorted(set(phrase_hits)))}")
    msg.append("Resolve one of:")
    msg.append("  1) Implement it now.")
    msg.append("  2) Remove the comment / placeholder code.")
    msg.append("  3) Link a tracker: TODO(PROJ-123), TODO(#42), or TODO(owner/repo#42).")
    msg.append("     Capture in Plane via plane-quick-capture or in GitHub via create-issue first.")
    sys.stderr.write("\n".join(msg) + "\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
