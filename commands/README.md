# Commands

Reusable command templates that standardize how we plan and run AI work.

## Table of contents

- [PRD workflow commands](#prd-workflow-commands)
- [Workflow commands](#workflow-commands)

## 📋 PRD workflow commands

Tuned spec-driven-workflow based on [ai-dev-tasks](https://github.com/snarktank/ai-dev-tasks/blob/main/create-prd.md)   

| Name           | Purpose                                                            | When to use                                                  | Link                                               |
| -------------- | ------------------------------------------------------------------ | ------------------------------------------------------------ | -------------------------------------------------- |
| Create PRD     | Generate a clear, actionable PRD in Markdown from a feature prompt | When starting a new feature and need structured requirements | [./prd/create-prd.md](./prd/create-prd.md)         |
| Generate tasks | Create a detailed task list from an existing PRD for developers    | After PRD is approved and you need implementation steps      | [./prd/generate-tasks.md](./prd/generate-tasks.md) |
| Process task   | Process a specific task from the generated task list               | When working through individual implementation tasks         | [./prd/process-task.md](./prd/process-task.md)     |

## ⚡ Workflow commands

| Name                 | Purpose                                                                            | When to use                                                                 | Link                                                                     |
| -------------------- | ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Commit               | Create a smart git commit with lint/test checks and conventional commit formatting | When ready to commit staged or unstaged changes                             | [./workflow/commit.md](./workflow/commit.md)                             |
| Codemaps             | Analyze codebase structure and update architecture documentation                   | When codebase structure changes significantly                               | [./workflow/codemaps.md](./workflow/codemaps.md)                         |
| Health Check         | Run comprehensive environment health check and fix all issues                      | When Claude Code environment shows problems or periodically for maintenance | [./workflow/health-check.md](./workflow/health-check.md)                 |
| Learning opportunity | Capture and structure learning moments from work                                   | When you discover something worth documenting or teaching                   | [./workflow/learning-opportunity.md](./workflow/learning-opportunity.md) |
| Reflection           | Guide end-of-session reflection for continuous improvement                         | At the end of a work session or project milestone                           | [./workflow/reflection.md](./workflow/reflection.md)                     |
| Ship                 | Push branch, open PR, merge to main, and clean up local + remote branch            | When a feature branch is ready to merge                                     | [./workflow/ship.md](./workflow/ship.md)                                 |
| Skill Create         | Analyze local git history to extract coding patterns and generate SKILL.md files   | When wanting to create skills from repository patterns                      | [./workflow/skill-create.md](./workflow/skill-create.md)                 |
