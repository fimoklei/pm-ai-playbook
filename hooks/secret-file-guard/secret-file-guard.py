#!/usr/bin/env python3
"""Blocks Write/Edit on secret files (.env, keys, certs, credentials)."""
import fnmatch
import json
import os
import sys

ALLOW_NAMES = {".env.example", ".env.sample", ".env.template", ".env.dist", ".env.local.example"}

DENY_NAMES = [
    (".env", "a .env file (environment secrets)"),
    (".env.*", "a .env variant (environment secrets)"),
    ("*.pem", "a private key / certificate (.pem)"),
    ("*.key", "a private key (.key)"),
    ("*.p8", "an Apple private key (.p8)"),
    ("*.p12", "a PKCS#12 keystore (.p12)"),
    ("*.pfx", "a PKCS#12 keystore (.pfx)"),
    ("*.jks", "a Java keystore (.jks)"),
    ("*.keystore", "a keystore"),
    ("*.crt", "a certificate (.crt)"),
    ("*.cer", "a certificate (.cer)"),
    ("*.der", "a certificate (.der)"),
    ("id_rsa", "an SSH private key"),
    ("id_dsa", "an SSH private key"),
    ("id_ecdsa", "an SSH private key"),
    ("id_ed25519", "an SSH private key"),
    ("credentials", "a credentials file"),
    ("credentials.json", "a credentials file"),
    ("*.secret", "a secrets file"),
    ("secrets.*", "a secrets file"),
    (".npmrc", "an .npmrc (may contain publish tokens)"),
    (".pypirc", "a .pypirc (may contain PyPI tokens)"),
    (".netrc", "a .netrc (may contain login credentials)"),
]

DENY_PATHS = [
    ("/.ssh/", "a file in ~/.ssh"),
    ("/.aws/", "a file in ~/.aws (cloud credentials)"),
    ("/.gnupg/", "a file in ~/.gnupg"),
]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    file_path = (payload.get("tool_input") or {}).get("file_path", "")
    if not file_path:
        return 0

    # Lowercase the basename before matching: fnmatch is case-sensitive on
    # POSIX, and macOS filesystems are case-insensitive, so .ENV would be the
    # same file as .env yet slip past case-sensitive patterns otherwise.
    name = os.path.basename(file_path).lower()
    if name in ALLOW_NAMES:
        return 0

    lowered = file_path.replace("\\", "/").lower()
    for fragment, reason in DENY_PATHS:
        if fragment in lowered:
            return block(file_path, reason)

    for pattern, reason in DENY_NAMES:
        if fnmatch.fnmatch(name, pattern):
            return block(file_path, reason)

    return 0


def block(file_path: str, reason: str) -> int:
    sys.stderr.write(
        f"BLOCKED by secret-file-guard: {file_path} looks like {reason}. "
        "Secret files are not touched via Write/Edit. "
        "If you really mean this, rename the file or adjust the hook.\n"
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
