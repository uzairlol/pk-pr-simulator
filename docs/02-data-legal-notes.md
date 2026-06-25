# Data Source Legal and Terms-of-Service Notes

**Document version:** 1.0  
**Date:** 2026-06-25  
**Status:** Phase 1 legal review complete — re-review before each new connector goes live  
**Related:** [Project Charter](01-project-charter.md) · [Ethics Application Draft](03-ethics-application-draft.md)

This document records a paragraph-level legal/ToS assessment for each data source planned in the MVP. It is **not legal advice**. Final compliance decisions should be confirmed with the university research office or legal counsel if uncertain.

**General principles enforced in code (from charter non-goals):**

- Prefer official APIs, RSS, and open government data over HTML scraping.
- Aggregate early; do not retain raw personal identifiers beyond documented retention windows.
- Honor `robots.txt`, rate limits, and deletion/expiry fields on every ingested document.
- Do not collect from any source until university ethics approval is granted.

---

## 1. Reddit — Developer Terms + Data API Terms

**Sources reviewed:** [Reddit Developer Terms](https://www.redditinc.com/policies/developer-terms), [Reddit Data API Terms](https://www.redditinc.com/policies/data-api-terms), [Responsible Builder Policy](https://www.redditinc.com/policies/responsible-builder-policy).

Reddit permits access to public content through the official Data API when developers register an application, authenticate, and comply with rate limits, attribution requirements, and prohibitions on commercial resale of bulk data. The API terms restrict using Reddit data to infer sensitive personal attributes, target individuals for surveillance, or build profiles for harassment or discrimination. For this project, Reddit is used only to fetch **public posts and comments** matching company/sector keywords within declared date ranges; content is stored with source lineage, deduplicated, and **aggregated to cohort-level signals** before any forecast output. User identifiers are minimized (hashed or dropped after deduplication where feasible), retention expiry is enforced, and no individual-level output path exists. PRAW or direct REST calls must respect current per-minute rate limits; a deleted-content sync process is required if we later store IDs long-term. **Risk level: moderate** — acceptable for academic research if ethics-approved and API-compliant; not suitable as a sole representative sample of Pakistan.

---

## 2. YouTube — Data API Terms of Service + Quota Policy

**Sources reviewed:** [YouTube API Services Terms of Service](https://developers.google.com/youtube/terms/api-services-terms-of-service), [Developer Policies](https://developers.google.com/youtube/terms/developer-policies), [Quota and Compliance Audit](https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits).

YouTube Data API access requires a Google Cloud project, API key or OAuth credentials, and adherence to quota units (default 10,000 units/day unless extension approved). The terms prohibit storing or aggregating YouTube data in ways that enable individual tracking outside permitted use, prohibit circumventing access controls, and require displaying YouTube attribution where applicable. Comment retrieval via `commentThreads.list` is **documented as incomplete** relative to all comments on high-volume videos — this limitation must appear in datasheets and papers. This project uses the API only for **public comments** on videos related to pilot telecom companies and sector events; comments are normalized, classified, and aggregated; no attempt is made to deanonymize or contact commenters. Quota budgeting and an extension request should be filed before large historical backfills. **Risk level: moderate** — acceptable with API key, quota plan, and ethics approval.

---

## 3. Meta — Content Library (Research Access)

**Sources reviewed:** [Meta Content Library for Research](https://transparency.meta.com/researchtools/meta-content-library), application requirements and affiliated-institution policies as published at time of review.

Meta's Content Library is **research-gated**: access typically requires affiliation with an eligible research institution, a formal application describing the research question, IRB/ethics approval documentation, and acceptance of Meta's research data use agreements. Bulk public scraping of Facebook/Instagram without authorization violates Meta's Terms of Service and is **explicitly out of scope** for this project (charter NG-5). If access is granted, use is limited to aggregate research queries permitted under the agreement; individual-level export for profiling is prohibited. Given approval latency (weeks to months), Meta is a **stretch connector**, not an MVP dependency. Application checklist: `docs/04-api-access-checklist.md`. **Risk level: high without approval; low–moderate with approved research access.**

---

## 4. Pakistani News Outlets — RSS, Sitemaps, robots.txt, and ToS

**Outlets in scope for MVP:** Dawn (`dawn.com`), The Express Tribune (`tribune.com.pk`), and one additional major English-language outlet (e.g., Business Recorder or Geo News English sections) selected by RSS availability.

**Sources reviewed:** per-outlet `robots.txt`, terms of use pages, and available RSS/sitemap endpoints.

Dawn and major Pakistani outlets generally permit automated access to **published RSS feeds and sitemaps** intended for syndication, while restricting bulk HTML scraping that imitates a browser crawler or republishes full article text commercially. This project prefers **RSS titles, summaries, and canonical URLs**; full article text is retrieved only where licensing/ToS clearly allow reading for non-commercial research, or where excerpts fall under fair dealing/fair use as advised by the university. `robots.txt` is checked before any crawler deployment and cached with a review date. Rate limiting (≤ 1 request/second per host unless otherwise allowed) and clear `User-Agent` identifying the academic project are required. Syndicated duplicate articles are deduplicated (MinHash/SimHash). **Risk level: low–moderate** when using official feeds; **high** if ignoring robots.txt or republishing paywalled content at scale.

---

## 5. GDELT — Global Database of Events, Language, and Tone

**Sources reviewed:** [GDELT Project](https://www.gdeltproject.org/), [GDELT Cloud / BigQuery documentation](https://blog.gdeltproject.org/announcing-the-gdelt-cloud/).

GDELT provides open event and media monitoring data intended for research and analysis. Access via public file exports or BigQuery is subject to GDELT's documented use policies; commercial resale of raw feeds is restricted, but academic analysis and derivative aggregate statistics are standard use. GDELT rows may contain URLs and snippets from global media including Pakistani outlets; we filter geographically and thematically to Pakistan-relevant and telecom-sector events. No individual social-media identities are sourced from GDELT for profiling. **Risk level: low** for academic aggregate forecasting with attribution.

---

## 6. PBS — Pakistan Bureau of Statistics (Census, PSLM, HIES)

**Sources reviewed:** [pbs.gov.pk](https://www.pbs.gov.pk/) publication pages, table download terms as stated on site.

PBS publishes official census tables, Pakistan Social and Living Standards Measurement (PSLM), and Household Integrated Economic Survey (HIES) microdata extracts for statistical purposes. Government statistics are the **lowest legal-risk anchor** for population post-stratification: province, urban/rural, age, income, and education cells. Data is stored in `data/external/pbs/` with download URL, date, and table version in `SOURCES.md`. Redistribution of microdata may require citing PBS and adhering to any survey confidentiality rules (typically no attempt to identify households). **Risk level: low** — use freely with proper citation and confidentiality respect.

---

## 7. PTA — Pakistan Telecommunication Authority Annual Reports

**Sources reviewed:** [pta.gov.pk](https://www.pta.gov.pk/) annual reports and statistical publications.

PTA publishes official sector statistics: mobile/broadband subscribers, operator market share, social-media usage surveys, and regulatory orders. These are public regulatory publications intended for policy and industry analysis. This project extracts **aggregate penetration and usage tables** to calibrate platform-representativeness weights in the population layer. **Risk level: low** — use with citation; no restrictions beyond standard government attribution.

---

## 8. SBP — State Bank of Pakistan Ecodata

**Sources reviewed:** [sbp.org.pk/ecodata](https://www.sbp.org.pk/ecodata/) and related statistical releases.

SBP ecodata provides macroeconomic time series (exchange rates, inflation indices, policy rates) useful for normalizing pricing-related PR scenarios (e.g., tariff hikes during currency depreciation). Data is open for research with source attribution. No personal data is involved. **Risk level: low.**

---

## 9. Survey Priors — Gallup Pakistan, PILDAT, Pew (Optional)

**Sources reviewed:** publisher-specific data-sharing policies; no bulk data acquired without written agreement.

Third-party survey microdata is **not assumed available**. Academic data-sharing requests must be emailed formally, describing aggregate non-commercial use, ethics approval, and deletion policies. Until an agreement exists, only **published topline statistics** from reports may be used as calibration priors with citation. Storing identifiable survey respondent records is out of scope unless a DUA explicitly permits it under ethics approval. **Risk level: low for published tables; moderate–high for microdata without DUA.**

---

## 10. Pakistan Legal and Governance Context

**Sources reviewed:** Prevention of Electronic Crimes Act (PECA) 2016; draft Personal Data Protection Bill (as publicly circulated); university ethics requirements (HEC-aligned).

PECA criminalizes unauthorized access to data and certain forms of online harassment; it reinforces that data collection must respect platform authorization and lawful access paths — reinforcing charter NG-5. Pakistan's evolving personal data protection framework imposes duties of purpose limitation, retention limits, and security even when processing is research-oriented; this project's data-minimization, aggregation-first, and `retention_expiry` design are intended to align with these principles. EU GDPR and NIST AI RMF are referenced as **governance design influences**, not jurisdictional mandates, unless the university or a data provider contract requires otherwise. **Risk level: compliance depends on execution** — ethics approval and this document's technical safeguards are mandatory.

---

## 11. Re-Review Triggers

Re-read and update this document when:

- Adding a new connector or changing from RSS to HTML scrape
- Receiving a platform compliance audit request (notably YouTube)
- Meta or survey-provider DUA terms change
- University legal office issues new guidance
- Ethics approval conditions impose additional constraints

---

## 12. Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-06-25 | Initial Phase 1 legal review for MVP sources |
