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
| read-tracker (Pre+PostToolUse)       | Read-before-Edit gate. Blocks Edit/Write/MultiEdit on an existing file that has not first been Read in the current session.                      | Automatically on every Read and Edit/Write/MultiEdit (all projects)              | `hooks/read-tracker/`         |
| anti-deflection (Stop)               | Scans the last assistant message for deflection phrases (pre-existing, out of scope, defer for later) and blocks the stop unless `path:line` or `#123`/`PROJ-123` evidence is supplied. | Automatically at the end of every assistant turn (all projects) | `hooks/anti-deflection/`      |
| vague-comments (PreToolUse)          | Blocks bare TODO/FIXME/HACK/XXX and vague phrases (for now, placeholder, implement later) in code files. Allows tracker-linked forms like TODO(PROJ-123) or TODO(#42). | Automatically on Edit/Write/MultiEdit of code files (all projects)               | `hooks/vague-comments/`       |
| devcontainer-portability (PreToolUse)| Blocks hardcoded host paths (`/Users/...`, `/home/<user>/...`, `C:\Users\...`) in Dockerfiles, docker-compose files, and devcontainer configs. Suggests relative paths, named volumes, or `${HOME}`. | Automatically on Edit/Write/MultiEdit of container/devcontainer configs (all projects) | `hooks/devcontainer-portability/` |
| secret-file-guard (PreToolUse)      | Blocks Write/Edit on secret files (`.env`, private keys, certs, keystores, credentials, `~/.ssh`, `~/.aws`, `~/.gnupg`). Allows `.env.example` and similar empty templates. | Automatically on Edit/Write/MultiEdit (all projects) | `hooks/secret-file-guard/` |
