# Rules

Rules for CLAUDE.md files, both globally and project-specific.

## Table of contents

- [Global rules](#global-rules)
- [Project rules](#project-rules)
- [Generic rules](#generic-rules)

## 🌍 Global rules

Templates and enforcement rules for CLAUDE.md files.

| Name              | Purpose                                                               | When to use                                                   | Link                                                                             |
| ----------------- | --------------------------------------------------------------------- | ------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Coding Guidelines | Behavioral guardrails to reduce common LLM coding mistakes            | Apply to all coding work as baseline                          | [./global/coding-guidelines-template.md](./global/coding-guidelines-template.md) |
| TDD Enforcement   | Enforce red-green-refactor discipline and coverage expectations       | When writing or updating code with tests                      | [./global/tdd-enforcement-template.md](./global/tdd-enforcement-template.md)     |
| Debugging         | Systematic debugging process before proposing fixes                   | When encountering bugs, test failures, or unexpected behavior | [./global/debugging-template.md](./global/debugging-template.md)                 |
| Project Template  | Template for project-level rules setup                                | When creating or refreshing project-specific standards        | [./global/project-template.md](./global/project-template.md)                     |
| Global Template   | Template for new global standard docs                                 | When adding a new global standard                             | [./global/global-template.md](./global/global-template.md)                       |
| Token Efficiency  | Context efficiency guidelines — respond with the delta, not the state | When adding context management guidance to a global CLAUDE.md | [./global/token-efficiency-template.md](./global/token-efficiency-template.md)   |

## 📦 Project rules

| Category | Purpose                                               | Files   | Link                                                   |
| -------- | ----------------------------------------------------- | ------- | ------------------------------------------------------ |
| Backend  | API, database, models, and query standards            | 4 files | [./project-rules/backend/](./project-rules/backend/)   |
| Frontend | Components, CSS, accessibility, and responsive design | 4 files | [./project-rules/frontend/](./project-rules/frontend/) |
| Testing  | Testing principles, TDD workflow, and quality gates   | 1 file  | [./project-rules/testing/](./project-rules/testing/)   |
| Workflow | Project organization and file layout                  | 1 file  | [./project-rules/workflow/](./project-rules/workflow/) |

### Backend rules

| Name                | Purpose                                               | When to use                         | Link                                                                           |
| ------------------- | ----------------------------------------------------- | ----------------------------------- | ------------------------------------------------------------------------------ |
| API Standards       | REST conventions, versioning, request/response format | When designing or implementing APIs | [./project-rules/backend/api.md](./project-rules/backend/api.md)               |
| Database Migrations | Schema changes, zero-downtime deployments, safety     | When modifying database schema      | [./project-rules/backend/migrations.md](./project-rules/backend/migrations.md) |
| Data Models         | Schema integrity, relationships, TypeScript types     | When defining data structures       | [./project-rules/backend/models.md](./project-rules/backend/models.md)         |
| Database Queries    | Security, performance, optimization patterns          | When writing database operations    | [./project-rules/backend/queries.md](./project-rules/backend/queries.md)       |

### Frontend rules

| Name              | Purpose                                            | When to use                              | Link                                                                                   |
| ----------------- | -------------------------------------------------- | ---------------------------------------- | -------------------------------------------------------------------------------------- |
| Accessibility     | Semantic HTML, ARIA, focus management, motion      | When building accessible UI components   | [./project-rules/frontend/accessibility.md](./project-rules/frontend/accessibility.md) |
| UI Components     | Design principles, state management, consistency   | When creating or organizing components   | [./project-rules/frontend/components.md](./project-rules/frontend/components.md)       |
| CSS               | Methodology, design tokens, utility-first patterns | When writing or organizing styles        | [./project-rules/frontend/css.md](./project-rules/frontend/css.md)                     |
| Responsive Design | Mobile-first, breakpoints, touch optimization      | When designing for multiple screen sizes | [./project-rules/frontend/responsive.md](./project-rules/frontend/responsive.md)       |

### Testing rules

| Name    | Purpose                                           | When to use                      | Link                                                                     |
| ------- | ------------------------------------------------- | -------------------------------- | ------------------------------------------------------------------------ |
| Testing | TDD workflow, test types, coverage, quality gates | When writing or organizing tests | [./project-rules/testing/testing.md](./project-rules/testing/testing.md) |

### Workflow rules

| Name                | Purpose                              | When to use                                       | Link                                                                                               |
| ------------------- | ------------------------------------ | ------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Directory Structure | Project organization and file layout | When setting up or reorganizing project structure | [./project-rules/workflow/directory-structure.md](./project-rules/workflow/directory-structure.md) |

## 🔧 Generic rules

| Name          | Purpose                                              | When to use                                                                     | Link                                                                 |
| ------------- | ---------------------------------------------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Communication | Communication guidelines and best practices          | When setting team communication norms in CLAUDE.md                              | [./generic-rules/communication.md](./generic-rules/communication.md) |
| Development   | Development workflow and coding practices            | When adding coding standards to a project CLAUDE.md                             | [./generic-rules/development.md](./generic-rules/development.md)     |
| Documentation | Project documentation standards and structure        | When creating or updating documentation                                         | [./generic-rules/documentation.md](./generic-rules/documentation.md) |
| Git           | Git workflow and commit standards                    | When using version control                                                      | [./generic-rules/git.md](./generic-rules/git.md)                     |
| Preferences   | Tool preferences and configuration                   | When setting up development environment                                         | [./generic-rules/preferences.md](./generic-rules/preferences.md)     |
| Performance   | Performance considerations and optimization guidance | When designing or optimizing code for efficiency                                | [./generic-rules/performance.md](./generic-rules/performance.md)     |
| Security      | Security guidelines and best practices               | When setting security policies for a Claude project or reviewing existing rules | [./generic-rules/security.md](./generic-rules/security.md)           |
| Validation    | Data validation and error handling                   | When implementing validation logic                                              | [./generic-rules/validation.md](./generic-rules/validation.md)       |
| Workflows     | Workflow patterns and automation                     | When adding planning, problem-solving, or verification behavior to CLAUDE.md    | [./generic-rules/workflows.md](./generic-rules/workflows.md)         |
