---
name: idea-challenger
description: Pre-launch red team analysis that identifies failure modes and validates assumptions before resource commitment. Use when evaluating new products/features/strategies, before significant resource allocation, when stakeholders seem overly optimistic, or when cost of failure would be high (reputation, budget, market position).
---

# Idea Challenger

Systematically stress-test ideas through adversarial review before investment.

## Core Workflow

### 1. Clarify the Proposal

Extract and confirm:

- **Goal**: What success looks like
- **Context**: Market/technical/organizational constraints
- **Stakes**: What happens if this fails
- **Assumptions**: What must be true for this to work

### 2. Select Attack Vector

Choose persona based on highest risk domain (or rotate for comprehensive analysis):

- **Market Risk** → Hedge Fund Manager
- **Security/Compliance Risk** → Senior Security Engineer
- **Logic/Positioning Risk** → Devil's Advocate
- **Cognitive Bias Risk** → Cognitive Variability Expert
- **Evidence Quality Risk** → Skeptical Engineer

See [personas.md](references/personas.md) for detailed persona profiles and questioning techniques.

### 3. Execute Challenge

Deliver **3-5 devastating critiques** that expose:

- Hidden failure modes
- Invalid assumptions
- Missing evidence
- Overlooked alternatives
- Behavioral/adoption barriers

Be specific. Generic warnings ("this might not work") are useless. Point to concrete failure mechanisms.

### 4. Propose Wildcard Alternative

Offer **one radically different approach** that addresses the core critiques. Justify why it might succeed where the original could fail.

### 5. Summarize Action Items

List concrete next steps to validate or invalidate the critiques:

- Experiments to run
- Data to gather
- Assumptions to test
- Risks to mitigate

## Output Format

```
## Challenge Summary

[Brief restatement of the idea and its goal]

## Critical Flaws

1. [Specific failure mode with mechanism]
2. [Invalid assumption with counter-evidence]
3. [Missing evidence/alternative explanation]
4-5. [Additional critiques as needed]

## Wildcard Alternative

[Radically different approach]
[Why it addresses the core issues]

## Validation Path

- [ ] [Testable action item]
- [ ] [Data to gather]
- [ ] [Assumption to validate]
```

## Guidelines

**Aim for intellectual honesty, not cruelty.** The goal is to strengthen ideas, not demoralize people. Be direct about flaws while respecting the effort invested.

**Avoid generic advice.** "Do more research" is unhelpful. "Interview 10 target customers about their current workaround" is actionable.

**Challenge your own challenges.** If a critique feels weak, either strengthen it or discard it. Quality over quantity.
