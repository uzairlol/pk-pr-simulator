# ADR-002: MVP Language Scope — English-First with Urdu/Roman Urdu Extension

**Status:** Accepted  
**Date:** 2026-06-25  
**Deciders:** Project team  
**Related:** [Charter §4.2](../01-project-charter.md) · [Requirements FR-3](../03-requirements.md)

## Context

Pakistani public discourse is multilingual: English, Urdu script, Roman Urdu, code-mixing, and regional languages. The perception layer needs labeled data and models for each script. AbjadNLP 2026 and related work show Urdu-specific modeling is feasible but data and annotation cost are non-trivial for a student team.

The charter must lock MVP scope to ship a backtestable system within thesis timeline while preserving a credible path to multilingual contribution (per-script evaluation table is itself a research finding).

## Decision

**MVP is English-first:**

- Ingestion, annotation, fine-tuning, and backtest pass/fail use **English documents** as the primary corpus for telecom PR events.
- **Urdu-script and Roman Urdu** are handled as an **extension track** in parallel:
  - `src/nlp/text_normalize.py` for Unicode normalization and Roman Urdu variant handling.
  - Language/script identifier tags all documents.
  - Per-script evaluation breakdown reported in Phase 4 (Should-have, not MVP blocker).

MVP success criteria SC-3 apply to **English held-out test set**. Urdu/Roman Urdu targets are reported as extension metrics, not gating.

## Alternatives considered

| Option | Pros | Cons |
|--------|------|------|
| **A. English-first + extension (chosen)** | Achievable annotation budget; clear MVP gate; still publishes script-gap findings | Under-represents Urdu-dominant discourse in MVP forecasts |
| **B. Full multilingual parity at MVP** | Stronger Pakistan validity | 3–6k labels × multiple scripts exceeds team capacity; delays all layers |
| **C. Urdu-only MVP** | Locally authentic | Excludes large English-language business media and international coverage; harder PTA/news alignment |
| **D. Translate-all-to-English** | Single model | Translation errors on code-mixed text; loses Roman Urdu social signal; poor research contribution |

## Consequences

**Positive:**

- Annotation guidelines and IAA pilot can start immediately on English news/social samples.
- `xlm-roberta-base` still used for extension experiments without blocking MVP.
- Paper can include "script-stratified performance gap" table as explicit contribution.

**Negative:**

- MVP forecasts may under-weight Urdu-dominant cohorts until extension is complete.
- Must state limitation prominently in thesis and dashboard.

**Follow-ups:**

- Phase 3.6: normalizer unit tests on 200 manually-checked Urdu/Roman strings.
- Phase 4.4: macro-F1 broken down by script even if MVP gates on English only.
