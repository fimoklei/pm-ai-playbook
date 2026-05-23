#!/usr/bin/env bash
# Detect Intent Layer state in a project
# Usage: ./detect_state.sh [path]
# Returns whether root context exists and which supported mode is present.

set -e

TARGET_PATH="${1:-.}"

HAS_AGENTS=false
HAS_CLAUDE=false
HAS_ADAPTER=false
HAS_INTENT_SECTION=false
CHILD_NODES=()

# Find root context files
if [ -f "$TARGET_PATH/AGENTS.md" ]; then
    HAS_AGENTS=true
fi

if [ -f "$TARGET_PATH/CLAUDE.md" ]; then
    HAS_CLAUDE=true
    if grep -q "@AGENTS.md" "$TARGET_PATH/CLAUDE.md" 2>/dev/null; then
        HAS_ADAPTER=true
    fi
fi

# Check for Intent Layer section
for root_file in AGENTS.md CLAUDE.md; do
    if [ -f "$TARGET_PATH/$root_file" ] && grep -q "## Intent Layer" "$TARGET_PATH/$root_file" 2>/dev/null; then
        HAS_INTENT_SECTION=true
    fi
done

# Find child AGENTS.md files
while IFS= read -r file; do
    CHILD_NODES+=("$file")
done < <(find "$TARGET_PATH" -name "AGENTS.md" -not -path "$TARGET_PATH/AGENTS.md" -not -path "*/node_modules/*" 2>/dev/null)

# Output state
echo "=== Intent Layer State ==="
echo "has_agents_md: $HAS_AGENTS"
echo "has_claude_md: $HAS_CLAUDE"
echo "claude_adapter_imports_agents: $HAS_ADAPTER"
echo "has_intent_section: $HAS_INTENT_SECTION"
echo "child_nodes: ${#CHILD_NODES[@]}"

for node in "${CHILD_NODES[@]}"; do
    echo "  - $node"
done

echo ""
if [ "$HAS_AGENTS" = false ] && [ "$HAS_CLAUDE" = false ]; then
    echo "state: none"
    echo "mode: none"
    echo "action: choose AGENTS.md only, CLAUDE.md only, or AGENTS.md canonical + CLAUDE.md adapter"
elif [ "$HAS_INTENT_SECTION" = false ]; then
    echo "state: partial"
    if [ "$HAS_AGENTS" = true ] && [ "$HAS_CLAUDE" = true ] && [ "$HAS_ADAPTER" = false ]; then
        echo "mode: parallel root files"
        echo "action: clarify canonical source; prefer AGENTS.md canonical + thin CLAUDE.md adapter"
    elif [ "$HAS_AGENTS" = true ] && [ "$HAS_CLAUDE" = true ]; then
        echo "mode: AGENTS.md canonical + CLAUDE.md adapter"
        echo "action: add Intent Layer section to AGENTS.md"
    elif [ "$HAS_AGENTS" = true ]; then
        echo "mode: AGENTS.md only"
        echo "action: add Intent Layer section to AGENTS.md"
    else
        echo "mode: CLAUDE.md only"
        echo "action: add Intent Layer section to CLAUDE.md"
    fi
else
    echo "state: complete"
    if [ "$HAS_AGENTS" = true ] && [ "$HAS_CLAUDE" = true ] && [ "$HAS_ADAPTER" = true ]; then
        echo "mode: AGENTS.md canonical + CLAUDE.md adapter"
    elif [ "$HAS_AGENTS" = true ] && [ "$HAS_CLAUDE" = true ]; then
        echo "mode: parallel root files"
        echo "warning: both root files exist without an @AGENTS.md adapter import; check for duplicated or conflicting instructions"
    elif [ "$HAS_AGENTS" = true ]; then
        echo "mode: AGENTS.md only"
    else
        echo "mode: CLAUDE.md only"
    fi
    echo "action: maintenance mode (audit/candidates/both)"
fi
