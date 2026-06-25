# System Requirements

**Document version:** 1.0  
**Date:** 2026-06-25  
**Status:** Approved for MVP implementation (Phase 2 lock)  
**Derived from:** [Project Charter](01-project-charter.md) · [Architecture](architecture.md)

---

## 1. Purpose

This document specifies functional and non-functional requirements for the Pakistan-focused cohort-level PR scenario simulator MVP. All requirements trace to charter scope (telecom sector, English-first, aggregate outputs) and non-goals NG-1 through NG-8.

---

## 2. Stakeholders and Users

| Stakeholder | Need |
|-------------|------|
| Student researcher | Reproducible pipeline for thesis evaluation |
| Supervisor / committee | Auditable methodology and scope discipline |
| Communications analyst (conceptual user) | Cohort-level scenario forecasts with uncertainty |
| Annotators | Clear labeling guidelines and consent |

---

## 3. Functional Requirements

### FR-1: Company dossier ingestion

| ID | Requirement | Priority | Acceptance criterion |
|----|-------------|----------|-------------------|
| FR-1.1 | System SHALL ingest structured company dossiers for 2–3 pilot telecom operators | Must | Validated Pydantic schema; 2–3 dossiers load without error |
| FR-1.2 | Dossier SHALL include brands, executives, controversies, messaging, pricing history, regional footprint, linked issues | Must | Schema fields documented in `src/ingestion/schema.py` (Phase 3) |
| FR-1.3 | Dossier data SHALL be sourced only from public materials | Must | Source URLs recorded per field where applicable |

### FR-2: Pakistan news and platform signal ingestion

| ID | Requirement | Priority | Acceptance criterion |
|----|-------------|----------|-------------------|
| FR-2.1 | System SHALL provide a common `Connector` interface for all data sources | Must | `fetch(query, since, until) -> list[RawDocument]` |
| FR-2.2 | MVP SHALL include news connector (Dawn + 2 outlets via RSS/official feeds) | Must | ≥1 successful fetch logged to Postgres manifest |
| FR-2.3 | MVP SHALL include GDELT connector for event context | Must | Pakistan-filtered events retrievable |
| FR-2.4 | MVP SHALL include at least one social connector (YouTube or Reddit) post-ethics | Must | API-compliant fetch with lineage metadata |
| FR-2.5 | System SHALL load PBS/PSLM and PTA aggregate tables | Must | Files in `data/external/` with `SOURCES.md` manifest |
| FR-2.6 | Each document SHALL carry `source_id`, `lineage`, `retention_expiry` | Must | Fields present on all ingested records |
| FR-2.7 | System SHALL deduplicate syndicated near-duplicate news | Must | MinHash/SimHash dedup unit-tested |

### FR-3: Multilingual text processing (perception layer)

| ID | Requirement | Priority | Acceptance criterion |
|----|-------------|----------|-------------------|
| FR-3.1 | System SHALL normalize English text for downstream NLP | Must | Normalizer runs on ingested corpus |
| FR-3.2 | System SHALL tag language/script (EN / Urdu-script / Roman-Urdu / code-mixed) | Should | Lang-id on ≥95% of documents |
| FR-3.3 | MVP SHALL classify sentiment, stance, emotion, event-type on English documents | Must | Fine-tuned checkpoints; macro-F1 per charter SC-3 |
| FR-3.4 | System SHALL provide Urdu/Roman Urdu normalization extension | Should | `text_normalize.py` unit-tested on 200-string sample |
| FR-3.5 | System SHALL link entities to dossier alias tables | Must | Rules-based linker with fuzzy matching |
| FR-3.6 | Evaluation SHALL report metrics stratified by script | Should | Per-script table in evaluation outputs |

### FR-4: Cohort modeling (population layer)

