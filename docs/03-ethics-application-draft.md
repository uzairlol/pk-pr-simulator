# University Ethics / IRB Application — Draft

**Document version:** 1.0  
**Date:** 2026-06-25  
**Status:** Draft — complete institution-specific fields, attach to official form, submit to IRB  
**Attachments to include:** [Project Charter](01-project-charter.md) (Section 3 non-goals), [Data Legal Notes](02-data-legal-notes.md)

> **Instructions:** Copy relevant sections into your university's official ethics application portal or PDF form. Replace all `[BRACKETED]` fields. Submit in **week 1** of the project; do not collect real platform data until approval is received.

---

## A. Applicant Information

| Field | Value |
|-------|-------|
| Principal investigator | `[Student name]` |
| Supervisor / faculty advisor | `[Supervisor name, department]` |
| Institution | `[University name, department]` |
| Student ID / registration | `[ID]` |
| Contact email | `[email]` |
| Project title | Pakistan-Focused Population Opinion Simulator for Company PR Scenario Forecasting |
| Funding source | `[None / HEC / university grant / self-funded]` |
| Expected project duration | `[e.g., 12–18 months]` |

---

## B. Study Summary (Plain Language)

This research develops and evaluates a **cohort-level simulation system** that helps analyze how public reactions to corporate PR scenarios in Pakistan's telecommunications sector might unfold over time. The system uses **publicly available** news articles, official government statistics, and **public** social-media posts/comments accessed through official APIs. It does **not** predict individual behavior, build marketing profiles, or contact private citizens.

Outputs are aggregate forecasts for predefined population segments (e.g., urban vs. rural, province-level cohorts) with uncertainty ranges and audit logs for academic reproducibility.

---

## C. Research Aims and Methods

### C.1 Aims

1. Build a reproducible pipeline from public data to cohort-level PR scenario forecasts.
2. Calibrate online discourse signals against Pakistan demographic structure (PBS/PSLM) and sector statistics (PTA).
3. Evaluate forecast quality on a curated set of historical telecom PR events in Pakistan.
4. Document governance safeguards for responsible use of AI-assisted public-opinion modeling.

### C.2 Methods (no covert or deceptive collection)

| Activity | Description | Personal data? |
|----------|-------------|----------------|
| Government statistics | Download PBS, PTA, SBP tables | No |
| News ingestion | RSS/official feeds from Pakistani news outlets | No (journalists named in bylines only as public figures) |
| Platform APIs | YouTube comments, Reddit posts via official APIs | Possibly — public pseudonymous handles |
| Annotation | 2–3 bilingual annotators label sentiment/stance on text samples | No collection from annotators beyond consent |
| Simulation | Mathematical models on cohort aggregates | No |

---

## D. Data Sources and Legal Basis

See attached `docs/02-data-legal-notes.md`. Summary:

- **Low risk:** PBS, PTA, SBP, GDELT (aggregate/event), news RSS.
- **Moderate risk (API-compliant, public content only):** YouTube Data API, Reddit Data API.
- **Conditional:** Meta Content Library only if research access approved.
- **Explicitly excluded:** Non-consensual scraping, bypassing access controls, private/group data not authorized for research.

**Legal basis / public interest:** Academic research in computational social science with data minimization; no commercial resale of raw feeds.

---

## E. Human Participants

### E.1 General public (indirect)

Members of the public may appear as authors of **public** social posts or comments. We do not interact with them, do not deceive them, and do not collect data beyond what is publicly accessible through approved APIs or feeds.

**Safeguards:**

- No individual-level forecasts or outputs (charter NG-1, NG-3).
- User identifiers stripped or hashed after deduplication where feasible.
- `retention_expiry` on stored documents; deletion job enforced.
- No inference of sensitive attributes (religion, ethnicity, etc.) (charter NG-4).

### E.2 Annotators (direct participants)

