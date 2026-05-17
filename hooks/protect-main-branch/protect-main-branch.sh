#!/bin/bash
# Prevents direct commits to main/master and force-pushes.
# Repos with .claude/allow-main-commits get smart mode:
#   only commits touching protected paths are blocked.
# PreToolUse hook — reads tool input from stdin JSON.

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
SESSION_CWD=$(echo "$INPUT" | jq -r '.cwd // empty')

deny() {
  local reason="$1"
  jq -n --arg reason "$reason" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: $reason
    }
  }'
  exit 2
}

# Resolve effective cwd: an inline `cd <path>` in the command wins, otherwise the
# session cwd. This matters because the agent often runs `cd /other/repo && git commit`
# while the session sits in a different repo on `main` — without this, the hook
# inspects the wrong repo's branch and blocks unrelated commits.
EFFECTIVE_CWD=$(echo "$COMMAND" | sed -nE 's/(^|.*[;&|][[:space:]]*)cd[[:space:]]+"([^"]+)".*/\2/p' | tail -1)
if [ -z "$EFFECTIVE_CWD" ]; then
  EFFECTIVE_CWD=$(echo "$COMMAND" | sed -nE "s/(^|.*[;&|][[:space:]]*)cd[[:space:]]+'([^']+)'.*/\\2/p" | tail -1)
fi
if [ -z "$EFFECTIVE_CWD" ]; then
  EFFECTIVE_CWD=$(echo "$COMMAND" | grep -oE '(^|[;&|]+[[:space:]]*)cd[[:space:]]+[^&|;]+' | tail -1 | sed -E 's/^.*cd[[:space:]]+//; s/^[[:space:]]+//; s/[[:space:]]+$//')
fi
EFFECTIVE_CWD="${EFFECTIVE_CWD/#\~/$HOME}"
if [ -z "$EFFECTIVE_CWD" ] || [ ! -d "$EFFECTIVE_CWD" ]; then
  EFFECTIVE_CWD="$SESSION_CWD"
fi

IS_COMMIT=$(echo "$COMMAND" | grep -qE '(^|[;&|]+[[:space:]]*)git[[:space:]]+commit\b' && echo true || echo false)
IS_FORCE_PUSH=$(echo "$COMMAND" | grep -qE '(^|[;&|]+[[:space:]]*)git[[:space:]]+push\b[^;&|]*(--force($|[=[:space:]])|-f([[:space:]]|$))' && echo true || echo false)

if [ -z "$EFFECTIVE_CWD" ] || [ ! -d "$EFFECTIVE_CWD" ]; then
  if [ "$IS_COMMIT" = "true" ] || [ "$IS_FORCE_PUSH" = "true" ]; then
    deny "BLOCKED: Cannot determine repository cwd for a protected git command. Run from a valid repo cwd or include an explicit cd <repo> first."
  fi
  exit 0
fi

BRANCH=$(git -C "$EFFECTIVE_CWD" branch --show-current 2>/dev/null)
REPO_ROOT=$(git -C "$EFFECTIVE_CWD" rev-parse --show-toplevel 2>/dev/null)

if [ -z "$REPO_ROOT" ]; then
  if [ "$IS_COMMIT" = "true" ] || [ "$IS_FORCE_PUSH" = "true" ]; then
    deny "BLOCKED: Cannot determine git repository root for a protected git command."
  fi
  exit 0
fi

# Only care about main/master
if [ "$BRANCH" != "main" ] && [ "$BRANCH" != "master" ]; then
  exit 0
fi

# Block: git commit on main
if [ "$IS_COMMIT" = "true" ]; then

  # Smart mode: marker file present → only block if protected paths are staged
  if [ -f "$REPO_ROOT/.claude/allow-main-commits" ]; then
    # Check already-staged files
    STAGED=$(git -C "$EFFECTIVE_CWD" diff --cached --name-only 2>/dev/null)
    # Also parse paths from 'git add' in chained commands (git add X && git commit)
    # This catches the PreToolUse race: git add hasn't run yet when hook fires
    ADD_PATHS=$(echo "$COMMAND" | grep -oE 'git add [^&|;]+' | sed 's/git add //' | tr ' ' '\n')
    STATUS_PATHS=""
    if echo "$ADD_PATHS" | grep -qE '^(-A|--all|\.|:/$)$'; then
      STATUS_PATHS=$(git -C "$EFFECTIVE_CWD" status --porcelain --untracked-files=all 2>/dev/null | sed -E 's/^...//')
    fi
    ALL_PATHS=$(printf '%s\n%s\n%s' "$STAGED" "$ADD_PATHS" "$STATUS_PATHS" | sort -u)

    PROTECTED=false
    while IFS= read -r file; do
      [ -z "$file" ] && continue
      case "$file" in
        .|:/.|:/|./.claude|./.claude/*|.claude|.claude/*|./06-system|./06-system/*|06-system|06-system/*)
          PROTECTED=true
          break
          ;;
      esac
    done <<< "$ALL_PATHS"

    if [ "$PROTECTED" != "true" ]; then
      exit 0  # Content-only commit, allow it
    fi

    # Protected paths staged — block with specific message
    deny "BLOCKED: Commit touches protected paths (.claude/ or 06-system/). Create a branch first: git checkout -b feature/<description> (or fix/<description>, chore/<description>)."
  fi

  # Default mode: no marker file → block all commits on main
  deny "BLOCKED: Cannot commit directly to main. Create a branch first: git checkout -b feature/<description> (or fix/<description>, chore/<description>)."
fi

# Block: git push --force on main (unconditional — no repo gets a pass)
if [ "$IS_FORCE_PUSH" = "true" ]; then
  deny "BLOCKED: Force-push to main is not allowed. This rewrites shared history."
fi

exit 0
