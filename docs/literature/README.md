# Phase 1 — Literature Review Index

**Status:** Complete (93 primary sources + 12 supplementary core references)  
**Matrix file:** [Pakistan_PR_Simulation_Literature_Matrix.xlsx](datasheets/Pakistan_PR_Simulation_Literature_Matrix.xlsx)  
**Pipeline reference:** [Zero to Published Paper Pipeline](Zero_to_Published_Paper_Pipeline.md) § Phase 1.1

---

## Matrix Structure

The spreadsheet contains three sheets:

| Sheet | Purpose |
|-------|---------|
| **Literature Matrix** | One row per source: citation, contribution, layers informed, Pakistan gap |
| **Layer Guide** | Definitions for Text-perception, Cohort-and-network, Pakistan calibration, Uncertainty/audit |
| **Coverage Summary** | Counts by source family and layer coverage |

### Column definitions (Literature Matrix)

1. **citation** — Author/year/title; source file traceability where extracted from PDF package  
2. **what it contributes** — Methodological or empirical contribution to this project  
3. **which of your layers it informs** — One or more of the four project layers  
4. **gap it leaves for Pakistan** — Explicit gap this project addresses

---

## Zotero Workflow

Import or verify all matrix sources in Zotero with these tags (match layer names):

| Zotero tag | Layer |
|------------|-------|
| `layer:perception` | Text-perception (NLP, events, sentiment) |
| `layer:cohort-network` | Opinion dynamics, diffusion, GNN, influence |
| `layer:calibration` | MRP, Bayesian fusion, survey weighting |
| `layer:audit` | SHAP, scoring rules, forecast evaluation |
| `layer:governance` | NIST AI RMF, GDPR, PECA, EU AI Act |
| `geo:pakistan` | Pakistan-specific or South Asia context |

**Recommended collections:**

- `PK-PR / Forecasting Systems`
- `PK-PR / Multilingual NLP`
- `PK-PR / Diffusion & Networks`
- `PK-PR / Calibration & MRP`
- `PK-PR / Explainability & Evaluation`
- `PK-PR / Governance`

Export the library periodically to `docs/datasheets/literature_zotero_export.bib` for version control (optional).

---

## Core Pipeline References (Section 1.1)

The following foundational works are required by the pipeline. They are either in the main matrix or listed as **supplementary rows** (IDs SUP-001–SUP-012) appended to the matrix:

| Topic | Reference | In matrix |
|-------|-----------|-----------|
| Forecasting | EMBERS, GDELT, Media Cloud, Hoaxy | EMBERS, Hoaxy, GDELT (SUP); Media Cloud (SUP) |
| NLP | BERT, GoEmotions, SemEval, MAVEN | SemEval, MAVEN; BERT, GoEmotions (SUP) |
| Urdu NLP | AbjadNLP 2026 + citations | AbjadNLP rows |
| Diffusion | Bounded confidence, IC, LT, Kleinberg | IC, bounded confidence; Kleinberg (SUP) |
| Calibration | Gelman MRP | MRP folder rows |
| GNN | Kipf & Welling GCN | SUP |
| Explainability | Lundberg & Lee SHAP | SHAP folder + SUP |
| Forecast eval | Gneiting & Raftery | Scoring-rules folder + SUP |
| Governance | NIST AI RMF, EU AI Act, GDPR, PECA, PDP Bill | SUP governance rows |

**Total count:** 93 data rows + 12 supplementary = **105 indexed sources** (exceeds 40+ exit criterion).

---

## Source Families in Matrix (from Coverage Summary)

Includes: AbjadNLP, SemEval, MAVEN, bounded confidence / opinion dynamics, EMBERS, Hoaxy, GNN, influence maximization, MRP, probabilistic forecast scoring, SHAP explainability, and related folders from the uploaded literature package.

---

## How This Feeds the Thesis/Paper

- **Related Work (Thesis Ch. 2 / Paper §2):** Organize by layer using the matrix; end with explicit Pakistan gap paragraph.  
- **Methods justification:** Cite diffusion and calibration papers when writing ADRs.  
- **Limitations:** Reuse "gap" column language for honest scope boundaries.

---

## Maintenance

- Add a row when you read a new paper that changes design decisions.  
- Re-export or commit xlsx when the matrix changes materially.  
- Link new ADRs in `docs/decisions/` to supporting citations from this matrix.
