# Pakistan-focused **cohort-level** population opinion simulator for company PR scenario forecasting in the telecommunications sector.

> This system is an **aggregate decision-support tool** — not a person-level prediction or targeting engine.

## Documentation

| Document | Description |
|----------|-------------|
| [Zero to Published Paper Pipeline](docs/Zero_to_Published_Paper_Pipeline.md) | Full 17-phase execution plan |
| [Phase 1 Completion Record](docs/PHASE1_COMPLETION.md) | Literature, charter, ethics, legal |
| [Phase 2 Completion Record](docs/PHASE2_COMPLETION.md) | Requirements, ADRs, stack, architecture |
| [Architecture](docs/architecture.md) | Mermaid diagrams and layer definitions |
| [Requirements](docs/03-requirements.md) | Functional and non-functional requirements |
| [ADRs](docs/decisions/README.md) | Architecture decision records |
| [Project Charter](docs/01-project-charter.md) | Scope lock, non-goals, MVP success criteria |
| [Data Legal Notes](docs/02-data-legal-notes.md) | ToS/legal review per data source |
| [Ethics Application Draft](docs/03-ethics-application-draft.md) | IRB submission template |
| [API Access Checklist](docs/04-api-access-checklist.md) | YouTube, Reddit, Meta, survey requests |
| [Literature Index](docs/literature/README.md) | Literature matrix + Zotero tagging guide |

## Current Status

**Phase 2** complete: requirements locked, 4 ADRs written, Poetry stack installed, architecture diagram committed.

**Phase 1** manual items still required before live data collection: supervisor sign-off, ethics/IRB approval, API applications.

## Quick Start

```powershell
# Python 3.10–3.12 required (PyTorch does not support 3.14)
py -3.10 -m pip install poetry
py -3.10 -m poetry config virtualenvs.in-project true
py -3.10 -m poetry install
copy .env.example .env

docker compose up -d db    # Postgres on localhost:5432
py -3.10 -m poetry run pytest tests/ -q
```

## Repository Structure

```
src/
  ingestion/      # Data connectors and schemas
  nlp/            # Multilingual perception layer
  population/     # MRP and cohort framing
  propagation/    # Opinion dynamics and diffusion
  fusion/         # Bayesian calibration
  scenario/       # Scenario encoding
  simulation/     # Time-stepped engine
  evaluation/     # Backtesting
  explainability/ # SHAP and audit explanations
  dashboard/      # Streamlit/Dash demo
  utils/          # Shared utilities
data/
  external/       # PBS, PTA, SBP (gitignored content)
  processed/      # Processed datasets
docs/             # Charter, legal, ethics, pipeline, ADRs
```

## License

MIT — see [LICENSE](LICENSE).
