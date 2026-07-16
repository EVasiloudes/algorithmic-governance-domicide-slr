---
tags:
  - MSc_PPM
  - Dissertation_MSc
---

# Writing Plan v1 — Agentic Task Decomposition

**Created:** 11 June 2026 · **Updated:** 16 July 2026
**Status:** Active — Extraction + thematic coding COMPLETE (147/151 papers scored). Next: Analysis + Ch2 drafting.
**Hard constraint:** 13,750 words max, 100% of grade. Submission deadline: **13 August 2026** (confirmed).

---

## 1. Target structure & word budget

| Ch. | Title | Words | Source material | Status |
|---|---|---|---|---|
| 1 | Introduction: The Algorithm and the City | 1,500 | Revised formative (cut ~40%, add bridge ¶ + provisional policy landing zone) | Drafted, needs trim |
| 2 | Theoretical Framework | 2,500 | Arrow · Deleuze/De Landa · Michael · King/Graham/Weizman — organised around **one primary axis: disciplinary → control** | Outline complete; prose drafting next |
| 3 | Methodology | 2,500 | Revised formative methods + completed PRISMA ns + calibration narrative from `SLR.log.md` | Drafted, needs tense shift to past + real ns |
| 4 | Findings: The Systematic Map | 3,500 | Extraction results: 147 scored papers across 4-theme framework; Search A/B divergence analysis; temporal trends; bridge papers | Extraction complete; analysis pending |
| 5 | Discussion | 2,250 | Findings × framework; the A/B convergence-gap finding; critical gap analysis; policy implications | Not started |
| 6 | Conclusion & Research Agenda | 1,250 | Discussion + limitations | Not started |
| — | Front/back matter, AI statement | 250 | — | Template exists |
| | **Total** | **13,750** | | |

**Structural decisions (confirmed):** the SLR *is* the data; Chapter 2 is a *theoretical framework*, not a conventional literature review — avoids duplicating Chapter 4. Screening tooling: Zotero only (Rayyan dropped). LaTeX `final-draft/` directory created at repo root as the submission pipeline.

---

## 2. Phase plan (week-by-week)
```mermaid
gantt
    dateFormat YYYY-MM-DD
    axisFormat %d %b
    section Pipeline
    Finalise strings + WoS scoping      :p1, 2026-06-12, 7d
    Execute searches + dedupe (Zotero)  :p2, after p1, 7d
    Snowballing (1 iteration)           :p3, after p1, 10d
    Full screening                     :p5, after p2, 14d
    Extraction + coding                 :p6, after p5, 12d
    section Writing
    Coding manual (1 page)              :w0, 2026-06-22, 5d
    Ch2 Theoretical Framework           :w1, 2026-06-26, 14d
    Ch4 Findings                        :w2, after p6, 10d
    Ch5 Discussion                      :w3, after w2, 7d
    Ch1+Ch3 revision, Ch6               :w4, after w3, 7d
    Polish, refs, proofread, submit     :w5, after w4, 7d
```

**Current position (16 Jul):** p6 (extraction + coding) COMPLETE. Analysis + Ch2 drafting begin in parallel.

**Revised timeline to deadline (13 Aug = 28 days):**

| Phase | Task | Days | Dates |
|---|---|---|---|
| 1 | Full-text retrieval + Zotero import | ✓ | 12–16 Jul |
| 2 | Snowballing from anchors | 5 | 12–16 Jul |
| 3 | Extraction + thematic coding (151 papers) | ✓ | 15–16 Jul |
| 4 | Analysis: descriptive stats, visualisations, bridge paper deep dives | 5 | 17–21 Jul |
| 5 | Ch2 Theoretical Framework writing | 7 | 17–23 Jul |
| 6 | Ch4 Findings (descriptive stats + synthesis) | 8 | 22–29 Jul |
| 7 | Ch5 Discussion + Ch6 Conclusion | 7 | 30 Jul – 5 Aug |
| 8 | Ch1+Ch3 revision, references, AI statement | 4 | 6–9 Aug |
| 9 | Polish, proofread, submit | 4 | 10–13 Aug |

**Contingency:** if full-text retrieval reveals >~80 papers with retrievable full text, narrow extraction scope (date-weighted sampling or tightened relevance). Finalise rule with Craig before extraction begins.

---

## 3. Agentic task decomposition

