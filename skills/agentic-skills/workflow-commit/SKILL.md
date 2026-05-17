---
name: workflow-commit
description: Use when the user asks to run workflow:commit, create a commit, make a git commit, stage changes, write a commit message, or prepare local changes for shipping.
license: MIT
---

# Workflow Commit

Create a safe, intentional git commit from the current worktree.

## Trigger Phrases

- `workflow:commit`
- `commit workflow`
- `make a commit`
- `create a commit`
- `stage and commit this`
- `commit these changes`

## Process

1. Inspect repository state:
   - Run `git status --short --branch`.
   - Run `git diff --staged`.
   - If nothing is staged, inspect `git diff` and `git status --short`, then propose what should be staged.

2. Protect user work:
   - Never revert, reset, discard, or overwrite user changes.
   - If unrelated changes are present, leave them untouched and stage only the files needed for the commit.
   - If the intended commit scope is ambiguous, ask before staging.

3. Honor main-branch policy:
   - Run `git branch --show-current` and `git rev-parse --show-toplevel`.
   - If on `main` or `master` and `.claude/allow-main-commits` is absent at the repo root, stop and create a feature branch before committing.
   - If on `main` or `master` and `.claude/allow-main-commits` exists, allow content-only commits but block commits touching `.claude/` or `06-system/`.
   - Check both already staged files and any files being staged for this commit before deciding.
   - If protected paths are involved, stop and create a feature branch before committing.

4. Run pre-commit checks:
   - Always run `git diff --check`.
   - If `package.json` exists, inspect scripts before choosing checks.
   - Prefer existing repo scripts in this order when present: lint, typecheck, test.
   - Do not invent missing scripts. If no check command is discoverable, say so clearly.
   - If checks fail, stop and help fix the issue before committing.

5. Review security gates:
   - Read the bundled `security.md` in this skill's directory before proposing the commit.
   - If the checklist reveals a blocker, stop and help resolve it.

6. Propose the commit:
   - Choose one conventional commit type: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, or `chore`.
   - Use a concise subject: `<type>: <description>`.
   - Add a body only when the change is complex or the why is not obvious.
   - Suggest splitting into multiple commits when the staged changes contain unrelated concerns.

7. Ask for approval before creating the commit:
   - Offer to use the message as-is, modify it, add a body, or stage different files.
   - After approval, create the commit.
   - Show the resulting commit hash and subject.

8. Offer the next step:
   - Ask whether to push, open a PR, or ship the branch.

## Command Notes

- Follow the active agent and project shell rules. In Michiel's Codex setup, prefix shell commands with `rtk`.
- Use non-interactive git commands whenever possible.
- Do not run destructive commands unless the user explicitly asks for them.
