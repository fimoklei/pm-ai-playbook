#!/usr/bin/env python3
"""
Six Hats Debate Orchestrator

Usage:
    python3 scripts/six_hats_debate.py "Your topic here" "/path/to/output/"
    python3 scripts/six_hats_debate.py "Should we launch v2?" "Projects/decisions/"

This script is a reference implementation. The actual debate runs via the SKILL.md
workflow in conversation. This file documents the expected behavior and can be used
for batch processing or testing.
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

ROUNDS = 3
# Sequential hats per round; Blue moderates after all rounds (see SKILL.md).
DEBATE_HAT_ORDER = ["white", "red", "yellow", "black", "green"]
HAT_LABELS = {
    "white": "White Hat (Facts & Information)",
    "red": "Red Hat (Emotion & Intuition)",
    "yellow": "Yellow Hat (Optimism & Benefits)",
    "black": "Black Hat (Caution & Risks)",
    "green": "Green Hat (Creativity & Alternatives)",
    "blue": "Blue Hat (Process & Moderation)",
}

TOPIC_MAX_LEN = 500

STUB_BODY = """# Six Hats Debate: {topic}

**Generated**: {when}

This stub was written by `scripts/six_hats_debate.py`. Replace it with full output by running the conversational workflow described in **SKILL.md** in your agent session (three rounds for the hats below, then Blue Hat synthesis).

**Rounds**: {rounds}, **Hat order each round**: {hat_chain}

Blue Hat (**{blue_label}**) synthesizes after the rounds; it does not take a turn with the other hats during each round.

---
*(Body intentionally empty — populate using the skill.)*
"""


def _die(msg: str) -> None:
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


def _resolve_safe_output_dir(raw: str) -> Path:
    if not raw or not raw.strip():
        raise ValueError("output path cannot be empty")
    candidate = Path(raw).expanduser().resolve(strict=False)
    allowed = [Path.cwd().resolve(), Path.home().resolve()]
    candidate_str = str(candidate)
    for base in allowed:
        base_str = str(base)
        try:
            if os.path.commonpath([candidate_str, base_str]) == base_str:
                return candidate
        except ValueError:
            continue
    raise ValueError("output path must be under CWD or your home directory")


def _sanitize_topic(raw: str) -> str:
    """Strip dangerous control chars, flatten line breaks for heading safety, cap length."""
    s = raw.strip()
    if not s:
        raise ValueError("topic cannot be empty")
    cleaned = []
    for ch in s:
        o = ord(ch)
        # Keep tab (9), LF (10), CR (13); strip other ASCII controls and DEL.
        if o == 127 or (o < 32 and o not in (9, 10, 13)):
            continue
        cleaned.append(ch)
    s = "".join(cleaned)
    s = re.sub(r"[\t\n\r]+", " ", s)
    s = re.sub(r" +", " ", s).strip()
    if not s:
        raise ValueError("topic cannot be empty")
    if len(s) > TOPIC_MAX_LEN:
        s = s[: TOPIC_MAX_LEN - 3] + "..."
    return s


def generate_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def main(topic: str, output_path: str):
    try:
        safe_topic = _sanitize_topic(topic)
    except ValueError as e:
        _die(str(e))

    try:
        output_dir = _resolve_safe_output_dir(output_path)
    except ValueError as e:
        _die(str(e))

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        _die("could not create output directory")

    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    when = now.strftime("%Y-%m-%d %H:%M:%S")
    output_file = output_dir / f"debate-{timestamp}.md"

    hat_chain = " → ".join(HAT_LABELS[h] for h in DEBATE_HAT_ORDER)
    body = STUB_BODY.format(
        topic=safe_topic,
        when=when,
        rounds=ROUNDS,
        hat_chain=hat_chain,
        blue_label=HAT_LABELS["blue"],
    )
    try:
        output_file.write_text(body, encoding="utf-8")
    except OSError:
        _die("could not write debate stub")

    print(f"Topic: {safe_topic}")
    print(f"Output: {output_file}")
    print(f"Rounds: {ROUNDS}")
    print(f"Hats per round: {hat_chain}")
    print(f"Moderation: {HAT_LABELS['blue']} after rounds")
    print("---")
    print("Stub written. Replace with full debate via SKILL.md in conversation.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/six_hats_debate.py <topic> <output_path>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
