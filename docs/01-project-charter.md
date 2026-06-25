# Project Charter: Pakistan-Focused Population Opinion Simulator

**Document version:** 1.0  
**Date:** 2026-06-25  
**Status:** Pending supervisor sign-off  
**Repository:** [pk-pr-simulator](https://github.com/uzairlol/pk-pr-simulator)

---

## 1. Problem Statement

Pakistani companies operating in high-visibility sectors face reputational and commercial risk from public-reaction dynamics that are fast-moving, multilingual, platform-skewed, and poorly represented by generic sentiment dashboards. This project builds an **aggregate decision-support system for cohort-level PR scenario forecasting** — not a person-level prediction engine. The system ingests public company profiles, Pakistan-relevant news and platform discourse, and official demographic/statistical anchors; processes text through a multilingual perception layer; calibrates cohort-level opinion estimates against population structure and survey priors; models propagation through explicit opinion-dynamics mechanisms; and outputs uncertainty-banded scenario forecasts with a full audit trail. The intended user is a communications strategist or risk analyst who needs defensible, contestable forecasts at the level of **population segments** (e.g., urban digital consumers in Punjab, price-sensitive households, journalist communities), not individual targeting or covert persuasion optimization.

---

## 2. Ethical and Methodological Anchor

> **This system is an aggregate decision-support tool. It does not predict, profile, or optimize influence at the individual level.**

All design, data handling, evaluation, and publication framing must preserve this distinction. Cohort outputs are advisory estimates with explicit uncertainty; they must never be presented as deterministic predictions of "what Pakistan thinks."

---

## 3. Non-Goals (Explicit Scope Exclusions)

The following are **out of scope** for this project and must not be added without a new charter revision and renewed ethics review:

| # | Non-goal | Rationale |
|---|----------|-----------|
| NG-1 | **Individual profiling or micro-targeting** | No building of person-level influence scores, psychographic profiles, or contact-level outreach lists from platform data. |
| NG-2 | **Covert persuasion optimization** | No features that recommend how to manipulate specific individuals or hidden audience segments for commercial or political gain. |
| NG-3 | **Monolithic "Pakistani public" claims** | No single scalar "national opinion" presented without cohort breakdown, calibration context, and uncertainty bands. |
| NG-4 | **Sensitive-trait inference** | No algorithmic inference of religion, ethnicity, political affiliation, or other sensitive attributes from text or behavior. Language/script may be used only as a coarse discourse proxy, with limitations stated. |
| NG-5 | **Covert or ToS-violating data collection** | No scraping where platform terms forbid it; no circumventing API access controls or research-gating requirements. |
| NG-6 | **Real-time operational surveillance** | MVP is retrospective and scenario-based (historical backtest + hypothetical scenarios), not a live monitoring or alerting product for ongoing surveillance of individuals. |
| NG-7 | **Broadcast ASR / full multimodal ingestion** | Television and radio transcript integration is deferred post-MVP due to ASR cost, licensing, and validation complexity. |
| NG-8 | **Claims of causal certainty** | The simulator models plausible diffusion and calibration dynamics; it does not claim proven causal identification of opinion change. |

---

## 4. MVP Scope Lock

### 4.1 Sector

**Telecommunications** — selected for MVP because PTA publishes rich annual penetration, broadband, and social-media usage statistics that support defensible calibration; the sector has a history of price, service-quality, and regulatory controversies suitable for backtesting; and pilot companies (e.g., Jazz, Telenor Pakistan, Zong, Ufone) have substantial public discourse footprints.

### 4.2 Language

**English-first** for MVP ingestion, annotation, and model training. Urdu-script and Roman Urdu normalization and classification are built as an extension track (normalizer + per-script evaluation breakdown) but are not required for MVP backtest pass/fail.

### 4.3 Platform and data connectors (MVP)

| Priority | Connector | Role |
|----------|-----------|------|
| P0 | PBS / PSLM demographic frame | Population post-stratification anchor |
| P0 | PTA annual report tables | Platform penetration calibration |
| P0 | Pakistani news (Dawn + 2 additional outlets via RSS/official feeds) | Primary discourse signal, lowest legal risk |
| P1 | GDELT | Global/event context layer |
| P1 | YouTube Data API (`commentThreads`) | Platform discourse (subject to API approval and quota) |
| P2 | Reddit (PRAW, compliant with Developer Terms) | Supplementary discourse |
| Deferred | Meta Content Library | Only if formal research access is approved; not an MVP dependency |

**MVP connector count:** minimum **3 live connectors** (news + GDELT + one social platform), as specified in Phase 3 exit criteria.

### 4.4 Simulation granularity

- **Daily time steps** for scenario trajectories.
- **Cohort-level** nodes in propagation layer (not individual user agents as primary output).
- **2–3 pilot company dossiers** manually constructed from public sources.

### 4.5 Architecture (high level)

Three functional layers plus fusion, per pipeline ADR-001 (to be formalized in Phase 2):

1. **Perception** — multilingual NLP (sentiment, stance, emotion, event type).
2. **Population** — MRP-calibrated cohort opinion priors from PBS/PSLM frame + survey benchmarks.
3. **Propagation** — bounded-confidence opinion dynamics with Independent Cascade and Linear Threshold baselines.
4. **Fusion** — Bayesian combination of survey priors, platform evidence, and scenario features with uncertainty bands.

---

## 5. Success Criteria (Numeric, MVP)

All criteria are evaluated on a held-out **historical event benchmark** of 15–30 Pakistan-relevant telecom PR events (curated in Phase 9). Splits: time-based holdout and company holdout.

| ID | Criterion | Target | Measurement |
|----|-----------|--------|-------------|
| SC-1 | **Forecast skill vs. text-only baseline** | Full system beats text-only sentiment trajectory baseline by **≥ 15% relative CRPS reduction** on the time-based test split | CRPS on cohort-aggregated sentiment/discourse trajectories |
| SC-2 | **Calibration** | 80% prediction intervals contain observed trajectory values **≥ 75%** of the time (reliability within ±5 pp of nominal) | Reliability diagram on held-out events |
| SC-3 | **NLP perception layer** | Macro-F1 **≥ 0.70** on English held-out test set for sentiment; stance macro-F1 **≥ 0.65** | Stratified held-out evaluation |
| SC-4 | **Generalization** | Full system beats text-only baseline on **company holdout split** (companies not seen during training dossier/NLP fine-tuning) | Same CRPS comparison, company-holdout partition |
| SC-5 | **Reproducibility** | One-command simulation rerun reproduces forecast within floating-point tolerance given fixed seed + config | Audit record hash match (Phase 8) |
| SC-6 | **Annotation quality** | Inter-annotator agreement κ **≥ 0.60** on shared 150-document pilot before scaling annotation | Cohen's/Fleiss' κ on dual-coded sample |

**MVP is not complete** until SC-1, SC-2, SC-5, and SC-6 are met. SC-3 and SC-4 are strongly expected; falling short triggers documented limitation statements, not scope expansion into individual-level modeling.

---

## 6. Key Stakeholders and Roles

| Role | Responsibility |
|------|----------------|
| Student researcher(s) | Implementation, documentation, ethics compliance, weekly supervisor updates |
| Supervisor | Charter sign-off, scope gate, thesis/paper guidance |
| University ethics committee | Approval before any real platform data collection |
| Annotators (2–3, disclosed) | Pilot and scaled labeling under annotation guidelines |

---

## 7. Dependencies and External Approvals

Before Phase 3 data collection begins:

- [ ] This charter signed off by supervisor (email acknowledgment sufficient)
- [ ] University ethics / IRB approval received
- [ ] Data legal notes reviewed (`docs/02-data-legal-notes.md`)
- [ ] YouTube API project created and quota request submitted
- [ ] Meta Content Library application submitted (optional, non-blocking)

---

## 8. Supervisor Sign-Off

| Field | Value |
|-------|-------|
| Supervisor name | _[To be completed]_ |
| Institution | _[To be completed]_ |
| Sign-off date | _[To be completed]_ |
| Sign-off method | Email / signed PDF / committee form |
| Notes or scope adjustments | _[To be completed]_ |

**Supervisor:** please reply to the student with "I approve the project charter v1.0 dated 2026-06-25" or list required changes. No implementation of real-data connectors may begin until this row is completed.

---

## 9. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-25 | Project team | Initial charter for Phase 1 lock |
