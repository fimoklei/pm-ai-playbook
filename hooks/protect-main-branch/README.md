# Protect Main Branch Hook

Prevents direct commits and force-pushes on `main` or `master` branch. Normal pushes are allowed (needed after merging feature branches).

Repos with `.claude/allow-main-commits` use smart mode: content-only commits on `main` are allowed, but commits touching protected paths (`.claude/` or `06-system/`) are blocked.

## Installation

1. **Copy the hook script:**
   ```bash
   mkdir -p ~/.claude/hooks
   cp protect-main-branch.sh ~/.claude/hooks/protect-main-branch.sh
   chmod +x ~/.claude/hooks/protect-main-branch.sh
   ```

2. **Add to `~/.claude/settings.json`:**
   ```json
   {
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Bash",
           "hooks": [
             {
               "type": "command",
               "command": "~/.claude/hooks/protect-main-branch.sh",
               "timeout": 5
             }
           ]
         }
       ]
     }
   }
   ```

3. **Restart Claude Code** to activate.

## How it works

1. Fires on every `Bash` tool call (PreToolUse event)
2. Parses the tool input JSON from stdin using `jq`
3. Exits immediately if not on `main` or `master`
4. Resolves the effective repo from an inline `cd <path>` in the command, falling back to the session `cwd`
5. Blocks `git commit` on `main` / `master`
6. In smart mode, allows content-only commits but blocks commits touching `.claude/` or `06-system/`
7. Blocks `git push --force` / `git push -f` — prevents destructive rewrite of shared history
8. Allows everything else (normal push, checkout, branch, merge, etc.)

## Testing

```bash
# Simulate a git commit on main (should deny)
echo '{"cwd":"/path/to/repo","tool_input":{"command":"git commit -m test"}}' | bash protect-main-branch.sh

# Simulate a force-push on main (should deny)
echo '{"cwd":"/path/to/repo","tool_input":{"command":"git push --force origin main"}}' | bash protect-main-branch.sh

# Simulate a normal push on main (should pass through silently)
echo '{"cwd":"/path/to/repo","tool_input":{"command":"git push origin main"}}' | bash protect-main-branch.sh

# Simulate a non-git command (should pass through silently)
echo '{"cwd":"/path/to/repo","tool_input":{"command":"ls -la"}}' | bash protect-main-branch.sh

# Simulate a command that changes repo inline; inline cd should win over cwd
echo '{"cwd":"/path/to/other/repo","tool_input":{"command":"cd /path/to/repo && git commit -m test"}}' | bash protect-main-branch.sh
```

## Removal

Remove the `PreToolUse` entry from `~/.claude/settings.json` and delete `~/.claude/hooks/protect-main-branch.sh`.