**Number:** 2–3 annotators (students or bilingual volunteers).  
**Task:** Label ~150-document pilot sample, then up to 3,000–6,000 documents for NLP training.  
**Time:** ~20–40 hours per annotator over project duration.  
**Risks:** Exposure to offensive public text; mitigated by content warnings, ability to skip abusive items, and no requirement to label graphic content.  
**Compensation:** `[Unpaid course credit / honorarium / volunteer — specify]`  
**Consent:** Written informed consent covering purpose, voluntary participation, withdrawal, and confidentiality of annotator identity in publications.

---

## F. Risks and Benefits

### F.1 Risks

| Risk | Likelihood | Severity | Mitigation |
|------|------------|----------|------------|
| Re-identification of platform users from stored quotes | Low | Moderate | Minimize IDs, aggregate early, retention limits, no public release of raw social JSON |
| Misuse of forecasts for manipulative targeting | Medium (external) | High | Charter non-goals; no individual-level features; publication emphasizes advisory/contestable outputs |
| Annotator distress from toxic content | Low–Medium | Low | Skip policy, guidelines, debrief contact |
| Non-representative online sample misread as "Pakistan" | Medium | Moderate | MRP calibration, uncertainty bands, explicit limitations in all outputs |
| ToS / legal non-compliance | Low | High | Legal notes doc, API-only access, ethics-gated collection start |

### F.2 Benefits

- Academic knowledge on calibrating multilingual, platform-skewed discourse for Pakistan.
- Open methodology and benchmark for responsible PR scenario analysis.
- Training value for student researchers in reproducible computational social science.

---

## G. Data Management

| Item | Policy |
|------|--------|
| Storage | Encrypted university laptop / approved cloud; Postgres metadata; raw files in gitignored `data/raw/` |
| Personal data | Minimized; no collection of annotator data beyond consent forms |
| Retention | Raw social documents: `[e.g., 24 months]` or until ethics-mandated deletion; government stats: permanent for reproducibility |
| Sharing | No public release of raw social JSON; processed aggregate benchmark and code on GitHub; model weights via Hugging Face with access controls if needed |
| Deletion | Automated `retention_expiry`; manual deletion on request if platform requires |
| Reproducibility | Audit logs with config hashes; no secrets in repository |

---

## H. Ethical Design Commitments (attach charter Section 3)

1. **No individual profiling** (NG-1)  
2. **No covert persuasion optimization** (NG-2)  
3. **No monolithic national opinion claims** (NG-3)  
4. **No sensitive-trait inference** (NG-4)  
5. **No ToS-violating collection** (NG-5)  
6. **No live surveillance product** (NG-6)  

---

## I. Conflict of Interest and Misuse

The researchers have no financial relationship with pilot telecom companies. The tool is for academic evaluation. A `docs/safeguards.md` document (Phase 10) will consolidate abuse-prevention language. Company dossiers use only public information.

---

## J. Timeline Relative to Ethics Approval

| Milestone | Requires approval? |
|-----------|-------------------|
| Literature review, charter, legal notes | No |
| Download PBS/PTA/SBP government data | `[Confirm with IRB — typically exempt]` |
| Live API pulls from YouTube/Reddit/news | **Yes** |
| Annotator recruitment | **Yes** |
| Simulation and backtest on archived data | **Yes** (if data collected post-approval) |

**Commitment:** No real platform data collection begins until written ethics approval is received.

---

## K. Submission Checklist

- [ ] Official university ethics form completed online or PDF
- [ ] This draft adapted to form field limits
- [ ] `docs/01-project-charter.md` attached (especially Section 3 non-goals)
- [ ] `docs/02-data-legal-notes.md` attached
- [ ] Annotator consent form draft attached (if required separately)
- [ ] Supervisor signature / endorsement
- [ ] Proof of submission saved to `docs/decisions/` or project records
- [ ] Approval letter filed when received — update this doc status to **Approved**

---

## L. Post-Approval Record

| Field | Value |
|-------|-------|
| IRB / ethics committee name | `[Committee name]` |
| Application reference number | `[REF]` |
| Submission date | `[DATE]` |
| Approval date | `[DATE]` |
| Expiry / renewal date | `[DATE]` |
| Conditions of approval | `[Any conditions]` |

---

## M. Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-06-25 | Initial draft for university submission |
