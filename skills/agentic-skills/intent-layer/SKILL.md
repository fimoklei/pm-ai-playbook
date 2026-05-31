---
name: intent-layer
description: >
  Use when initializing or maintaining agent-friendly repo context, setting up AGENTS.md
  or CLAUDE.md, adding local rules, defining verification commands, or checking whether
  context files are stale.
---

# Intent Layer

Context infrastructure that helps agents find local rules, understand ownership boundaries, verify changes, and notice when context may be stale.

## Root Context Strategy

Default: use `AGENTS.md` as the canonical cross-agent source. Use `CLAUDE.md` as a thin Claude Code adapter when Claude Code is used.

Supported modes:

| Mode | Use when | Root files |
|------|----------|------------|
| AGENTS.md only | The project wants one portable context surface | `AGENTS.md` |
| CLAUDE.md only | The project is Claude-only and has no cross-agent need | `CLAUDE.md` |
| AGENTS.md canonical + CLAUDE.md adapter | Claude Code is used, but context should stay portable | `AGENTS.md` plus thin `CLAUDE.md` |

Adapter example:

```markdown
@AGENTS.md

## Claude Code Specific Instructions

- Prefer editing existing files over creating new abstractions.
- Use plan mode for large refactors.
- Run local verification commands before final response.
```

Child `AGENTS.md` files in subdirectories are encouraged for complex subsystems. Root adapters should point to canonical context instead of duplicating it.

## Required Root Intent Layer

Add this to the canonical context file at project root: `AGENTS.md` by default, or `CLAUDE.md` in CLAUDE-only mode. In adapter mode, add it to `AGENTS.md`; `CLAUDE.md` imports it.

```markdown
## Intent Layer

**Before modifying code in a subdirectory, read its AGENTS.md first** to understand local patterns and invariants.

- **[Area 1]**: `path/to/AGENTS.md` - Brief description
- **[Area 2]**: `path/to/AGENTS.md` - Brief description

### Global Invariants

- [Invariant that applies across all areas]
- [Another global invariant]
```

This navigation contract is mandatory when child context nodes exist. Extend it with the project's real boundaries and global invariants; do not leave placeholder areas in finalized context.

## Workflow

```
1. Detect state
   scripts/detect_state.sh /path/to/project
   -> Returns: none | partial | complete

2. Route
   none/partial -> Initial setup (steps 3-5)
   complete     -> Maintenance (step 6)

3. Measure [gate - show table first]
   scripts/analyze_structure.sh /path/to/project
   scripts/estimate_tokens.sh /path/to/each/source/dir
   scripts/check_context_staleness.sh /path/to/project

4. Decide
   No root file        -> Ask which supported mode to use
   Existing root files -> Preserve intent; add adapter/import only if useful
   Child nodes needed  -> Add local AGENTS.md files with verification commands

5. Execute
   Add the Required Root Intent Layer to the canonical root context file
   Use references/templates.md for structure
   Use references/node-examples.md for real-world patterns
   Validate: canonical source is clear, READ-FIRST directive exists, every node has Verification, <4k tokens per node

6. Maintenance mode (when state=complete)
   Ask user:
   a) Audit nodes     -> Use references/capture-protocol.md for SME questions
   b) Find candidates -> Re-measure tokens, suggest new nodes
   c) Staleness check -> Run scripts/check_context_staleness.sh
   d) Both/all
```

## When to Create Child Nodes

| Signal | Action |
|--------|--------|
| >20k tokens in directory | Create AGENTS.md |
| Responsibility shift | Create AGENTS.md |
| Hidden contracts/invariants | Document in nearest ancestor |
| Cross-cutting concern | Place at LCA |

Do NOT create for: every directory, simple utilities, test folders (unless complex).

## Staleness Risk Levels

`scripts/check_context_staleness.sh` uses git history as a review trigger, not as proof that context is wrong.

| Level | Meaning | Action |
|-------|---------|--------|
| LOW | Little code movement since the context update | Review during normal maintenance |
| MEDIUM | Meaningful movement or one critical-looking path changed | Review verification commands and invariants |
| HIGH | Heavy movement, many commits, or several critical-looking paths changed | Audit before trusting the node |
| UNKNOWN | Git history or context files are unavailable | Inspect freshness manually |

## Capture Questions

When documenting existing code, ask:
1. What does this area own? What's out of scope?
2. What invariants must never be violated?
3. What repeatedly confuses new engineers?
4. What patterns should always be followed?

## Resources

**Scripts:**
- `scripts/detect_state.sh` - Check Intent Layer state (none/partial/complete)
- `scripts/analyze_structure.sh` - Find semantic boundaries
- `scripts/estimate_tokens.sh` - Measure directory complexity
- `scripts/check_context_staleness.sh` - Flag context nodes with code movement since their last update

**References:**
- `references/templates.md` - Root and child node templates
- `references/node-examples.md` - Real-world examples
- `references/capture-protocol.md` - SME interview protocol
