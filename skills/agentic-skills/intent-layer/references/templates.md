# Intent Layer Templates

## Root Context Templates

### AGENTS.md Canonical Root

```markdown
# Project Context

This is the canonical cross-agent context file.

## Intent Layer

**Before modifying code in a subdirectory, read its AGENTS.md first** to understand local patterns and invariants.

- **[Area 1]**: `path/to/AGENTS.md` - Brief description
- **[Area 2]**: `path/to/AGENTS.md` - Brief description

### Global Invariants

- [Invariant that applies across all areas]
- [Another global invariant]

### Verification

| Change type | Required command | Notes |
|---|---|---|
| API behavior | `pnpm test:api` | Required before final response |
| UI component | `pnpm test:ui` | Use when touching components |
| Type changes | `pnpm typecheck` | Required for shared types |
| Build-impacting changes | `pnpm build` | Required before PR |

### Definition of Done

- Relevant tests pass.
- Typecheck passes where applicable.
- No public API changed without docs update.
- No schema change without migration.
- No new abstraction unless existing patterns are insufficient.
```

### CLAUDE.md Thin Adapter

Use when Claude Code is used and `AGENTS.md` is canonical:

```markdown
@AGENTS.md

## Claude Code Specific Instructions

- Prefer editing existing files over creating new abstractions.
- Use plan mode for large refactors.
- Run local verification commands before final response.
```

## Child Node Template

Each AGENTS.md in subdirectories:

```markdown
# {Area Name}

## Purpose
[1-2 sentences: what this area owns, what it explicitly doesn't do]

## Entry Points
- `main_api.ts` - Primary API surface
- `cli.ts` - CLI commands

## Contracts & Invariants
- All DB calls go through `./db/client.ts`
- Never import from `./internal/` outside this directory

## Patterns
To add a new endpoint:
1. Create handler in `./handlers/`
2. Register in `./routes.ts`
3. Add types to `./types.ts`

## Anti-patterns
- Never call external APIs directly; use `./clients/`
- Don't bypass validation layer
- Do not write weak verification instructions like "run tests", "make sure it works", or "follow best practices"

## Verification

| Change type | Required command | Notes |
|---|---|---|
| API behavior | `pnpm test:api` | Required before final response |
| UI component | `pnpm test:ui` | Use when touching components |
| Type changes | `pnpm typecheck` | Required for shared types |
| Build-impacting changes | `pnpm build` | Required before PR |

## Definition of Done

- Relevant tests pass.
- Typecheck passes where applicable.
- No public API changed without docs update.
- No schema change without migration.
- No new abstraction unless existing patterns are insufficient.

## Related Context
- Database layer: `./db/AGENTS.md`
- Shared utilities: `../shared/AGENTS.md`
```

## Verification Examples

Commands must be concrete and copy-pastable. Replace the examples with the real project commands before finalizing a context node.

### Node/TypeScript

| Change type | Required command | Notes |
|---|---|---|
| Type changes | `pnpm typecheck` | Required for shared packages |
| Unit behavior | `pnpm test -- --runInBand` | Use local package test command if narrower |
| Build-impacting changes | `pnpm build` | Required before PR |

### Python

| Change type | Required command | Notes |
|---|---|---|
| Unit behavior | `pytest` | Narrow to `pytest tests/path` when possible |
| Type changes | `mypy .` | Use only if configured |
| Formatting/lint | `ruff check .` | Include formatter command if separate |

### Monorepo

| Change type | Required command | Notes |
|---|---|---|
| Package-local change | `pnpm --filter <package> test` | Prefer local verification first |
| Shared package change | `pnpm -r typecheck` | Required when shared contracts move |
| Cross-package build | `pnpm -r build` | Required for release-facing changes |

### Frontend App

| Change type | Required command | Notes |
|---|---|---|
| Component behavior | `pnpm test:ui` | Use when touching components |
| Route/page behavior | `pnpm test:e2e` | Required for user journeys |
| Build-impacting changes | `pnpm build` | Required before PR |

### Backend Service

| Change type | Required command | Notes |
|---|---|---|
| API behavior | `pnpm test:api` | Required for endpoint changes |
| Database/schema | `pnpm migrate:test` | Required for migrations |
| Contract changes | `pnpm test:contract` | Required for public API changes |

## Measurements Table Format

```
| Directory        | Tokens | Threshold | Needs Node? |
|------------------|--------|-----------|-------------|
| src/components   | ~30k   | 20-64k    | YES (2-3k)  |
| src/pages        | ~22k   | 20-64k    | YES (2-3k)  |
| src/lib          | ~8k    | <20k      | NO          |
```

Thresholds:
- <20k tokens -> No node needed
- 20-64k tokens -> 2-3k token node
- >64k tokens -> Split into child nodes
