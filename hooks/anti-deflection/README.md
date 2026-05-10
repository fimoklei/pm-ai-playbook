# Anti-Deflection Hook

`Stop` hook that scans Claude's last assistant message for deflection language ("pre-existing", "out of scope", "defer for later", "not related to my changes", etc.) and blocks the stop unless concrete evidence is supplied.

## How it works

- Reads the transcript at `transcript_path` and isolates the last assistant message.
- Searches for deflection patterns. For each match, looks within ~200 characters for **evidence**:
  - `path/to/file.ext:42` — file path with line number, OR
  - `#123` — GitHub issue ref, OR
  - `PROJ-123` — Plane/Jira-style ticket ref.
- If a deflection phrase appears **without** evidence in its window → exit 2 with a stderr message instructing Claude to either fix the issue or cite a tracker reference.
- Honors `stop_hook_active` to avoid infinite Stop loops.

## Installation

1. **Copy the script:**
   ```bash
   mkdir -p ~/.claude/hooks
   cp anti-deflection.py ~/.claude/hooks/anti-deflection.py
   chmod +x ~/.claude/hooks/anti-deflection.py
   ```

2. **Add to `~/.claude/settings.json`:**
   ```json
   {
     "hooks": {
       "Stop": [
         {
           "hooks": [
             {
               "type": "command",
               "command": "python3 ~/.claude/hooks/anti-deflection.py",
               "timeout": 10
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
# Allowed: deflection with evidence
echo '{"transcript_path":"/dev/null","stop_hook_active":false}' \
  | python3 ~/.claude/hooks/anti-deflection.py
echo "exit: $?"   # expect 0 (no transcript = no-op)
```

Trigger live by ending a turn with "this is pre-existing" without a `file:line` or `#123` reference — the next Stop will be blocked.

## Removal

Remove the `Stop` matcher from `~/.claude/settings.json` and delete the script.
