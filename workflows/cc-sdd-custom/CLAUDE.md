# Agentic SDLC and Spec-Driven Development

Kiro-style spec-driven development on an agentic SDLC. Fork of cc-sdd v3 with optional intent-exploration upstream of discovery.

## Project Context

### Paths
- Steering: `.kiro/steering/`
- Specs: `.kiro/specs/`

### Steering vs Specification

**Steering** (`.kiro/steering/`) — guides AI with project-wide rules and context
**Specs** (`.kiro/specs/`) — formalize development process for individual features

### Active Specifications
- Check `.kiro/specs/` for active specifications
- Use `/kiro-spec-status [feature-name]` to check progress

## Development Guidelines
- Think in English, generate responses in English. All Markdown content written to project files (e.g., requirements.md, design.md, tasks.md, research.md, validation reports) MUST be written in the target language configured for this specification (see `spec.json.language`).

## Minimal Workflow

- Phase 0 (optional): `/kiro-steering`, `/kiro-steering-custom`
- Intent (optional, only for vague ideas): `/kiro-intent "idea"` — delegates to global `intent-explorer` skill, writes `.kiro/specs/<slug>/intent-spec.md`. Skip when the idea already has a clear problem statement.
- Discovery: `/kiro-discovery "idea"` — determines action path, writes `brief.md` (+ `roadmap.md` for multi-spec). Auto-detects `intent-spec.md` if present and skips overlapping questions.
- Phase 1 (Specification):
  - Single spec: `/kiro-spec-quick {feature} [--auto]` or step by step:
    - `/kiro-spec-init "description"`
    - `/kiro-spec-requirements {feature}`
    - `/kiro-validate-gap {feature}` (optional: for existing codebase)
    - `/kiro-spec-design {feature} [-y]`
    - `/kiro-validate-design {feature}` (optional: design review)
    - `/kiro-spec-tasks {feature} [-y]`
  - Multi-spec: `/kiro-spec-batch` — creates all specs from `roadmap.md` in parallel by dependency wave
- Phase 2 (Implementation): `/kiro-impl {feature} [tasks]`
  - Without task numbers: autonomous mode (subagent per task + independent review + final validation)
  - With task numbers: manual mode (selected tasks in main context, still reviewer-gated before completion)
  - `/kiro-validate-impl {feature}` (standalone re-validation)
- Progress check: `/kiro-spec-status {feature}` (use anytime)

## Skills Structure
Skills are located in `.claude/skills/kiro-*/SKILL.md`
- Each skill is a directory with a `SKILL.md` file
- Skills run inline with access to conversation context
- Skills may delegate parallel research to subagents for efficiency
- Additional files (templates, examples, rules) can be added to skill directories
- `kiro-review` — task-local adversarial review protocol used by reviewer subagents
- `kiro-debug` — root-cause-first debug protocol used by debugger subagents
- `kiro-verify-completion` — fresh-evidence gate before success or completion claims
- `kiro-intent` — local addition. Optional pre-discovery filter; depends on global `intent-explorer` skill
- **If there is even a 1% chance a skill applies to the current task, invoke it.** Do not skip skills because the task seems simple.

## Development Rules
- 3-phase approval workflow: Requirements → Design → Tasks → Implementation
- Human review required each phase; use `-y` only for intentional fast-track
- Keep steering current and verify alignment with `/kiro-spec-status`
- Follow the user's instructions precisely, and within that scope act autonomously: gather the necessary context and complete the requested work end-to-end in this run, asking questions only when essential information is missing or the instructions are critically ambiguous.

## Steering Configuration
- Load entire `.kiro/steering/` as project memory
- Default files: `product.md`, `tech.md`, `structure.md`
- Custom files are supported (managed via `/kiro-steering-custom`)

## Local Additions vs Upstream cc-sdd v3
- `kiro-intent` skill — delegate-skill calling global `intent-explorer`. `disable-model-invocation: true` (explicit user invocation only).
- `kiro-discovery` patch — Step 1 globs for `intent-spec.md`; Step 4 reads it and skips overlapping questions when present. Non-breaking when intent-spec.md is absent.
- Everything else: byte-identical to upstream v3.0.2.
