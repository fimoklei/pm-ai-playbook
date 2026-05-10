# Devcontainer-Portability Hook

`PreToolUse` on `Edit|Write|MultiEdit`. Blocks hardcoded host paths in container/devcontainer configs so they remain portable across machines and VPS deploys.

## How it works

- **In scope** (filename-based):
  - `Dockerfile`, `*.Dockerfile`, `Dockerfile.*`
  - `docker-compose*.yml/.yaml`, `compose*.yml/.yaml`
  - Anything inside `.devcontainer/`
  - `devcontainer.json`
- **Blocked patterns** in the new content:
  - macOS host: `/Users/...`
  - Linux host: `/home/<user>/...`
  - Windows host: `C:\Users\...` or `C:/Users/...`
- On a hit → exit 2 with a message listing the offending snippets and three suggested replacements:
  - Relative path (`./data`, `../config`) for repo-local mounts.
  - Named volume (`kp-data:/app/data`).
  - Environment variable (`${HOME}/...`, `${DATA_DIR}`).

## Installation

1. **Copy the script:**
   ```bash
   mkdir -p ~/.claude/hooks
   cp devcontainer-portability.py ~/.claude/hooks/devcontainer-portability.py
   chmod +x ~/.claude/hooks/devcontainer-portability.py
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
               "command": "python3 ~/.claude/hooks/devcontainer-portability.py",
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
# Should block (Users path in a docker-compose file)
echo '{"tool_name":"Write","tool_input":{"file_path":"/tmp/docker-compose.yml","content":"volumes:\n  - /Users/me/data:/app/data\n"}}' \
  | python3 ~/.claude/hooks/devcontainer-portability.py
echo "exit: $?"   # expect 2

# Should allow (relative path)
echo '{"tool_name":"Write","tool_input":{"file_path":"/tmp/docker-compose.yml","content":"volumes:\n  - ./data:/app/data\n"}}' \
  | python3 ~/.claude/hooks/devcontainer-portability.py
echo "exit: $?"   # expect 0
```

## Removal

Remove the matcher from `~/.claude/settings.json` and delete the script.