| ID | Requirement | Priority | Acceptance criterion |
|----|-------------|----------|-------------------|
| FR-4.1 | System SHALL build post-stratification frame: province × urban/rural × age band | Must | `frame_builder.py` outputs population weights |
| FR-4.2 | System SHALL operationalize charter cohorts (urban digital, rural, price-sensitive, journalists, etc.) | Must | Cohort definitions documented in datasheet |
| FR-4.3 | System SHALL implement MRP for cohort opinion priors with partial pooling | Must | PyMC/NumPyro model runs end-to-end |
| FR-4.4 | System SHALL calibrate against ≥1 survey prior or published topline | Should | Posterior predictive checks documented |
| FR-4.5 | System SHALL NOT infer sensitive traits (religion, ethnicity) | Must | Code review + charter NG-4 compliance |

### FR-5: Propagation and diffusion

| ID | Requirement | Priority | Acceptance criterion |
|----|-------------|----------|-------------------|
| FR-5.1 | System SHALL build multiplex network (outlets, cohorts, issues) | Must | NetworkX graph from ingested data |
| FR-5.2 | System SHALL implement bounded-confidence opinion dynamics | Must | Explicit equation with logged parameters |
| FR-5.3 | System SHALL implement Independent Cascade and Linear Threshold baselines | Must | Baselines runnable for ablation |
| FR-5.4 | Primary simulation nodes SHALL be cohort-level, not individuals | Must | No individual-level forecast output path |

### FR-6: Fusion and scenario conditioning

| ID | Requirement | Priority | Acceptance criterion |
|----|-------------|----------|-------------------|
| FR-6.1 | System SHALL fuse survey priors, platform evidence, and scenario features via Bayesian fusion | Must | Posterior with credible intervals |
| FR-6.2 | System SHALL encode hypothetical scenarios (price hike, boycott, apology, etc.) | Must | `scenario/encoder.py` schema documented |
| FR-6.3 | Fusion SHALL prevent viral-but-unrepresentative spikes from dominating priors | Must | Documented weighting; ablation in Phase 9 |
| FR-6.4 | System SHALL separate latent cohort belief from visible posting probability | Must | Per ADR-004; two state variables in model |

### FR-7: Simulation orchestration

| ID | Requirement | Priority | Acceptance criterion |
|----|-------------|----------|-------------------|
| FR-7.1 | System SHALL run daily time-stepped simulations via Mesa-based engine | Must | Config-driven `simulation/run` |
| FR-7.2 | Runs SHALL be specified by YAML config (company, scenario, dates, seed, checkpoints) | Must | `configs/run_*.yaml` |
| FR-7.3 | One command SHALL reproduce full pipeline for a pilot config | Must | Charter SC-5 |

### FR-8: Uncertainty-banded outputs

| ID | Requirement | Priority | Acceptance criterion |
|----|-------------|----------|-------------------|
| FR-8.1 | Forecasts SHALL include uncertainty bands (e.g., 80% intervals) | Must | Intervals on all cohort trajectories |
| FR-8.2 | Outputs SHALL be cohort-aggregated only | Must | No per-user scores in API or dashboard |
| FR-8.3 | System SHALL present multiple cohorts; no single "national score" without breakdown | Must | Charter NG-3 |

### FR-9: Audit trail and explainability

| ID | Requirement | Priority | Acceptance criterion |
|----|-------------|----------|-------------------|
| FR-9.1 | Every run SHALL log seed, config, source doc IDs, checkpoint hashes, outputs | Must | `utils/audit.py` record per run |
| FR-9.2 | Runs SHALL log to Weights & Biases | Should | W&B project configured |
| FR-9.3 | NLP components SHALL support SHAP attributions (Phase 10) | Should | SHAP layer for classifiers |
| FR-9.4 | Global explanation SHALL identify top drivers (cohorts, events, sources) | Should | Query over audit records |

### FR-10: Evaluation and backtesting

| ID | Requirement | Priority | Acceptance criterion |
|----|-------------|----------|-------------------|
| FR-10.1 | System SHALL evaluate on 15–30 historical telecom PR events | Must | Benchmark datasheet |
| FR-10.2 | Evaluation SHALL use time-based and company holdout splits | Must | No random shuffle of events |
| FR-10.3 | Metrics SHALL include CRPS, Brier, calibration plots | Must | Charter SC-1, SC-2 |
| FR-10.4 | Ablations SHALL compare full system vs. text-only and diffusion baselines | Must | Results table in Phase 9 |

