# Hooks

Hook patterns that enforce quality and consistency in AI development workflows.

## Table of contents

- [Claude Code hooks](#claude-code-hooks)

## 🪝 Claude Code hooks

Global hooks installed in `~/.claude/hooks/` that apply to all Claude Code sessions.

| Name                                 | Purpose                                                                                                                                          | When to use                                                                      | Link                          |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------- | ----------------------------- |
| coding-principles (UserPromptSubmit) | Injects coding principles (DRY, YAGNI, KISS, Pragmatic) and behavioral guidelines into every user prompt. Adds random animal emoji to responses. | Automatically on every user input (all projects)                                 | `hooks/coding-principles/`    |
| protect-main-branch (PreToolUse)     | Blocks direct commits and force-pushes on main/master. Allows normal pushes for merging.                                                         | Automatically on every Bash tool call (all projects)                             | `hooks/protect-main-branch/`  |
| typecheck-after-edit (PostToolUse)   | Runs `tsc --noEmit` after editing `.ts`/`.tsx` files. Surfaces type errors immediately.                                                          | Automatically after Edit/Write on TypeScript files (projects with tsconfig.json) | `hooks/typecheck-after-edit/` |
| format-on-edit (PostToolUse)         | Auto-formats files after edits using Prettier (web/config) and Black (Python). Silent when formatters are missing.                               | Automatically after Edit/Write on supported file types (all projects)            | `hooks/format-on-edit/`       |
