---
name: workflow-ship
description: Use when the user asks to run workflow:ship, ship a branch, publish a feature branch, open and merge a PR, or push/PR/merge/cleanup completed work.
license: MIT
---

# Workflow Ship

Ship the current feature branch by pushing, opening a PR, merging it to `main`, and cleaning up safely.

## Trigger Phrases

- `workflow:ship`
- `ship workflow`
- `ship this branch`
- `publish this branch`
- `open and merge a PR`
- `push, PR, merge, and clean up`

## Process

1. Verify branch state:
   - Run `git branch --show-current`.
   - Stop if the branch is `main` or `master`.
   - Run `git status --short --branch`.
   - Stop if there are uncommitted changes and suggest `workflow:commit`.
   - Run `git log main..HEAD --oneline` and stop if there are no commits ahead of `main`.

2. Run cross-model review as final gate:
   - Detect runtime by checking the `CLAUDECODE` environment variable:
     - If `$CLAUDECODE` is set, the host is Claude Code -> the reviewer is **Codex**.
     - Otherwise (Codex, plain shell, CI, anything else) -> the reviewer is **Claude**.
   - Codex reviewer path (running inside Claude Code):
     - Verify `codex` is on PATH (`command -v codex`). If missing, stop with a clear error - do not silently skip.
     - Run `codex review --base main` in the foreground. Stream the output to the user.
   - Claude reviewer path (running inside Codex or elsewhere):
     - Verify `claude` is on PATH (`command -v claude`). If missing, stop with a clear error - do not silently skip.
     - Run, in the foreground, streaming output to the user:
       ```
       git diff main...HEAD | claude -p --model sonnet "Review this diff for defects (bugs, edge cases, security holes, broken assumptions). For every finding output a line in this exact format: 'Review comment: [P0|P1|P2|P3] <description>'. If there are no findings, output exactly: 'No findings.' Do not output anything else."
       ```
   - If the reviewer exits non-zero, stop and report - do not push.
   - Parse the reviewer stdout for the regex `Review comment:|\[P[0-3]\]`.
   - If there is no match, the review is clean. Continue to step 3 without prompting.
   - If there is a match, halt and present two options to the user (use `AskUserQuestion` in Claude Code; in Codex or other hosts, prompt the user explicitly and wait for an answer):
     - `Abort ship` (Recommended) - stop the workflow. The user fixes the findings outside ship (e.g. via `workflow:commit`) and re-runs `workflow:ship`. Do not attempt fixes inside this workflow.
     - `Ignore findings and ship anyway` - continue to step 3.

3. Push the branch:
   - Detect whether an upstream exists with `git rev-parse --abbrev-ref --symbolic-full-name @{u}`.
   - If no upstream exists, run `git push -u origin <branch>`.
   - If upstream exists, run `git push`.

4. Summarize the shipment:
   - Run `git log main..HEAD --oneline`.
   - Run `git diff --stat main...HEAD`.
   - Show the commits and a compact summary before creating the PR.

5. Create the PR:
   - Use `gh pr create`.
   - Derive the title from the branch name and commits using conventional-commit style.
   - Include a body with `## Summary` and `## Test plan`.
   - Show the PR URL.

6. Merge safely:
   - Run `gh pr merge <number> --merge --delete-branch`.
   - If the merge fails because checks are failing, conflicts exist, or review is required, stop and report the blocker.
   - Never force-merge.

7. Update local main:
   - Switch to `main`.
   - Pull the latest `main`.

8. Delete the local branch:
   - Run `git branch -d <branch>`.
   - If safe deletion fails, do not use `-D`; report the reason and let the user decide.

9. Confirm final state:
   - Run `git status --short --branch`.
   - Run `git branch --list`.
   - Confirm the worktree is clean and on `main`.

## Error Handling

- If the branch has no commits ahead of `main`, stop and say there is nothing to ship.
- If the selected reviewer binary (`codex` in Claude Code, `claude` elsewhere) is not on PATH, stop with a clear error - do not silently skip the review gate.
- If the reviewer exits non-zero, stop and report the failure - do not push.
- If `gh` is not authenticated or available, stop and report the exact blocker.
- If the remote branch was already deleted by the merge step, skip remote deletion silently.

## Command Notes

- Follow the active agent and project shell rules.
- Use non-interactive git commands whenever possible.
- Do not run destructive commands unless the user explicitly asks for them.
