#!/usr/bin/env python3
"""
Anti-deflection Stop hook.

Reads the transcript, finds the LAST assistant message, scans its text for
deflection phrases. If found, exits 2 to send Claude back with feedback.

Honors stop_hook_active to avoid infinite loops.

Whitelist: a deflection phrase is allowed if it appears alongside concrete
evidence on the same or next line — `path/to/file.ext:LINE` style reference.
That makes "scope-deferral with proof" possible (which CLAUDE.md endorses).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

DEFLECTION_PATTERNS = [
    r"\bpre-existing\b",
    r"\bnot related to (?:my|the) changes?\b",
    r"\bout of scope\b",
    r"\bbeyond (?:the |this )?scope\b",
    r"\bdefer(?:red)? (?:to|for) later\b",
    r"\bleft as[- ]is\b",
    r"\bwould require (?:a )?(?:larger|bigger|broader) refactor\b",
    r"\bnot (?:caused )?by (?:my|the) changes?\b",
    r"\bunrelated to (?:my|the) (?:work|changes?)\b",
    r"\bfor (?:a )?future (?:pr|task|iteration)\b",
]

# Evidence: file path with extension + colon + line number, OR explicit issue ref.
EVIDENCE_RE = re.compile(
    r"(?:[\w./\-]+\.\w{1,6}:\d+)"           # path:line
    r"|(?:#\d+)"                            # GitHub #123
    r"|(?:[A-Z][A-Z0-9]+-\d+)"              # PROJ-123
)


def last_assistant_text(transcript_path: str) -> str:
    p = Path(transcript_path)
    if not p.exists():
        return ""
    last = ""
    try:
        for line in p.read_text(errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = obj.get("message") or obj
            role = msg.get("role") or obj.get("type")
            if role != "assistant":
                continue
            content = msg.get("content")
            if isinstance(content, str):
                last = content
            elif isinstance(content, list):
                parts = []
                for c in content:
                    if isinstance(c, dict) and c.get("type") == "text":
                        parts.append(c.get("text", ""))
                if parts:
                    last = "\n".join(parts)
    except OSError:
        return ""
    return last


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    if payload.get("stop_hook_active"):
        return 0

    transcript = payload.get("transcript_path")
    if not transcript:
        return 0

    text = last_assistant_text(transcript)
    if not text:
        return 0

    matches: list[str] = []
    for pat in DEFLECTION_PATTERNS:
        m = re.search(pat, text, re.IGNORECASE)
        if not m:
            continue
        # Look for evidence within ~200 chars of the match.
        window_start = max(0, m.start() - 50)
        window_end = min(len(text), m.end() + 200)
        window = text[window_start:window_end]
        if EVIDENCE_RE.search(window):
            continue
        matches.append(m.group(0))

    if not matches:
        return 0

    flagged = ", ".join(sorted(set(matches)))
    sys.stderr.write(
        "[anti-deflection] Your final message used deflection language without "
        f"concrete evidence: {flagged}\n"
        "Either fix the issue, or cite specific evidence: file path with line "
        "number (path/to/file.ts:42) or tracker reference (#123, PROJ-456) and "
        "one technical reason it cannot be addressed in this turn.\n"
        "Source: CLAUDE.md — root cause over workarounds, facts over comfort.\n"
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