### FR-11: Dashboard (Phase 11)

| ID | Requirement | Priority | Acceptance criterion |
|----|-------------|----------|-------------------|
| FR-11.1 | Dashboard SHALL allow scenario selection and forecast visualization | Could (Phase 11) | Streamlit/Dash demo |
| FR-11.2 | Dashboard SHALL display audit trail for selected run | Could (Phase 11) | Audit viewer panel |

---

## 4. Non-Functional Requirements

### NFR-1: Traceability and reproducibility

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1.1 | Every forecast reproducible from logged seed + config + data manifest | 100% of published results |
| NFR-1.2 | Config files version-controlled; checkpoint hashes in audit log | Mandatory |
| NFR-1.3 | Docker Compose brings up Postgres + app for demo | Phase 11 |

### NFR-2: Data minimization and deletion

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-2.1 | Personal identifiers stripped or hashed after dedup | Default on social connectors |
| NFR-2.2 | `retention_expiry` enforced by deletion job | No expired raw docs retained |
| NFR-2.3 | No raw social JSON in public GitHub release | Release assets exclude PII |

### NFR-3: Security and compliance

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-3.1 | API keys and secrets in `.env` only | Never committed |
| NFR-3.2 | Data collection gated on ethics approval | Enforced before Phase 3 live pulls |
| NFR-3.3 | Connector behavior complies with documented legal notes | Per `02-data-legal-notes.md` |

### NFR-4: Explainability and governance

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-4.1 | Propagation uses inspectable equations, not black-box LLM agents | ADR-001 |
| NFR-4.2 | Safeguards doc cross-references enforcing code paths | Phase 10 |
| NFR-4.3 | Forecasts labeled advisory/contestable in UI and docs | All user-facing outputs |

### NFR-5: Performance and compute

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-5.1 | Full MVP pipeline runs on a single GPU workstation (≥8 GB VRAM) | 1× consumer GPU |
| NFR-5.2 | NLP inference batchable; training fits 1 GPU with gradient accumulation | No multi-node requirement |
| NFR-5.3 | NetworkX for prototyping; igraph if graph exceeds ~100k nodes | Documented switch point |
| NFR-5.4 | Postgres for metadata; DuckDB/Parquet for analytics workloads | Hybrid storage |

### NFR-6: Maintainability and quality

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-6.1 | `pytest` for ingestion, normalization, fusion logic | CI green on PR |
| NFR-6.2 | `ruff` + `black` + `mypy` on `src/` | GitHub Actions Phase 12 |
| NFR-6.3 | ADRs for major design decisions | `docs/decisions/` |

### NFR-7: Observability

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-7.1 | Experiment metrics logged to W&B | All training runs |
| NFR-7.2 | Structured logging in ingestion and simulation | JSON or key-value logs |

---

## 5. Requirements Traceability Matrix

| Charter success criterion | Requirements |
|---------------------------|--------------|
| SC-1 CRPS vs. baseline | FR-6, FR-7, FR-10 |
| SC-2 Calibration | FR-8, FR-10 |
| SC-3 NLP F1 | FR-3 |
| SC-4 Company holdout | FR-10 |
| SC-5 Reproducibility | FR-7, FR-9, NFR-1 |
| SC-6 Annotator κ | FR-3 (annotation process, Phase 4) |
| NG-1 No individual profiling | FR-5.4, FR-8.2, NFR-2 |
| NG-3 No monolith | FR-8.3 |
| NG-5 ToS compliance | FR-2, NFR-3 |

---

## 6. Out of Scope (MVP)

- Meta Content Library (unless approved) — FR-2.4 fallback only
- Broadcast ASR — charter NG-7
- GNN propagation — post-MVP stretch (ADR-001)
- Real-time surveillance — charter NG-6
- Individual-level SHAP explanations — ADR-004

---

## 7. Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-06-25 | Initial requirements lock for Phase 2 |
