# Read-Tracker Hook

Read-before-Edit gate. Blocks any `Edit`/`Write`/`MultiEdit` on an existing file that has not first been `Read` in the current session. Defends against stale views after context compaction.

## How it works

- **`PostToolUse` on `Read`** (mode `record`): appends the absolute path to a per-session log at `~/.claude/hooks/state/read-tracker/<session_id>.txt`.
- **`PreToolUse` on `Edit|Write|MultiEdit`** (mode `check`):
  - Path does not exist → allowed (creating a new file).
  - Path was previously `Read` (or already mutated) in this session → allowed.
  - Otherwise → exit 2 + stderr message; Claude gets feedback and must `Read` first.

## Installation

1. **Copy the script:**
   ```bash
   mkdir -p ~/.claude/hooks
   cp read-tracker.py ~/.claude/hooks/read-tracker.py
   chmod +x ~/.claude/hooks/read-tracker.py
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
               "command": "python3 ~/.claude/hooks/read-tracker.py check",
               "timeout": 5
             }
           ]
         }
       ],
       "PostToolUse": [
         {
           "matcher": "Read",
           "hooks": [
             {
               "type": "command",
               "command": "python3 ~/.claude/hooks/read-tracker.py record",
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
# Simulate a check that should block
echo '{"session_id":"test","tool_input":{"file_path":"/etc/hosts"}}' \
  | python3 ~/.claude/hooks/read-tracker.py check
echo "exit: $?"   # expect 2
```

State files live in `~/.claude/hooks/state/read-tracker/`. Safe to delete to reset.

## Removal

Remove the matchers from `~/.claude/settings.json` and delete the script + `state/read-tracker/` directory.