### Author-only (substantive intellectual work — never delegated)
- All screening include/exclude decisions ✓ (done)
- All coding judgements
- The argument: thesis, interpretation of findings, discussion claims
- Final wording of every paragraph (agent drafts are raw material)
- Supervision meetings and decisions arising

### Agent-delegable (with author review)
| Task | When | Notes |
|---|---|---|
| Citation verification sweep | Continuous; final pass wk of submission | Flag `[VERIFY]` items |
| Reference list formatting & deduplication | Phase p2; final week | Match existing author-date style |
| PRISMA diagram updates from real ns | After p5, p6 | Mermaid, theme-neutral |
| `SLR.log.md` iteration entries | Each calibration | Append-only; author confirms counts |
| Consistency passes (British English, terminology, tense) | After each chapter draft | esp. Ch3 future→past tense shift |
| Word-budget tracking per chapter | Weekly | Report drift > 10% |
| Extraction spreadsheet scaffolding | p6 | Columns: year, discipline, geography, doc type, codes |
| Descriptive statistics + charts from extraction | w2 | Counts by theme × year for longitudinal claim |
| Draft-zero prose for mechanical sections (e.g., PRISMA narration) | w2, w4 | Flagged for authorial rewrite per AI statement |
| Meeting agendas + email drafts | As needed | Established pattern |

### Standing agent workflows
1. **Pre-edit protocol:** re-read target file immediately before editing (Obsidian churn); fall back to scripted replace.
2. **Checkpoint commits** at each phase boundary with descriptive messages.
3. **Never touch:** frozen formative; `SLR.log.md` history.

---

## 4. Open questions (carry to next supervision)

1. Corpus-size contingency rule — if >80 papers with retrievable full text, agree narrowing mechanism. (Needed *before* extraction.)
2. Should we schedule one more supervision slot before submission?

---

## 5. Immediate tasks (12 Jul – 14 Jul)

| Priority | Task | Who | Notes |
|---|---|---|---|
| **High** | Begin analysis: descriptive stats, Search A/B divergence, temporal trends | Agent | Extraction data ready in `corpus/extraction_results.csv` |
| **High** | Qualitative deep dives: 5-8 bridge papers for Ch.4 vignettes | Agent | Use `corpus/extractions/*.json` key_quotes |
| **Medium** | Build visualisations: scatter plot (T1×T4), PRISMA flow, theme distribution | Agent | Matplotlib + Mermaid |
| **Medium** | Draft Ch2 prose (theoretical framework) | Author + Agent | Outline exists at `projects/dissertation/ch2-outline.md` |
| **High** | Run snowballing from anchor texts (Graham 2006, Kitchin 2014, Weizman 2007) | Author + Agent | Agent can format candidate lists from reference PDFs |
| **Low** | Write AI-use statement draft from AGENTS.md conventions | Agent | Place in `final-draft/dissertation.tex` appendix A |

## 6. Completed milestones

- [x] Search strings finalised + calibrated (Iteration 1, 11 Jun)
- [x] WoS + Scopus searches executed (3 Jul)
- [x] Policy Commons grey literature search executed (3 Jul)
- [x] All RIS files deduplicated (874 unique records)
- [x] AI-assisted title/abstract screening (DS4-flash, temp 0.0) — 151 Include
- [x] `Included_151_records.ris` and tagged variant verified correct
- [x] Full-text retrieval: 145/148 PDFs located and extracted (pipeline_01_extract_v2)
- [x] AI-assisted thematic coding (DS4-flash, temp 0.0) — 147/151 papers scored across 4 themes
- [x] SLR.log.md captures full calibration + execution history

## 7. Version history

- **v1.3 (16 Jul 2026):** Full-text retrieval + extraction + thematic coding complete. 147/151 papers scored. Initial analysis: A/B divergence confirmed, bridge papers identified, analysis modalities recommended. Phase plan updated to reflect 28-day runway.
- **v1.2 (12 Jul 2026):** Screening complete milestone added. Revised phase plan + immediate tasks for 12–14 Jul. Contingency rule added. Completed milestones section. Gordon-clarke.
- **v1.1 (30 Jun 2026):** Rayyan/pilot-screen removed, `final-draft/` LaTeX directory created.
- **v1 (11 Jun 2026):** Initial decomposition. Pending supervision review.
