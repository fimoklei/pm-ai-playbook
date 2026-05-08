---
name: kiro-intent
description: Pre-discovery intent exploration for genuinely vague ideas. Use when the user pitches an idea where the real user-need, problem framing, or core assumptions are unclear — before /kiro-discovery. Delegates to the intent-explorer skill, which produces .kiro/specs/<slug>/intent-spec.md. The output is auto-detected by /kiro-discovery and downstream spec skills, so the user does not need to pass intent context as an argument. Skip this skill entirely when the user already has a clear problem statement.
disable-model-invocation: true
allowed-tools: Skill, Read
argument-hint: <vague-idea-or-problem>
---

# kiro-intent Skill

## Purpose

Optional upstream filter for `/kiro-discovery`. Activates intent-driven exploration (JTBD, first principles, cross-pollination) when the idea is too unformed for discovery's boundary-oriented interview to be productive.

## When to Use

- User pitches a feature without a clear problem statement
- Stakeholders disagree on what is being built
- Idea sounds like a solution masquerading as a problem ("we need a dashboard")
- High-stakes decisions where getting intent wrong is costly

## When NOT to Use

- User already has a sharp problem statement, target user, and outcome
- Bug fixes, config changes, refactors (use `/kiro-discovery` directly, or skip to direct implementation)
- An `intent-spec.md` already exists for this feature

## Execution

1. Verify the `intent-explorer` skill is available. If not, surface a clear message:
   > "kiro-intent depends on the global `intent-explorer` skill (~/.claude/skills/intent-explorer/). Install it, or skip this step and run `/kiro-discovery` directly."
   Stop on missing dependency.
2. Invoke the `intent-explorer` skill via the Skill tool with `args: $ARGUMENTS`.
3. The intent-explorer drives the conversation through Quick or Deep mode, ending by writing `.kiro/specs/<slug>/intent-spec.md`.
4. After the intent-spec.md is written, suggest the next command:
   > "Intent captured. Run `/kiro-discovery <idea>` — it will detect the intent-spec.md and skip overlapping questions."

## Hand-off Contract

This skill writes nothing itself. The intent-explorer writes `.kiro/specs/<slug>/intent-spec.md`. `/kiro-discovery` and downstream skills auto-detect this file via filesystem glob — no flags, no markers, no arguments needed. File-existence is the source of truth.

## Critical Constraints

- Do not duplicate intent-explorer methodology here — single source of truth lives in the global skill
- Do not write any files from this skill — delegation only
- Do not auto-trigger; this skill is `disable-model-invocation: true` because intent exploration is a deliberate user choice, not something Claude should start unilaterally
