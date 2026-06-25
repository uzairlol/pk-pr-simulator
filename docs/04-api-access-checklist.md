# API and Research Data Access Checklist

**Document version:** 1.0  
**Date:** 2026-06-25  
**Purpose:** Track long-lead access applications started in Phase 1  
**Related:** [Data Legal Notes](02-data-legal-notes.md) · [Ethics Application Draft](03-ethics-application-draft.md)

Platform and survey data approvals often take **2–8 weeks**. Start all applications in Phase 1 even if connectors are built in Phase 3.

---

## 1. YouTube Data API (Google Cloud)

### Status

| Step | Done | Date | Notes |
|------|------|------|-------|
| Create Google Cloud project | [ ] | | |
| Enable YouTube Data API v3 | [ ] | | |
| Create API key (restrict by IP/API) | [ ] | | |
| Store key in `.env` (never commit) | [ ] | | |
| Document daily quota budget | [ ] | | Default 10,000 units/day |
| Submit quota extension request (if backfill needed) | [ ] | | [Extension form](https://support.google.com/youtube/contact/yt_api_form) |
| Complete compliance audit questionnaire if requested | [ ] | | |

### Project description (for quota extension)

> Academic research at `[University]`: retrieving **public** YouTube comments (`commentThreads.list`) on videos related to Pakistan telecommunications sector PR events for aggregate sentiment/stance analysis. No individual profiling; data aggregated to cohort level; retention limits enforced. Ethics approval: `[REF or pending]`.

### MVP endpoints

- `search.list` — discover videos by keyword (quota-heavy; minimize)
- `videos.list` — metadata
- `commentThreads.list` — primary discourse signal

---

## 2. Reddit Data API (PRAW)

### Status

| Step | Done | Date | Notes |
|------|------|------|-------|
| Create Reddit account for project | [ ] | | |
| Register script/app at reddit.com/prefs/apps | [ ] | | |
| Store client_id / secret in `.env` | [ ] | | |
| Read Developer Terms + Data API Terms | [x] | 2026-06-25 | See legal notes |
| Implement rate-limit handling | [ ] | | Phase 3 |
| Document subreddits and keywords | [ ] | | e.g., r/pakistan, company names |

### Project description

> Non-commercial academic research: fetch public posts/comments mentioning Pakistan telecom operators and PR-related events; aggregate for cohort-level simulation; comply with Responsible Builder Policy.

---

## 3. Meta Content Library for Research

### Status

| Step | Done | Date | Notes |
|------|------|------|-------|
| Confirm institution on eligible list | [ ] | | |
| Supervisor affiliation verified | [ ] | | |
| Ethics approval obtained or proof of submission | [ ] | | Often required with application |
| Submit Content Library application | [ ] | | [Meta research tools](https://transparency.meta.com/researchtools/meta-content-library) |
| Complete data use training / agreement | [ ] | | |
| Access granted | [ ] | | **Stretch goal — not MVP blocker** |

### Suggested application summary

> We study aggregate public-reaction dynamics to corporate PR scenarios in Pakistan's telecom sector. We request Content Library access to compute **cohort-aggregated** discourse statistics comparable to other platforms, with no individual-level profiling or targeting. Research is supervised at `[University]`; IRB reference `[REF]`. Outputs are uncertainty-banded academic forecasts with audit trails.

---

## 4. GDELT

### Status

| Step | Done | Date | Notes |
|------|------|------|-------|
| Choose access path (file export vs. BigQuery) | [ ] | | |
| Create GCP BigQuery account if needed | [ ] | | |
| Document query filters (Pakistan, telecom) | [ ] | | Phase 3 |
| No application required for standard access | [x] | | Open research use |

---

## 5. Survey Data — Gallup Pakistan / PILDAT

### Status

| Step | Done | Date | Notes |
|------|------|------|-------|
| Identify relevant published reports | [ ] | | Topline priors only for MVP |
| Draft academic data-sharing email | [ ] | | Template below |
| Email sent to Gallup Pakistan | [ ] | | |
| Email sent to PILDAT | [ ] | | |
| Data use agreement signed (if microdata) | [ ] | | Optional |

### Email template (adapt before sending)

```
Subject: Academic data request — aggregate public-opinion calibration (telecom sector, Pakistan)

Dear [Organization] team,

I am a graduate student at [University] under the supervision of [Supervisor Name].
We are building a cohort-level research simulator for analyzing public reactions to
corporate PR scenarios in Pakistan's telecommunications sector. The project is
aggregate and non-commercial; we do not profile individuals.

We would like to inquire whether [published tables / de-identified aggregate data /
academic sharing arrangement] are available on topics such as [trust in operators,
service satisfaction, media consumption, or sector reputation], for use as calibration
priors in a Bayesian population model.

We have [submitted / received] university ethics approval [REF] and can provide
our project charter and data handling policy. Any data would be cited per your
requirements, stored securely, and not redistributed.

Thank you for your consideration.

[Name]
[University, Department]
[Email]
```

---

## 6. News Outlets (No API Key — RSS Review)

### Status

| Outlet | RSS / feed URL verified | robots.txt reviewed | Date |
|--------|-------------------------|---------------------|------|
| Dawn | [ ] | [ ] | |
| The Express Tribune | [ ] | [ ] | |
| Third outlet (TBD) | [ ] | [ ] | |

---

## 7. Master Tracker

| Resource | Owner | Priority | Application date | Response date | Status |
|----------|-------|----------|------------------|---------------|--------|
| YouTube API | `[name]` | P1 | | | Not started |
| Reddit API | `[name]` | P2 | | | Not started |
| Meta Content Library | `[name]` | Stretch | | | Not started |
| Gallup Pakistan | `[name]` | Optional | | | Not started |
| PILDAT | `[name]` | Optional | | | Not started |

---

## 8. Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-06-25 | Initial Phase 1 checklist |
