# Vague-Comments Hook

`PreToolUse` on `Edit|Write|MultiEdit`. Blocks bare `TODO`/`FIXME`/`HACK`/`XXX` markers and vague placeholder phrases in code, unless a tracker reference is attached.

## How it works

- Active only on code extensions: `.ts .tsx .js .jsx .mjs .cjs .py .rb .go .rs .java .kt .scala .cs .cpp .cc .c .h .hpp .php .swift .m .mm .sh .bash .zsh .fish .sql .lua .vue .svelte`. Markdown and notes are skipped.
- Extracts the new content (`Write.content`, `Edit.new_string`, or all `MultiEdit.edits[*].new_string`).
- **Blocks**:
  - Bare markers: `TODO`, `FIXME`, `HACK`, `XXX` (case-insensitive).
  - Vague phrases: `for now`, `placeholder`, `implement later`, `to be implemented`, `temporary fix`, `temporary workaround`, `fix later`.
- **Allows** any marker with a tracker reference:
  - `TODO(PROJ-123)` — Plane/Jira/etc.
  - `TODO(#42)` — GitHub issue in current repo.
  - `TODO(owner/repo#42)` — GitHub cross-repo.
- On a hit → exit 2 with a message that lists the offending markers and the three resolutions: implement now, remove the comment, or link a tracker (capture via `plane-quick-capture` or `create-issue` first).

## Installation

1. **Copy the script:**
   ```bash
   mkdir -p ~/.claude/hooks
   cp vague-comments.py ~/.claude/hooks/vague-comments.py
   chmod +x ~/.claude/hooks/vague-comments.py
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
               "command": "python3 ~/.claude/hooks/vague-comments.py",
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
# Should block (bare TODO in a .ts file)
echo '{"tool_name":"Write","tool_input":{"file_path":"/tmp/x.ts","content":"// TODO: fix this\n"}}' \
  | python3 ~/.claude/hooks/vague-comments.py
echo "exit: $?"   # expect 2

# Should allow (TODO with tracker ref)
echo '{"tool_name":"Write","tool_input":{"file_path":"/tmp/x.ts","content":"// TODO(PROJ-123): fix this\n"}}' \
  | python3 ~/.claude/hooks/vague-comments.py
echo "exit: $?"   # expect 0
```

## Removal

Remove the matcher from `~/.claude/settings.json` and delete the script.
