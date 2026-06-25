# Phase 2 Completion Record

**Phase:** Requirements & Architecture Lock (Weeks 3–5)  
**Target exit criteria:** [Pipeline § Phase 2](Zero_to_Published_Paper_Pipeline.md#phase-2--requirements--architecture-lock-weeks-35-overlaps-phase-1)

---

## Deliverables

| # | Deliverable | Location | Status |
|---|-------------|----------|--------|
| 2.1 | Functional & non-functional requirements | [03-requirements.md](03-requirements.md) | **Done** |
| 2.2 | ADR-001 Three-layer architecture | [decisions/ADR-001-three-layer-architecture.md](decisions/ADR-001-three-layer-architecture.md) | **Done** |
| 2.2 | ADR-002 MVP language scope | [decisions/ADR-002-mvp-language-scope.md](decisions/ADR-002-mvp-language-scope.md) | **Done** |
| 2.2 | ADR-003 Tech stack | [decisions/ADR-003-tech-stack.md](decisions/ADR-003-tech-stack.md) | **Done** |
| 2.2 | ADR-004 Belief vs. discourse | [decisions/ADR-004-belief-vs-discourse.md](decisions/ADR-004-belief-vs-discourse.md) | **Done** |
| 2.3 | `pyproject.toml` + `poetry.lock` | Repository root | **Done** |
| 2.3 | Postgres via Docker Compose | [docker-compose.yml](../docker-compose.yml) | **Done** |
| 2.3 | Environment template | [.env.example](../.env.example) | **Done** |
| 2.4 | Architecture diagram | [architecture.md](architecture.md) | **Done** |
| 2.4 | Smoke tests | [tests/test_environment.py](../tests/test_environment.py) | **Done** |

---

## Exit Criteria Checklist

| Criterion | Status |
|-----------|--------|
| Requirements doc committed | ✅ |
| 4 ADRs committed | ✅ |
| `poetry install` succeeds on fresh clone | ✅ (use Python 3.10–3.12; in-project `.venv`) |
| Architecture diagram committed and rendering | ✅ (Mermaid in `architecture.md`) |

---

## Local Setup (verified)

```powershell
# Requires Python 3.10–3.12 (not 3.14 — PyTorch incompatible)
cd pk-pr-simulator
py -3.10 -m pip install poetry
py -3.10 -m poetry config virtualenvs.in-project true
py -3.10 -m poetry install
copy .env.example .env

# Postgres metadata store
docker compose up -d db

# Verify (10 tests pass; torch/transformers skip if Windows DLL issue — install VC++ redist or use CPU wheel)
py -3.10 -m poetry run pytest tests/ -q
```

**Note:** If `import torch` fails with `WinError 1114`, install [Microsoft VC++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe) or reinstall PyTorch CPU-only: `poetry run pip install torch --index-url https://download.pytorch.org/whl/cpu`

---

## Phase 3 Readiness

Proceed to **Data Foundation** once Phase 1 manual items are done (ethics approval before live API pulls):

- Download PBS / PTA / SBP → `data/external/`
- `src/population/frame_builder.py`
- `src/ingestion/schema.py` + connectors
- `src/nlp/text_normalize.py`

---

## Document History

| Date | Event |
|------|-------|
| 2026-06-25 | Phase 2 documentation, ADRs, stack, and architecture completed |
