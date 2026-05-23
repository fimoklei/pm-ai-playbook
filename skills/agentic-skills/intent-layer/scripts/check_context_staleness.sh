#!/usr/bin/env bash
# Flag context files that may be stale compared with code movement.
# Usage: ./check_context_staleness.sh [path]

set -e

TARGET_PATH="${1:-.}"

if ! git -C "$TARGET_PATH" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "UNKNOWN: git history unavailable"
    echo "- Target: $TARGET_PATH"
    echo "- Recommendation: inspect context freshness manually"
    exit 0
fi

REPO_ROOT=$(git -C "$TARGET_PATH" rev-parse --show-toplevel)
cd "$REPO_ROOT"

mtime() {
    if stat -f %m "$1" >/dev/null 2>&1; then
        stat -f %m "$1"
    else
        stat -c %Y "$1"
    fi
}

context_timestamp() {
    context_file="$1"
    ts=$(git log -1 --format=%ct -- "$context_file" 2>/dev/null || true)
    if [ -n "$ts" ]; then
        echo "$ts"
    else
        mtime "$context_file"
    fi
}

context_date() {
    ts="$1"
    if date -r "$ts" "+%Y-%m-%d" >/dev/null 2>&1; then
        date -r "$ts" "+%Y-%m-%d"
    else
        date -d "@$ts" "+%Y-%m-%d"
    fi
}

days_since() {
    ts="$1"
    now=$(date +%s)
    echo $(( (now - ts) / 86400 ))
}

is_ignored_dir_path() {
    path="$1"
    case "$path" in
        */node_modules/*|node_modules/*|*/.git/*|.git/*|*/dist/*|dist/*|*/build/*|build/*|*/.next/*|.next/*|*/__pycache__/*|__pycache__/*)
            return 0
            ;;
    esac
    return 1
}

is_lockfile() {
    path="$1"
    case "$path" in
        *package-lock.json|*pnpm-lock.yaml|*yarn.lock|*bun.lockb|*Cargo.lock|*poetry.lock|*Pipfile.lock)
            return 0
            ;;
    esac
    return 1
}

is_critical_path() {
    path="$1"
    case "$path" in
        *auth*|*payment*|*payments*|*billing*|*permission*|*security*|*migration*|*migrations*|*.github/workflows/*|*deploy*|*infra*)
            return 0
            ;;
    esac
    return 1
}

context_files=$(find "$TARGET_PATH" \
    \( -name "AGENTS.md" -o -name "CLAUDE.md" \) \
    -not -path "*/node_modules/*" \
    -not -path "*/.git/*" \
    -not -path "*/dist/*" \
    -not -path "*/build/*" \
    -not -path "*/.next/*" \
    2>/dev/null | sort)

if [ -z "$context_files" ]; then
    echo "UNKNOWN: no AGENTS.md or CLAUDE.md files found"
    echo "- Target: $TARGET_PATH"
    echo "- Recommendation: create a root context file before checking staleness"
    exit 0
fi

echo "=== Context Staleness Check ==="
echo "Target: $TARGET_PATH"
echo ""

printf '%s\n' "$context_files" | while IFS= read -r context_file; do
    [ -n "$context_file" ] || continue

    governed_dir=$(dirname "$context_file")
    context_ts=$(context_timestamp "$context_file")
    last_update=$(context_date "$context_ts")
    age_days=$(days_since "$context_ts")
    governs_dependencies=false
    if grep -qiE "dependencies|dependency|package manager|lockfile|lock file" "$context_file" 2>/dev/null; then
        governs_dependencies=true
    fi

    changed_files_raw=$(
        {
            git log --since="@$context_ts" --name-only --pretty=format: -- "$governed_dir" 2>/dev/null
            git diff --name-only -- "$governed_dir" 2>/dev/null
            git diff --cached --name-only -- "$governed_dir" 2>/dev/null
        } | sort -u
    )
    changed_files=""
    changed_count=0
    critical_count=0

    if [ -n "$changed_files_raw" ]; then
        while IFS= read -r changed_file; do
            [ -n "$changed_file" ] || continue
            [ "$changed_file" = "$context_file" ] && continue
            if is_ignored_dir_path "$changed_file"; then
                continue
            fi
            if is_lockfile "$changed_file" && [ "$governs_dependencies" = false ]; then
                continue
            fi
            changed_files="${changed_files}${changed_file}
"
            changed_count=$((changed_count + 1))
            if is_critical_path "$changed_file"; then
                critical_count=$((critical_count + 1))
            fi
        done <<EOF
$changed_files_raw
EOF
    fi

    commit_count=$(git log --since="@$context_ts" --format=%H -- "$governed_dir" 2>/dev/null | sort -u | wc -l | tr -d ' ')

    risk="LOW"
    recommendation="context appears current enough; review during normal maintenance"
    if [ "$changed_count" -ge 40 ] || [ "$commit_count" -ge 15 ] || [ "$critical_count" -ge 3 ]; then
        risk="HIGH RISK"
        recommendation="audit this context node before trusting it"
    elif [ "$changed_count" -ge 10 ] || [ "$commit_count" -ge 5 ] || [ "$critical_count" -ge 1 ]; then
        risk="MEDIUM RISK"
        recommendation="review verification commands and invariants"
    fi

    echo "$risk: $context_file"
    echo "- Governs: $governed_dir"
    echo "- Last context update: $last_update ($age_days days ago)"
    echo "- Files changed since then: $changed_count"
    echo "- Recent commits: $commit_count"
    if [ "$critical_count" -gt 0 ]; then
        echo "- Critical-looking paths changed: $critical_count"
    fi
    echo "- Recommendation: $recommendation"
    echo ""
done
