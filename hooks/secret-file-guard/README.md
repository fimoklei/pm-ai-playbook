# Secret-File-Guard Hook

`PreToolUse` on `Edit|Write|MultiEdit`. Blocks an agent from writing or editing secret files (`.env`, private keys, certificates, keystores, credential files). Costs nothing day to day; prevents the rare disaster — committing a private key, overwriting a production `.env`.

## How it works

- Reads the tool-call JSON from stdin and inspects `tool_input.file_path`.
- Matches the basename against an allow-list first, then a deny-list of names/globs, plus a deny-list of path fragments.
- On a hit → exit 2 with a named reason on stderr. Claude Code treats exit 2 as a hard block and surfaces the message to the agent.
- A missing or unparseable payload, or a call without a `file_path`, exits 0 (never blocks unrelated tools).
- **Blocked (filename / glob):**
  - `.env` and any `.env.*` variant (environment secrets).
  - Keys & certs: `*.pem`, `*.key`, `*.p8`, `*.p12`, `*.pfx`, `*.jks`, `*.keystore`, `*.crt`, `*.cer`, `*.der`.
  - SSH private keys: `id_rsa`, `id_dsa`, `id_ecdsa`, `id_ed25519`.
  - Credentials & tokens: `credentials`, `credentials.json`, `*.secret`, `secrets.*`, `.npmrc`, `.pypirc`, `.netrc`.
- **Blocked (path fragment):** anything under `~/.ssh/`, `~/.aws/`, or `~/.gnupg/`.
- **Allowed on purpose:** `.env.example`, `.env.sample`, `.env.template`, `.env.dist`, `.env.local.example` — these are empty templates with no real secrets.

## Installation

1. **Copy the script:**
   ```bash
   mkdir -p ~/.claude/hooks
   cp secret-file-guard.py ~/.claude/hooks/secret-file-guard.py
   chmod +x ~/.claude/hooks/secret-file-guard.py
   ```

2. **Add to `~/.claude/settings.json`:**
   ```json
   {
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Edit|Write|MultiEdit",
           "hooks": [
             {
               "type": "command",
               "command": "python3 ~/.claude/hooks/secret-file-guard.py",
               "timeout": 5
             }
           ]
         }
       ]
     }
   }
   ```

3. **Restart Claude Code** to activate.

## Testing

```bash
# Should block (a .env file)
echo '{"tool_input":{"file_path":"/x/.env"}}' \
  | python3 ~/.claude/hooks/secret-file-guard.py
echo "exit: $?"   # expect 2

# Should allow (an .env.example template)
echo '{"tool_input":{"file_path":"/x/.env.example"}}' \
  | python3 ~/.claude/hooks/secret-file-guard.py
echo "exit: $?"   # expect 0

# Should allow (ordinary source file)
echo '{"tool_input":{"file_path":"/x/src/app.ts"}}' \
  | python3 ~/.claude/hooks/secret-file-guard.py
echo "exit: $?"   # expect 0

# Should block (uppercase variant — matching is case-insensitive)
echo '{"tool_input":{"file_path":"/x/.ENV"}}' \
  | python3 ~/.claude/hooks/secret-file-guard.py
echo "exit: $?"   # expect 2
```

Matching lowercases the basename first, so casing tricks (`.ENV`, `prod.PEM`, `ID_RSA`) cannot slip past the deny-list.

## Removal

Remove the matcher from `~/.claude/settings.json` and delete the script.
