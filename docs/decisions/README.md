# Architecture Decision Records (ADRs)

This folder records significant design decisions for the pk-pr-simulator project. Each ADR follows the template: **Context → Decision → Alternatives → Consequences**.

ADRs are written at decision time and reorganized into the thesis Methods chapter during Phase 13.

| ADR | Title | Status |
|-----|-------|--------|
| [ADR-001](ADR-001-three-layer-architecture.md) | Three-layer architecture + fusion vs. end-to-end LLM simulator | Accepted |
| [ADR-002](ADR-002-mvp-language-scope.md) | English-first MVP; Urdu/Roman Urdu as extension | Accepted |
| [ADR-003](ADR-003-tech-stack.md) | Python/PyTorch stack, Poetry, Postgres, W&B | Accepted |
| [ADR-004](ADR-004-belief-vs-discourse.md) | Latent cohort belief ≠ visible posting probability | Accepted |

## Template for new ADRs

```markdown
# ADR-NNN: Title

**Status:** Proposed | Accepted | Superseded  
**Date:** YYYY-MM-DD  
**Deciders:** [names]

## Context
[What problem or constraint forces a decision?]

## Decision
[What we chose.]

## Alternatives considered
| Option | Pros | Cons |
|--------|------|------|

## Consequences
**Positive:** ...  
**Negative:** ...  
**Follow-ups:** ...
```
