# pk-pr-simulator

Pakistan-focused **cohort-level** population opinion simulator for company PR scenario forecasting in the telecommunications sector.

> This system is an **aggregate decision-support tool** — not a person-level prediction or targeting engine.

## Documentation

| Document | Description |
|----------|-------------|
| [Zero to Published Paper Pipeline](docs/Zero_to_Published_Paper_Pipeline.md) | Full 17-phase execution plan |
| [Phase 1 Completion Record](docs/PHASE1_COMPLETION.md) | Phase 1 status and exit criteria |
| [Project Charter](docs/01-project-charter.md) | Scope lock, non-goals, MVP success criteria |
| [Data Legal Notes](docs/02-data-legal-notes.md) | ToS/legal review per data source |
| [Ethics Application Draft](docs/03-ethics-application-draft.md) | IRB submission template |
| [API Access Checklist](docs/04-api-access-checklist.md) | YouTube, Reddit, Meta, survey requests |
| [Literature Index](docs/literature/README.md) | Literature matrix + Zotero tagging guide |
| [Literature Matrix (xlsx)](docs/datasheets/Pakistan_PR_Simulation_Literature_Matrix.xlsx) | 105 indexed sources |

## Current Status

**Phase 1** documentation is complete in-repo. Remaining Phase 1 actions require you:

1. Supervisor sign-off on the [project charter](docs/01-project-charter.md)
2. University ethics/IRB submission using the [ethics draft](docs/03-ethics-application-draft.md)
3. File API access applications per the [checklist](docs/04-api-access-checklist.md)

Do **not** begin real platform data collection until ethics approval is granted.

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
