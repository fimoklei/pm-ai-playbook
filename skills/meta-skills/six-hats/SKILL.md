---
name: six-hats
description: "Structured six-hats thinking sessions for debating decisions. Use when user says \"six hats\", \"six hats debate\", or wants to explore a decision through six colored-perspective lenses in sequential rounds with a final recommendation."
---
# Six Hats Debate Skill

## How It Works

1. **User submits the topic** — paste the decision, plan, or question in chat.
2. **User specifies output path** — e.g. `Projects/my-debate/` or any path.
3. **Skill runs 3 rounds** of sequential debate, one hat at a time.
4. **Blue hat moderates** — summarizes and provides the final recommendation.
5. **Summary written to `{output_path}/debate-{timestamp}.md`**.

---

## The Six Hats

| Hat | Role | Focus |
|-----|------|-------|
| **White** | Facts & Information | What do we know? What's unknown? What data exists? |
| **Red** | Emotion & Intuition | Gut feelings, hunches, what feels wrong even without evidence |
| **Yellow** | Optimism & Benefits | Why could this work? What's the best outcome? |
| **Black** | Caution & Risks | What could go wrong? What are the failure modes? |
| **Green** | Creativity & Alternatives | New ideas, different approaches, lateral thinking |
| **Blue** | Process & Moderation | Orchestrates the debate, manages time, writes final summary |

---

## Debate Rules

- Each hat speaks **sequentially**: White → Red → Yellow → Black → Green → Blue
- **Round 1**: Each hat responds to the original topic
- **Round 2**: Each hat sees Round 1 output and can counter, amplify, or concede
- **Round 3**: Final statements — hats can shift positions based on the debate
- **Blue hat** does not contribute opinions during rounds; only moderates and summarizes at the end

---

## Output Format

```markdown
# Six Hats Debate: {topic}

**Date**: {timestamp}
**Rounds**: 3

---

## Final Recommendation (Blue Hat)

*Synthesized conclusion and recommended course of action.*

---

## Round 1

### White Hat
{facts and information}

### Red Hat
{emotion and intuition}

### Yellow Hat
{optimism and benefits}

### Black Hat
{caution and risks}

### Green Hat
{creativity and alternatives}

---

## Round 2

{...same structure...}

## Round 3

{...same structure...}

---

## Raw Debate Data

{all hat statements in order, unfiltered}
```

---

## Workflow

1. Read this SKILL.md
2. Ask user for the **topic** and **output path**
3. Run Round 1 — prompt each hat sequentially, collect responses
4. Run Round 2 — feed Round 1 back to each hat, collect responses
5. Run Round 3 — feed Round 2 back to each hat, collect responses
6. Blue hat synthesizes → writes final recommendation
7. Write complete debate file to `{output_path}/debate-{timestamp}.md`
8. Report file path to user

---

## Hat Prompt Templates

### White Hat (Facts)
```
You are the White Hat in a structured six-hats debate.
Topic: {topic}
Round: {n}
Previous positions: {prev_hats_output}

Focus: Facts, data, known information, gaps in knowledge.
Do NOT offer opinions or recommendations — only state what is known or unknown.

Your response should be 2-4 paragraphs.
```

### Red Hat (Emotion)
```
You are the Red Hat in a structured six-hats debate.
Topic: {topic}
Round: {n}
Previous positions: {prev_hats_output}

Focus: Gut feelings, emotional reactions, intuition without justification.
Speak from emotion — no need to rationalize.

Your response should be 2-4 paragraphs.
```

### Yellow Hat (Optimism)
```
You are the Yellow Hat in a structured six-hats debate.
Topic: {topic}
Round: {n}
Previous positions: {prev_hats_output}

Focus: Why this could work, best-case scenarios, benefits and value.
Be genuinely optimistic but ground it in logic.

Your response should be 2-4 paragraphs.
```

### Black Hat (Caution)
```
You are the Black Hat in a structured six-hats debate.
Topic: {topic}
Round: {n}
Previous positions: {prev_hats_output}

Focus: Risks, failure modes, why this could go wrong.
Be a devil's advocate — identify the sharpest objections.

Your response should be 2-4 paragraphs.
```

### Green Hat (Creativity)

```
You are the Green Hat in a structured six-hats debate.
Topic: {topic}
Round: {n}
Previous positions: {prev_hats_output}

Focus: New ideas, alternatives, lateral thinking.
Build on previous arguments or introduce entirely new angles.

Your response should be 2-4 paragraphs.
```

### Blue Hat (Moderation)
```
You are the Blue Hat — the moderator and synthesizer.
Topic: {topic}
Previous positions: {prev_hats_output}

You have watched 3 rounds of debate. Now provide:
1. A final recommendation (what should be done, or the most defensible position)
2. Key points of agreement across hats
3. Key unresolved tensions
4. Suggested next steps or deeper questions

Format your final recommendation prominently. After that, include the raw debate summary.

Your response should be 4-6 paragraphs.
```

---

## Notes

- Do not run hats in parallel — sequential builds better debate momentum
- If the topic is too vague, ask the user to clarify before starting
- Each round must complete fully before moving to the next round
- Always write the output file — do not skip this step
