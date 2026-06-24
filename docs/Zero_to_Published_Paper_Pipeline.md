# From Zero Repo to Peer-Reviewed Paper: Full Execution Pipeline
### Pakistan-Focused Population Opinion Simulator for Company PR Scenario Forecasting

This is a literal, sequential build plan. Each phase has: what you do, in what order, with what tool, and what "done" looks like. Nothing is assumed. Follow phases in order — later phases depend on artifacts from earlier ones.

**Realistic timeline:** 12–18 months if you treat this as a real research program (2-semester build + 3–6 months to get a paper through review). The doc you uploaded already gives a 2-semester gantt for the *system*; this pipeline wraps that with everything before it (setup) and after it (publishing).

---

## PHASE 0 — Tooling, Accounts, and Repo (Day 1, ~1 day of setup)

### 0.1 Accounts you need before writing a line of code
1. GitHub account (if you don't have one): github.com/join.
2. Hugging Face account (huggingface.co/join) — for models/datasets later.
3. Weights & Biases account (wandb.ai) — free tier, for experiment tracking.
4. Google account with Colab Pro or access to a university GPU cluster (ask your department; most CS departments have a slurm cluster or a few A100/3090 boxes for thesis students).
5. Overleaf account (overleaf.com) — for the eventual thesis/paper in LaTeX.
6. Zotero account (zotero.org) — reference manager, install the browser connector now. You will accumulate 60–100+ references; do not do this by hand in Word.
7. ORCID ID (orcid.org/register) — you'll need this for the eventual paper submission. Takes 2 minutes, get it now.

### 0.2 Local machine setup
```bash
# Check what you have
git --version          # install from git-scm.com if missing
python3 --version      # need 3.10+
```
Install Python tooling:
```bash
curl -sSL https://install.python-poetry.org | python3 -   # or use plain venv if you prefer
python3 -m pip install --upgrade pip
```
Install Docker Desktop (docker.com) — you'll containerize the pipeline later so it runs identically on your laptop, your teammate's laptop, and any cloud GPU box.

### 0.3 Create the GitHub repository
```bash
mkdir pk-pr-simulator && cd pk-pr-simulator
git init
git branch -M main
```
On GitHub: create a new **empty** repo named `pk-pr-simulator` (no README, no .gitignore — you'll push your own). Then:
```bash
git remote add origin git@github.com:<your-username>/pk-pr-simulator.git
```
Create `.gitignore` (Python + data + secrets template — use GitHub's official Python template, then append):
```
data/raw/
data/interim/
*.env
.env.local
wandb/
*.ckpt
*.pt
```
Create `LICENSE` — for a university research project, MIT or Apache-2.0 is standard unless your university has IP rules requiring otherwise (**check with your supervisor/university research office before choosing a license** — some universities claim partial IP on student theses).

### 0.4 Repo skeleton
```bash
mkdir -p src/{ingestion,nlp,population,propagation,fusion,scenario,simulation,evaluation,explainability,dashboard,utils}
mkdir -p data/{raw,interim,processed,external}
mkdir -p notebooks tests docs configs scripts paper
mkdir -p docs/datasheets docs/decisions
touch README.md CONTRIBUTING.md CODE_OF_CONDUCT.md
```
`data/raw/` etc. should be **empty in git** (gitignored) — add `.gitkeep` files so the folder structure still exists for collaborators:
```bash
find data -type d -exec touch {}/.gitkeep \;
```

### 0.5 Project management
1. Create a GitHub Project (Projects tab → New project → Board template) with columns: Backlog / This Sprint / In Progress / Review / Done.
2. Create GitHub Issues for every phase below as an Epic, then break each into tasks. This *is* your task list — don't keep a separate to-do doc that drifts out of sync.
3. Set up branch protection on `main`: Settings → Branches → require PR review before merge (even if it's just your teammate reviewing, this builds the habit and gives you a clean commit history for your thesis appendix).

### 0.6 First commit
```bash
git add .
git commit -m "chore: initial repo skeleton"
git push -u origin main
```

**Phase 0 exit criteria:** repo exists on GitHub, skeleton folders pushed, project board created, all accounts above are live.

---

## PHASE 1 — Literature Review, Scoping Lock, Ethics Clearance (Weeks 1–4)

This phase produces zero code. Skipping or rushing it is the #1 reason these projects fail their defense or get rejected from review — committees and reviewers ask "why didn't you cite X" or "did you get ethics approval" before they ask about your model.

### 1.1 Systematic literature pull
Your doc already names the core literature. Pull every one of these into Zotero **today**, read abstracts, tag by layer:
- Forecasting systems: EMBERS, GDELT, Media Cloud, Hoaxy
- NLP: BERT (Devlin et al.), GoEmotions, SemEval sentiment/stance tasks, MAVEN
- Urdu/Roman Urdu NLP: the AbjadNLP 2026 paper and anything it cites
- Diffusion/opinion dynamics: bounded confidence models, Independent Cascade, Linear Threshold, Kleinberg's influence maximization paper
- Calibration: Gelman's MRP papers, Bayesian fusion references
- GNNs: Kipf & Welling GCN paper
- Explainability: SHAP (Lundberg & Lee)
- Forecast evaluation: Gneiting & Raftery on scoring rules
- Governance: NIST AI RMF, EU AI Act, GDPR text, Pakistan PECA 2016, Pakistan draft Personal Data Protection Bill

Build a **literature matrix** spreadsheet (Google Sheets, link it in `docs/`) with columns: citation, what it contributes, which of your layers it informs, gap it leaves for Pakistan. This spreadsheet becomes your Related Work section later — don't lose it.

### 1.2 Write the formal scoping document
Create `docs/01-project-charter.md`:
- One-paragraph problem statement (use the "aggregate decision-support system, not person-level prediction engine" framing — this is your ethical and methodological anchor, repeat it everywhere).
- Explicit list of **non-goals**: no individual profiling, no covert persuasion optimization, no claim of predicting "the Pakistani public" as a monolith.
- MVP scope lock: English-first, one sector (pick one: FMCG, telecom, or banking — telecom is attractive because PTA data is richest), one or two platform connectors, daily simulation steps.
- Success criteria for the MVP (be numeric: e.g. "beats text-only sentiment baseline by X% on held-out events").

Get your supervisor to sign off on this document in writing (email is fine) before building anything. This is the document you'll point to in your defense when asked "why didn't you do X."

### 1.3 University ethics review
Even though your design is aggregate/cohort-level, you are still touching:
- Scraped/API-derived social media data (which can contain personal data even if you don't use it that way)
- Survey-derived demographic data
- Possibly broadcast transcripts

**Action items:**
1. Find your university's Institutional Review Board / Ethics Review Committee (every accredited Pakistani university has one — ask your department; HEC requires it).
2. Fill out their human-subjects/data-ethics application. Key things to state explicitly: you minimize personal data, aggregate early, never build individual profiles, retention limits, no scraping where ToS forbid it.
3. Attach your non-goals list from 1.2.
4. Submit and wait — this can take 2–6 weeks depending on your university, so submit this in **week 1**, not after you've built the data pipeline. Do not collect any real platform data before approval lands.

### 1.4 Legal review of data sources
Before integrating any API, read its terms of service and write one paragraph per source in `docs/02-data-legal-notes.md`:
- Reddit Developer Terms + Data API Terms
- YouTube Data API Terms of Service + quota policy
- Meta Content Library access conditions (research-gated; you likely need to apply formally — start that application in this phase, approval can take weeks)
- News sites' robots.txt / ToS (Dawn, etc.) — prefer their official APIs/RSS over scraping HTML
- PBS, PTA, SBP — these are official government open-data sources, lowest legal risk, use freely with citation

**Phase 1 exit criteria:** literature matrix complete (40+ sources), charter signed off by supervisor, ethics application submitted, data legal notes written, Meta/YouTube API applications submitted (approval lag absorbed into your timeline now, not later).

---

## PHASE 2 — Requirements & Architecture Lock (Weeks 3–5, overlaps Phase 1)

### 2.1 Functional/non-functional requirements doc
`docs/03-requirements.md` — derive directly from your charter:
- FR: ingest company dossier; ingest Pakistan news/social signals; multilingual classification; cohort modeling; scenario-conditioned simulation; uncertainty-banded output; audit trail.
- NFR: traceability (every forecast must be reproducible from a logged seed+config), data minimization, deletion-aware storage, explainability, modest compute footprint (must run on a single GPU workstation).

### 2.2 Architecture decision records (ADRs)
For every major design choice, write a short ADR in `docs/decisions/` (template: context, decision, alternatives considered, consequences). Do this **as you decide**, not retroactively — your thesis Methods chapter is basically your ADR folder, reorganized. Minimum ADRs to write now:
- ADR-001: Three-layer architecture (perception/population/propagation) + fusion layer, vs. single end-to-end LLM agent simulator (rejected: cost + validation difficulty).
- ADR-002: MVP language scope (English-first, Urdu/Roman Urdu as extension).
- ADR-003: Tech stack (Section 2.3).
- ADR-004: Belief vs. visible-discourse separation (latent cohort opinion ≠ posting probability).

### 2.3 Tech stack — install everything now
```bash
poetry init  # or: python3 -m venv .venv && source .venv/bin/activate
poetry add torch transformers datasets accelerate
poetry add networkx python-igraph mesa
poetry add pandas pyarrow duckdb sqlalchemy psycopg2-binary
poetry add plotly dash streamlit
poetry add pymc arviz numpyro     # for Bayesian fusion / MRP
poetry add shap scikit-learn
poetry add pytest pytest-cov black ruff mypy
poetry add wandb
poetry add fastapi uvicorn        # if you expose an API for the dashboard
```
Postgres for metadata (Docker):
```bash
docker run --name pk-pr-db -e POSTGRES_PASSWORD=devpassword -p 5432:5432 -d postgres:16
```
Pin everything: `poetry lock`, commit `pyproject.toml` + `poetry.lock`.

### 2.4 Draw and commit the architecture diagram
Recreate the flowchart from your original doc (Company dossier / news / platform data / PBS demographics / survey priors → ingestion → NLP layer + cohort builder → network generator + fusion → simulation engine → forecasts + audit trail → dashboard) as an actual diagram — Mermaid (renders natively in GitHub markdown) or draw.io. Put it in `docs/architecture.md` and reference it everywhere. This is the single image every reader (supervisor, defense committee, paper reviewer) will look at first.

**Phase 2 exit criteria:** requirements doc + 4 ADRs committed, full dependency stack installs cleanly via `poetry install` on a fresh clone, architecture diagram committed and rendering.

---

## PHASE 3 — Data Foundation (Weeks 4–10)

### 3.1 Official statistical anchors (no legal risk, start here)
1. Download PBS 2023 census tables + PSLM/HIES microdata extracts from pbs.gov.pk. Store raw files in `data/external/pbs/`, write the download date + URL into a `SOURCES.md` manifest (you need this for reproducibility and for citing exact access dates in your paper).
2. Download PTA annual report tables (telecom/broadband/social media penetration) from pta.gov.pk.
3. Pull SBP exchange rate data if you need budget-normalization context (sbp.org.pk/ecodata).
4. If you can get a research data-sharing arrangement with Gallup Pakistan or PILDAT, formally email them now (academic requests often get a yes if you mention your university and explain the aggregate, non-commercial use) — this can take weeks, start early.

### 3.2 Build the demographic post-stratification frame
- Define cells: province × urban/rural × age band × (optionally) income tercile from PSLM/HIES.
- Build `src/population/frame_builder.py` that loads PBS/PSLM tables and outputs a clean cell-by-cell population-weight table (this is the backbone of your MRP step in Phase 5).
- Write a datasheet (`docs/datasheets/pbs_frame.md`) following the Datasheets-for-Datasets format: motivation, composition, collection process, known limitations.

### 3.3 Company dossier schema
Design a structured schema (Pydantic models in `src/ingestion/schema.py`) covering: brands/SKUs, executives, ownership signals, prior controversies, official messaging/CSR claims, labor issues, pricing history, regional footprint, linked issues (inflation, religion-sensitive controversy, etc.) — exactly the fields your original doc lists. Manually populate this for **2–3 pilot companies** in your chosen sector (telecom or FMCG) by reading public filings, news archives, and company CSR reports. This manual dossier-building work is tedious but is a real, citable contribution (your "public-profile knowledge graph").

### 3.4 Platform/news connectors — build one at a time, behind a common interface
Define an abstract `Connector` interface (`src/ingestion/base.py`) with `.fetch(query, since, until) -> list[RawDocument]`. Implement, in this order (easiest legal path first):
1. **News connector**: Dawn (and 2–3 other major Pakistani outlets) via RSS/sitemap where available, else their own search APIs if they have one. Respect robots.txt.
2. **GDELT connector**: GDELT's BigQuery/API access for global event context — straightforward, well-documented, no ToS friction.
3. **YouTube comments connector**: once your API key/quota approval is through, use the official `commentThreads` endpoint — note its documented completeness limits explicitly in your datasheet.
4. **Reddit connector**: via PRAW, complying with the Developer Terms + DPA you read in Phase 1.
5. **(Stretch) Meta Content Library**: only if your research-access application was approved.

Each connector writes raw JSON to `data/raw/<source>/<date>/`, with a manifest row in Postgres recording source, query, fetch timestamp, and a content hash (for dedup later).

### 3.5 Deduplication & lineage
- Build `src/ingestion/dedup.py`: near-duplicate detection across syndicated news (MinHash/SimHash on normalized text) — Pakistani news has heavy syndication, this matters more than it sounds.
- Every document gets a `source_id`, `lineage` (which connector, which query, fetch time), and a `retention_expiry` field from day one — this is your deletion-aware handling requirement, build it in now rather than retrofitting.

### 3.6 Urdu / Roman Urdu normalization
Build `src/nlp/text_normalize.py`:
- Unicode normalization for Urdu script (NFC, handle presentation-form variants).
- Roman Urdu spelling-variation normalizer (transliteration-aware fuzzy matching or a lookup table built from common variants — start with a rules-based pass, this is a legitimate small research contribution on its own if done carefully).
- Language/script identifier (fastText langid or a fine-tuned classifier) to tag each document as EN / Urdu-script / Roman-Urdu / code-mixed before anything downstream touches it.

**Phase 3 exit criteria:** PBS/PTA data loaded and frame-builder runs end-to-end; 2–3 company dossiers populated; at least 3 connectors live and pulling real (ethics-approved) data into Postgres with lineage and dedup; normalizer unit-tested on a held-out sample of 200 manually-checked Urdu/Roman-Urdu strings.

---

## PHASE 4 — Perception Layer / Multilingual NLP (Weeks 8–16)

### 4.1 Annotation
You cannot fine-tune without labeled Pakistan-specific data.
1. Stand up Label Studio (self-hosted, free) or use Hugging Face's `argilla`.
2. Write annotation guidelines (`docs/annotation-guidelines.md`) covering sentiment, stance (toward company), emotion (map to GoEmotions categories), event type, credibility cues.
3. Recruit 2–3 annotators (classmates, bilingual friends — disclose this in your ethics paperwork if it wasn't already covered) and have them label a shared sample of ~150 documents to compute inter-annotator agreement (Cohen's/Fleiss' kappa) before scaling up.
4. Once IAA is acceptable (κ > 0.6 is a reasonable bar to state and defend), annotate your target sample — aim for 3,000–6,000 labeled documents total across tasks; this is the realistic ceiling for a student team's annotation budget.

### 4.2 Model selection and baselines
- Start with multilingual encoder baselines: `xlm-roberta-base` for the multilingual case, plus an Urdu-specific checkpoint if one exists on Hugging Face Hub with decent community validation (check model cards critically).
- Fine-tune separate heads (or a multi-task head) for: sentiment, stance, emotion (GoEmotions-style), event-type (MAVEN-inspired schema adapted to PR/crisis events).
- Log every run to Weights & Biases: hyperparameters, metrics, confusion matrices, dataset version hash.

```bash
# example skeleton command you'll actually run
python -m src.nlp.train --task sentiment --model xlm-roberta-base \
  --train data/processed/sentiment_train.parquet \
  --eval data/processed/sentiment_eval.parquet \
  --output checkpoints/sentiment-v1 --wandb-project pk-pr-simulator
```

### 4.3 Entity resolution
Build a company/issue entity linker (`src/nlp/entity_resolution.py`): start with fuzzy string matching + alias tables from your dossiers (Phase 3.3), upgrade to a trained NER+linking model only if the rules-based pass demonstrably underperforms.

### 4.4 Evaluation
- Held-out test set, stratified by language/script.
- Report standard metrics (macro-F1 for classification tasks) **broken down by script** (Urdu vs Roman Urdu vs English) — this breakdown is itself a research finding worth a table in your paper, since your literature review already flags script-dependent performance gaps.

**Phase 4 exit criteria:** annotation guideline + IAA report committed; fine-tuned checkpoints for sentiment/stance/emotion/event-type pushed to a private Hugging Face Hub repo (or stored as release artifacts, not in git directly — model weights don't belong in git); per-script evaluation table produced.

---

## PHASE 5 — Population / Cohort Layer (Weeks 14–20)

### 5.1 Cohort definition
Operationalize the cohort list from your doc (urban digital consumers, rural consumers, price-sensitive households, loyal customers, employees, investors, journalists, activist communities, province/city groups) as a concrete set of post-stratification cells combining your PBS/PSLM frame with whatever proxy signals you can defensibly attach to platform users (e.g., self-declared location, language/script as a rough proxy — **never** infer sensitive traits like religion or ethnicity algorithmically; state this as a hard rule in code comments and in your ethics doc).

### 5.2 Multilevel regression and post-stratification (MRP)
- Implement in PyMC or NumPyro (`src/population/mrp_model.py`): a hierarchical model predicting cohort-level opinion/sentiment as a function of demographic cell, with partial pooling across provinces.
- Calibrate against whatever survey priors you secured in Phase 3.1 (Gallup Pakistan/PILDAT/Pew where topically relevant).
- Validate with posterior predictive checks; plot calibration curves.

**Phase 5 exit criteria:** MRP model runs end-to-end on real PBS/PSLM frame + at least one survey prior dataset, produces cohort-level posterior estimates with credible intervals, posterior predictive checks documented in a notebook.

---

## PHASE 6 — Propagation / Diffusion Layer (Weeks 18–24)

### 6.1 Multiplex network construction
`src/propagation/network_builder.py`: build a graph where nodes are users/outlets/issues and edges represent follow/reply/share relations (from your platform connectors) plus a media-exposure edge type connecting outlets to cohorts. Use NetworkX for prototyping, switch to igraph for anything beyond ~100k nodes (NetworkX gets slow fast).

### 6.2 Opinion dynamics implementation
Implement the bounded-confidence update rule your doc specifies:
- `src/propagation/opinion_dynamics.py`: cohort opinion at time *t+1* as a function of event severity, media exposure, peer influence (gated by a bounded-confidence threshold), company response quality, and persistence/decay.
- Keep this as an explicit, inspectable equation with logged parameters per run — not a black box. This is exactly the kind of explicit, auditable mechanism that distinguishes your project from a generic LLM-agent simulator, and it's a major selling point in your eventual paper's framing.

### 6.3 Diffusion baselines
Implement Independent Cascade and Linear Threshold (`src/propagation/diffusion_baselines.py`) as interpretable baselines you will compare your full model against in evaluation — these are required for Phase 9's ablation study, build them now.

### 6.4 (Stretch, post-MVP) GNN extension
Only after 6.1–6.3 work and are evaluated: implement a GCN/GraphSAGE model (PyTorch Geometric) for contagion-risk scoring or stance propagation over the interaction graph. Treat this as an ablation arm, not a dependency.

**Phase 6 exit criteria:** network builder produces a real multiplex graph from ingested data; bounded-confidence model and both diffusion baselines run on at least one historical pilot event end-to-end.

---

## PHASE 7 — Fusion & Calibration Layer (Weeks 22–26)

### 7.1 Bayesian fusion
`src/fusion/bayesian_fusion.py`: combine (a) MRP survey-calibrated priors, (b) platform-derived evidence (NLP layer outputs aggregated to cohort level), and (c) event-severity terms from the scenario encoder into a posterior forecast with explicit uncertainty bands. This is the layer that prevents a viral but unrepresentative social-media spike from overriding your demographic-grounded priors — state this explicitly as a design property in your writeup, it's a direct answer to the "representativeness" problem your original doc identifies as the central risk.

### 7.2 Scenario encoder
`src/scenario/encoder.py`: turn a structured hypothetical event (price hike, safety incident, executive controversy, boycott call, apology, regulatory action, CSR campaign, misinformation wave) into the feature vector the fusion/propagation layers consume. Define this schema carefully — it's the main user-facing "input" of your whole system.

**Phase 7 exit criteria:** given a scenario spec + a company dossier, the fusion layer outputs a calibrated forecast trajectory with uncertainty bands, runnable end-to-end from a single config file.

---

## PHASE 8 — Simulation Orchestration (Weeks 24–28)

### 8.1 Time-stepped engine
Use Mesa to wrap perception+population+propagation+fusion into a daily time-stepped simulation (`src/simulation/engine.py`). Every run takes a YAML config (`configs/run_*.yaml`) specifying: company, scenario, date range, random seed, model checkpoint versions.

### 8.2 Experiment tracking and audit trail
Every run logs to W&B *and* writes a local audit record (`src/utils/audit.py`) capturing: seed, full config, source document IDs used, model checkpoint hashes, calibration settings, output forecast + uncertainty. This is non-negotiable per your own design doc's governance requirements — and it's also exactly what a thesis committee or peer reviewer will ask "can you reproduce this specific number" about.

**Phase 8 exit criteria:** one command (`python -m src.simulation.run --config configs/run_pilot1.yaml`) reproduces a full simulation end-to-end from raw data to forecast, with a complete audit record written to disk.

---

## PHASE 9 — Evaluation & Backtesting (Weeks 26–32)

### 9.1 Build the historical event benchmark
Manually curate 15–30 real Pakistan-relevant corporate/PR events (price hikes, safety incidents, etc.) across 2–3 sectors, with: event date, scenario label, company response coding, and ground-truth discourse trajectory (volume/sentiment over time, reconstructed from your archived data). Document this as a dataset in `docs/datasheets/backtest_events.md` — this benchmark, if clean, is independently publishable as a resource paper later.

### 9.2 Splits and protocol
- Time-based train/validation/test split (train on earlier events, test on later ones — never shuffle randomly, that leaks future information).
- Held-out **company** split (some companies never appear in training) to test generalization, not just memorization of a company's specific history.
- Component ablations: full system vs. text-only sentiment baseline vs. event-volume-only baseline vs. pure diffusion baseline (your Phase 6.3 outputs).

### 9.3 Metrics
- Probabilistic accuracy: Brier score, CRPS (continuous ranked probability score) for trajectory forecasts — cite Gneiting & Raftery for why proper scoring rules matter here.
- Calibration plots (reliability diagrams) for your uncertainty bands.
- Standard classification metrics for the perception layer (already done in Phase 4, reuse/aggregate here).

**Phase 9 exit criteria:** a single `evaluation/run_backtest.py` script produces a results table (full system vs. each baseline, on time-based and company-holdout splits) with calibration plots — this table is the centerpiece of both your thesis Results chapter and your eventual paper.

---

## PHASE 10 — Explainability & Governance Hardening (Weeks 30–34, overlaps Phase 9)

1. SHAP attributions for the discriminative (NLP/classification) components (`src/explainability/shap_layer.py`).
2. Global explanation view: which events/cohorts/topics/sources/network paths moved a given forecast most — this can literally be a query over your Phase 8 audit records plus a feature-importance pass on the fusion layer.
3. Finalize datasheets for **every** locally-assembled dataset (annotation set, backtest benchmark, dossiers).
4. Write `docs/safeguards.md` consolidating: data minimization rules actually enforced in code (point to the retention_expiry field from Phase 3.5), cohort-only output guarantee (point to a code-level check that no individual-level output path exists), abuse-prevention notes, and the "forecasts are advisory and contestable" policy statement.

**Phase 10 exit criteria:** explanation outputs render for at least 3 backtest cases; all datasheets complete; safeguards doc complete and cross-referenced to specific code locations (not just prose promises).

---

## PHASE 11 — Dashboard / Productization (Weeks 32–36)

1. Build a Streamlit or Plotly Dash app (`src/dashboard/app.py`): scenario editor (pick company, pick scenario type, set severity/timing parameters) → trajectory forecast plot with uncertainty bands → explanation panel (Phase 10 outputs) → audit trail viewer.
2. Network visualization panel via Cytoscape.js (embed in the Dash app or a separate lightweight page) showing cohort-level diffusion structure for a selected run.
3. Containerize: `Dockerfile` + `docker-compose.yml` wiring Postgres + the dashboard app together, so a committee member or reviewer can run `docker compose up` and see it live.

**Phase 11 exit criteria:** `docker compose up` on a fresh machine brings up a working demo against at least the backtest pilot data.

---

## PHASE 12 — Testing, CI/CD, Documentation Polish (continuous, finalize Weeks 34–36)

1. Unit tests for every module under `src/` (`pytest`, target meaningful coverage on ingestion/normalization/fusion logic — not vanity 100%, but real coverage of the parts most likely to silently break).
2. GitHub Actions workflow (`.github/workflows/ci.yml`): run `ruff`, `mypy`, `pytest` on every PR.
3. Set up `mkdocs` or just a clean `docs/` README tree as your documentation site; deploy to GitHub Pages if you want a public-facing project site (nice for your CV/portfolio regardless of the paper outcome).
4. Tag a release: `git tag v1.0-mvp && git push --tags`. Attach model checkpoints and the backtest dataset as release assets (not committed to git history directly).

**Phase 12 exit criteria:** CI green on `main`; a tagged v1.0 release exists with attached artifacts.

---

## PHASE 13 — Thesis Writing (Weeks 30–40, overlaps heavily with Phases 9–12)

Start writing the moment Phase 9 produces real numbers — do not wait until everything is "finished." Structure (standard CS thesis):

1. **Abstract** (write last, even though it's first).
2. **Introduction** — problem, why Pakistan-specific, why aggregate-not-individual framing matters, contributions list (this maps directly to your charter from Phase 1.2).
3. **Related Work** — your Phase 1.1 literature matrix, organized by layer (forecasting systems, multilingual NLP, diffusion models, calibration, governance frameworks), ending with an explicit gap statement.
4. **Data** — PBS/PSLM frame, dossiers, connectors, normalization, annotation, datasheets (Phases 3–4). Include your honest limitations (Meta access gating, ASR being out of MVP scope, etc. — your original doc already names these, use them verbatim as your stated limitations).
5. **Methods** — your ADRs (Phase 2.2) turned into prose: perception/population/propagation/fusion architecture, the opinion-update equation, MRP, diffusion baselines.
6. **Experiments & Results** — Phase 9's backtest table, ablations, calibration plots, per-script NLP performance breakdown from Phase 4.4.
7. **Explainability & Governance** — Phase 10 outputs and safeguards.
8. **Discussion** — what worked, what the representativeness problem still means for interpretation, honest discussion of remaining risk.
9. **Limitations & Future Work** — broadcast/ASR integration, GNN extension, expanding the backtest benchmark.
10. **Ethics statement** — your Phase 1.3 approval, your non-goals, your safeguards doc.
11. **Conclusion**.

Set up the Overleaf project now, use your university's official thesis LaTeX template if one exists (ask your department — most do). Share the Overleaf project with your supervisor for inline comments.

**Weekly cadence:** send your supervisor a draft chapter every 1–2 weeks; do not save all writing for the final month.

**Phase 13 exit criteria:** full draft, supervisor sign-off, formatted per university requirements, submitted to your department by their deadline.

---

## PHASE 14 — Defense / Viva (Week ~40)

1. Build a 15–20 slide deck (Beamer or Google Slides) mirroring the thesis structure, leading with the architecture diagram and the backtest results table — those two slides carry most of the weight.
2. Rehearse the live demo from Phase 11's Docker setup on the **actual machine/network** you'll present on, beforehand — demo failures during a defense are avoidable and embarrassing.
3. Prepare answers for the obvious challenge questions: "how do you know this isn't just memorizing a few companies," "how is this different from just a sentiment dashboard," "what stops misuse for actual persuasion targeting" — your ADRs, ablations, and safeguards doc are literally your answers, know them cold.

**Phase 14 exit criteria:** thesis defended/passed.

---

## PHASE 15 — From Thesis to a Submittable Paper (Weeks 38–46, can overlap defense prep)

A thesis is not a paper. Reviewers want a tight, novel, well-evidenced 6–10 page argument, not a comprehensive narrative.

### 15.1 Pick the right venue (do this early — it determines format and even what experiments matter)
Realistic options for work at this stage, roughly easiest-to-hardest acceptance bar:
- **Regional/specialized workshops**: something like the AbjadNLP workshop track (already in your literature list) is a strong fit if you lean into the Urdu/Roman-Urdu NLP contribution specifically.
- **Computational social science venues**: ICWSM, WWW (Web Conf) workshops, ASONAM — good fit for the cohort/diffusion/calibration framing.
- **Regional CS conferences in Pakistan/South Asia** (e.g., university-hosted or HEC-recognized conferences) — lower bar, good first publication, useful before aiming higher.
- **Journal route**: a computational social science or applied AI journal if you want the fuller system contribution in one place rather than splitting it.

**Practical advice:** your single system has at least 2–3 separable papers in it (the Urdu/Roman-Urdu NLP + script-performance findings; the calibrated cohort-diffusion simulator + backtest benchmark; the governance/safeguard design pattern). Splitting increases your total publication count and each paper's clarity — discuss this explicitly with your supervisor before writing the paper.

### 15.2 Reshape content for the chosen venue
1. Get the venue's LaTeX template (most use ACL-style, ACM-style, or IEEE-style — set this up in a **new** Overleaf project, don't just trim the thesis file).
2. Cut Related Work down to the essential comparisons; cut Data/Methods to what's needed to reproduce your specific results, push extended detail to an appendix or a linked technical report.
3. Make sure the **one** clearest result (your backtest table) is presented within the first 2 pages of the results section, not buried.
4. Write a sharp, specific contributions list (3–4 bullet points) in the introduction — this is what gets skimmed by reviewers and program-committee members during bidding.

### 15.3 Internal review before submission
1. Have your supervisor review the full draft.
2. Get 1–2 peers (lab-mates, other faculty) to do a "cold read" — someone who hasn't seen the project should be able to follow the abstract+intro alone. If they can't, revise.
3. Run it past a release/IP check with your university (some require sign-off before external submission) and confirm anonymization requirements if the venue is double-blind (remove names, GitHub repo links that reveal identity, acknowledgments).

**Phase 15 exit criteria:** camera-ready-quality draft in the venue's template, internally reviewed, anonymized if required.

---

## PHASE 16 — Submission and Peer Review Cycle (Weeks 46–56+, mostly waiting + 2–4 weeks of active revision)

1. Create an account on the venue's submission system (most modern venues use **OpenReview**; older ones use **EasyChair** or **CMT** or **Microsoft CMT**). Do this well before the deadline — system glitches at the last hour are common.
2. Submit: paper PDF, supplementary material (your code repo link — anonymized fork if double-blind, or a real link if not), and any required ethics/reproducibility checklist (many venues now require an explicit "ethics statement" and a "limitations" section — you already have both from Phase 13).
3. **Wait.** Review periods typically run 6–10 weeks. Use this time productively: keep improving the codebase, start drafting paper #2 from the split in 15.1, or start the next backtest expansion.
4. **Reviews arrive.** Read all reviews fully before reacting to any single one. Categorize feedback into: (a) factual misunderstandings you can clarify, (b) valid weaknesses needing new experiments, (c) scope disagreements you'll respectfully push back on.
5. **Rebuttal/response period** (if the venue has one): write a point-by-point response, be precise and non-defensive, run any small additional experiment reviewers specifically asked for if feasible in the window.
6. **Decision**: accept / accept-with-minor-revisions / reject.
   - If accepted: proceed to Phase 17.
   - If rejected: revise based on reviewer feedback (this feedback is valuable even outside that venue) and resubmit to your next-choice venue from the list in 15.1. This is completely normal — most published papers were rejected at least once first.

**Phase 16 exit criteria:** acceptance decision received (possibly after one resubmission cycle).

---

## PHASE 17 — Camera-Ready and Publication (Weeks 56–60)

1. Address all "minor revisions" / camera-ready instructions exactly as specified (formatting, page limit, required sections).
2. Complete the copyright/license transfer or open-access form the venue requires.
3. Register for the conference if it's conference-based (budget for this — ask your department about HEC/university travel or registration grants for student authors, these often exist and are underused).
4. **Post a preprint** to arXiv (cs.CL or cs.SI category fits) at or around acceptance, if the venue allows it (most do, check their policy) — this maximizes visibility and citation count regardless of venue prestige.
5. Make the final code release on GitHub: tag `v1.0-paper`, write a clean top-level README pointing to the paper, update the citation block (`CITATION.cff` file — GitHub renders this automatically as a "cite this repository" button).
6. Update your CV/LinkedIn/ORCID with the publication; link the GitHub repo and arXiv preprint from your ORCID profile.

**Phase 17 exit criteria:** paper published (proceedings or journal issue), preprint live, repo tagged and citable, ORCID updated.

---

## Cross-Cutting Things to Maintain the Entire Time

- **Weekly supervisor check-ins** from Phase 1 onward — don't go silent for a month, it's the single biggest derailment risk in projects this long.
- **Keep the audit trail discipline from day one** — retrofitting reproducibility in month 8 is far more painful than building it in during Phase 3.
- **Re-read your own non-goals list (Phase 1.2) every time you're tempted to add an individual-level feature** — scope creep into person-level prediction is both an ethical risk and the single fastest way to get desk-rejected by a reviewer or flagged by your ethics committee.
- **Budget for API/data approval lag** (Meta Content Library, Gallup/PILDAT data-sharing requests) by starting those applications in Phase 1, not when you need the data in Phase 3.

---

## One-Page Timeline Summary

| Phase | Weeks | Output |
|---|---|---|
| 0. Setup | 1 (day) | Repo, accounts, skeleton |
| 1. Lit review + ethics | 1–4 | Charter, ethics approval, lit matrix |
| 2. Architecture | 3–5 | Requirements, ADRs, stack installed |
| 3. Data foundation | 4–10 | Frame, dossiers, connectors, normalizer |
| 4. Perception/NLP | 8–16 | Fine-tuned classifiers, IAA report |
| 5. Population/MRP | 14–20 | Calibrated cohort posteriors |
| 6. Propagation | 18–24 | Network + opinion dynamics + baselines |
| 7. Fusion | 22–26 | Calibrated forecasts w/ uncertainty |
| 8. Orchestration | 24–28 | One-command reproducible simulation |
| 9. Evaluation | 26–32 | Backtest benchmark + results table |
| 10. Explainability | 30–34 | SHAP, datasheets, safeguards doc |
| 11. Dashboard | 32–36 | Dockerized demo |
| 12. CI/Docs | 34–36 | CI green, v1.0 tagged |
| 13. Thesis writing | 30–40 | Submitted thesis |
| 14. Defense | ~40 | Passed defense |
| 15. Paper reshaping | 38–46 | Camera-ready-quality draft |
| 16. Submission/review | 46–56+ | Decision (possibly 1 resubmit cycle) |
| 17. Publication | 56–60 | Published + preprint + tagged repo |

This is long because the ask was for *every* step, not the abridged version — but every phase above maps to something already justified in your original project brief, so none of it is scope you're inventing; it's the brief's architecture made executable.
