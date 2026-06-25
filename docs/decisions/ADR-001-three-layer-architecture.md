# ADR-001: Three-Layer Architecture with Fusion vs. End-to-End LLM Agent Simulator

**Status:** Accepted  
**Date:** 2026-06-25  
**Deciders:** Project team  
**Related:** [Architecture](../architecture.md) · [Requirements FR-4–FR-7](../03-requirements.md)

## Context

The project must forecast cohort-level public reactions to corporate PR scenarios in Pakistan. Two broad architectural families exist:

1. **Modular pipeline:** perception (NLP) → population (MRP cohort priors) → propagation (opinion dynamics) → fusion (Bayesian calibration) → simulation orchestration.
2. **End-to-end LLM agent simulator:** large language models emulate individual or group agents interacting on social media in a single generative loop.

The charter requires auditable, reproducible, cohort-level outputs with uncertainty bands (NFR-4.1, FR-9). Reviewers and ethics committees will ask how forecasts are validated and whether the system enables individual targeting (NG-1, NG-2).

## Decision

Adopt a **three-layer architecture plus fusion layer**:

| Layer | Responsibility |
|-------|----------------|
| **Perception** | Multilingual classification (sentiment, stance, emotion, event type); entity linking |
| **Population** | PBS/PSLM post-stratification; MRP cohort opinion priors |
| **Propagation** | Multiplex network; bounded-confidence dynamics; IC/LT baselines |
| **Fusion** | Bayesian combination of priors, platform evidence, scenario features |

Mesa wraps layers into a **daily time-stepped simulation engine**. A **dashboard** consumes forecasts and audit records.

Defer **GNN-based propagation** (Kipf & Welling-style) to post-MVP ablation only.

## Alternatives considered

| Option | Pros | Cons |
|--------|------|------|
| **A. Modular three-layer + fusion (chosen)** | Each layer unit-testable; ablations natural; equations inspectable; aligns with EMBERS/GDELT-style forecasting tradition | Integration complexity; more code than a single notebook |
| **B. End-to-end LLM multi-agent simulator** | Rich emergent behavior; fast to prototype narratives | High API cost; hard to validate; opaque dynamics; difficult reproducibility; ethical scrutiny on agent personas mimicking real groups |
| **C. Text-only sentiment dashboard (no simulation)** | Simple | Fails charter SC-1/SC-4; no scenario conditioning or diffusion; cannot answer "what if" PR questions |
| **D. Single monolithic fine-tuned LLM forecaster** | One model to maintain | No demographic calibration; conflates belief and discourse; poor uncertainty quantification |

## Consequences

**Positive:**

- Methods chapter maps cleanly to layers and ADRs.
- Phase 9 ablations (full vs. text-only vs. diffusion-only) are first-class.
- Bounded-confidence update rule is citable and defensible vs. black-box LLM behavior.

**Negative:**

- Higher implementation surface area across `src/` modules.
- Interface contracts between layers must be versioned in configs.

**Follow-ups:**

- Document layer I/O schemas in Phase 3 (`ingestion/schema.py`) and Phase 7 (`scenario/encoder.py`).
- Draw architecture diagram in `docs/architecture.md` (Phase 2.4).
