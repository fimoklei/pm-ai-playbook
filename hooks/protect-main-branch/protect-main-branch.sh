#!/bin/bash
# Prevents direct commits to main/master and force-pushes.
# Repos with .claude/allow-main-commits get smart mode:
#   only commits touching protected paths are blocked.
# PreToolUse hook — reads tool input from stdin JSON.

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
SESSION_CWD=$(echo "$INPUT" | jq -r '.cwd // empty')

# Resolve effective cwd: an inline `cd <path>` in the command wins, otherwise the
# session cwd. This matters because the agent often runs `cd /other/repo && git commit`
# while the session sits in a different repo on `main` — without this, the hook
# inspects the wrong repo's branch and blocks unrelated commits.
EFFECTIVE_CWD=$(echo "$COMMAND" | grep -oE '(^|[;&|]+[[:space:]]*)cd[[:space:]]+[^&|;]+' | tail -1 | sed -E 's/^.*cd[[:space:]]+//' | xargs)
EFFECTIVE_CWD="${EFFECTIVE_CWD/#\~/$HOME}"
if [ -z "$EFFECTIVE_CWD" ] || [ ! -d "$EFFECTIVE_CWD" ]; then
  EFFECTIVE_CWD="$SESSION_CWD"
fi

BRANCH=$(git -C "$EFFECTIVE_CWD" branch --show-current 2>/dev/null)

# Only care about main/master
if [ "$BRANCH" != "main" ] && [ "$BRANCH" != "master" ]; then
  exit 0
fi

REPO_ROOT=$(git -C "$EFFECTIVE_CWD" rev-parse --show-toplevel 2>/dev/null)

# Block: git commit on main
if echo "$COMMAND" | grep -qE '(^|[;&|]+[[:space:]]*)git[[:space:]]+commit\b'; then

  # Smart mode: marker file present → only block if protected paths are staged
  if [ -f "$REPO_ROOT/.claude/allow-main-commits" ]; then
    # Check already-staged files
    STAGED=$(git -C "$EFFECTIVE_CWD" diff --cached --name-only 2>/dev/null)
    # Also parse paths from 'git add' in chained commands (git add X && git commit)
    # This catches the PreToolUse race: git add hasn't run yet when hook fires
    ADD_PATHS=$(echo "$COMMAND" | grep -oE 'git add [^&|;]+' | sed 's/git add //' | tr ' ' '\n')
    ALL_PATHS=$(printf '%s\n%s' "$STAGED" "$ADD_PATHS" | sort -u)

    PROTECTED=false
    while IFS= read -r file; do
      [ -z "$file" ] && continue
      case "$file" in
        .claude/*|06-system/*)
          PROTECTED=true
          break
          ;;
      esac
    done <<< "$ALL_PATHS"

    if [ "$PROTECTED" != "true" ]; then
      exit 0  # Content-only commit, allow it
    fi

    # Protected paths staged — block with specific message
    jq -n '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: "BLOCKED: Commit touches protected paths (.claude/ or 06-system/). Create a branch first: git checkout -b feature/<description> (or fix/<description>, chore/<description>)."
      }
    }'
    exit 2
  fi

  # Default mode: no marker file → block all commits on main
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "BLOCKED: Cannot commit directly to main. Create a branch first: git checkout -b feature/<description> (or fix/<description>, chore/<description>)."
    }
  }'
  exit 2
fi

# Block: git push --force on main (unconditional — no repo gets a pass)
if echo "$COMMAND" | grep -qE '(^|[;&|]+[[:space:]]*)git[[:space:]]+push\b[^;&|]*(--force\b|-f\b)'; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "BLOCKED: Force-push to main is not allowed. This rewrites shared history."
    }
  }'
  exit 2
fi

exit 0
