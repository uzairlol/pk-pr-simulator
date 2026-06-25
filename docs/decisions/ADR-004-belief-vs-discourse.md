# ADR-004: Belief vs. Visible Discourse — Separate Latent States

**Status:** Accepted  
**Date:** 2026-06-25  
**Deciders:** Project team  
**Related:** [Requirements FR-6.4, FR-8](../03-requirements.md) · [ADR-001](ADR-001-three-layer-architecture.md)

## Context

Platform data (tweets, comments, posts) measures **visible discourse** — who chose to post, in what language, on which platform. It does not equal **latent opinion** across the population. In Pakistan, representation gaps are acute: urban English Twitter users are not rural Urdu-speaking mobile users; telecom churn anger may be expressed offline or in WhatsApp groups invisible to APIs.

A common failure mode is training a sentiment model on posts and treating its output as "public opinion," which reviewers will reject as ecologically invalid.

## Decision

The simulator maintains **two distinct cohort-level state variables**:

| State | Meaning | Updated by |
|-------|---------|------------|
| **Latent belief** \(b_{c,t}\) | Estimated true opinion/sentiment of cohort \(c\) at time \(t\) | MRP priors, Bayesian fusion, bounded-confidence peer influence |
| **Visible discourse intensity** \(v_{c,t}\) | Observed posting volume and valence of public text | NLP perception layer on ingested documents; linked via a **posting propensity** function \(v \sim f(b, \text{severity}, \text{media exposure})\) |

**Rules:**

1. Fusion layer updates **belief** posteriors; perception layer informs **discourse** observations used as likelihood evidence, not as direct belief replacement.
2. Forecast outputs default to **belief trajectories with uncertainty**; discourse trajectories are secondary diagnostic outputs.
3. No code path equates "sentiment of posts" to "sentiment of cohort" without passing through fusion calibration.
4. Dashboard and API must label outputs: *"Model-estimated cohort belief (calibrated)"* vs. *"Observed platform discourse (biased sample)"*.

Posting propensity is explicit and logged (e.g., logistic link with cohort platform penetration weights from PTA).

## Alternatives considered

| Option | Pros | Cons |
|--------|------|------|
| **A. Separate belief and discourse (chosen)** | Honest about representativeness; fusion layer has clear job; strong thesis framing | More state to track; requires calibration data |
| **B. Discourse-only (sentiment = opinion)** | Simple | Violates representativeness requirement; fails reviewer scrutiny |
| **C. Belief-only (ignore posts)** | Clean priors | Wastes platform data; no event responsiveness |
| **D. LLM "what would people think" queries** | Easy narrative | Unvalidated; conflates belief and discourse; not reproducible |

## Consequences

**Positive:**

- Direct answer to "social media isn't representative" criticism.
- Ablation can show value of fusion vs. text-only baseline (charter SC-1).
- Aligns with MRP + Bayesian survey calibration literature.

**Negative:**

- Posting propensity model must be documented and sensitivity-tested.
- Users may confuse two output series without clear UI labeling.

**Follow-ups:**

- Implement in `src/fusion/bayesian_fusion.py` and `src/propagation/opinion_dynamics.py` (Phases 5–7).
- Add glossary entries to `docs/architecture.md`.
- Phase 10 explainability must attribute belief shifts separately from discourse spikes.
