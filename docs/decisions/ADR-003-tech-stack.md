# ADR-003: Technology Stack — Python, PyTorch, Poetry, Postgres, W&B

**Status:** Accepted  
**Date:** 2026-06-25  
**Deciders:** Project team  
**Related:** [Requirements NFR-5, NFR-6](../03-requirements.md) · `pyproject.toml`

## Context

The system spans NLP fine-tuning, Bayesian inference, graph algorithms, agent-based simulation, dashboards, and experiment tracking. The stack must:

- Run on a **single GPU workstation** (NFR-5.1).
- Support reproducible installs for collaborators and thesis examiners.
- Use mature libraries for each layer without unnecessary microservices.

The development machine has **Python 3.10 and 3.14** available; PyTorch does not yet reliably support 3.14, so the project pins **Python 3.10–3.12**.

## Decision

| Concern | Choice |
|---------|--------|
| Language | Python 3.10+ (recommended 3.10 or 3.12) |
| Packaging | **Poetry** (`pyproject.toml` + `poetry.lock`) |
| Deep learning | PyTorch, Hugging Face `transformers`, `datasets`, `accelerate` |
| Graphs | NetworkX (prototype), `python-igraph` (scale-up) |
| Agent simulation | Mesa |
| Tabular / analytics | pandas, PyArrow, DuckDB |
| Metadata DB | PostgreSQL 16 via Docker Compose |
| ORM / DB driver | SQLAlchemy + psycopg2-binary |
| Bayesian / MRP | PyMC, ArviZ, NumPyro |
| ML utilities | scikit-learn, SHAP |
| Visualization / UI | Plotly, Dash, Streamlit |
| API (dashboard backend) | FastAPI + Uvicorn |
| Experiment tracking | Weights & Biases |
| Dev quality | pytest, pytest-cov, black, ruff, mypy |

**Local development:**

```bash
poetry env use 3.10          # or 3.12
poetry install
docker compose up -d db      # Postgres on localhost:5432
```

Secrets (API keys, `DATABASE_URL`) live in `.env`, gitignored.

## Alternatives considered

| Option | Pros | Cons |
|--------|------|------|
| **A. Poetry + PyTorch ecosystem (chosen)** | Standard ML research stack; lockfile reproducibility | Poetry learning curve; Windows path quirks |
| **B. Conda/mamba only** | Easy CUDA binaries | Heavier env; weaker lockfile for non-Python deps |
| **C. Plain requirements.txt** | Simple | No dev/prod groups; drift between machines |
| **D. JAX-only (no PyTorch)** | Fast NumPyro integration | Weaker HF transformers ergonomics for fine-tuning |
| **E. Cloud-only (no local GPU)** | No hardware cost | Violates NFR-5.1; reproducibility harder for defense demo |

## Consequences

**Positive:**

- `poetry install` on fresh clone satisfies Phase 2 exit criteria.
- Postgres manifest for ingestion lineage is production-pattern without over-engineering.
- W&B satisfies NFR-7.1 out of the box.

**Negative:**

- Windows developers must install Docker Desktop for Postgres.
- CUDA PyTorch wheel selection may require manual `poetry source` or env vars on some GPUs.
- PyMC sampling can be slow on CPU — acceptable for cohort-level MRP, not massive hierarchies.

**Follow-ups:**

- Phase 12: GitHub Actions CI with CPU-only PyTorch for unit tests.
- Document `DATABASE_URL` in `.env.example`.
- Pin `torch` in lockfile after first successful install on target GPU machine.
