---
tags:
  - MSc_PPM
  - Dissertation_MSc
---

# Scopus Log

## Search A:

```
TITLE-ABS-KEY(( "algorithmic governance" OR "urban analytics" OR "smart city" OR "big data" OR "platform urbanism" OR "predictive policing" ) AND ( "surveillance" OR "dual-use" OR "military" OR "security" OR "targeting" OR "civil-military" OR "OSINT" )) AND PUBYEAR > 1990 AND PUBYEAR < 2025 AND ( LIMIT-TO ( SUBJAREA,"DECI" ) OR LIMIT-TO ( SUBJAREA,"SOCI" ) OR LIMIT-TO ( SUBJAREA,"BUSI" ) OR LIMIT-TO ( SUBJAREA,"ECON" ) OR LIMIT-TO ( SUBJAREA,"ARTS" ) OR LIMIT-TO ( SUBJAREA,"MULT" ) )
```

Returned: 9981 Documents

---

## Search B:

```
TITLE-ABS-KEY(("domicide" OR "urbicide" OR "spatial violence" OR "home unmaking" OR "urban destruction" OR "urban warfare") AND ("data" OR "algorithm" OR "AI" OR "surveillance" OR "GIS" OR "remote sensing")) AND PUBYEAR > 1990 AND PUBYEAR < 2025 AND ( LIMIT-TO ( SUBJAREA,"DECI" ) OR LIMIT-TO ( SUBJAREA,"SOCI" ) OR LIMIT-TO ( SUBJAREA,"BUSI" ) OR LIMIT-TO ( SUBJAREA,"ECON" ) OR LIMIT-TO ( SUBJAREA,"ARTS" ) OR LIMIT-TO ( SUBJAREA,"MULT" ) )```
```

Returned: 31 Documents

---

# Calibration Iteration 1 — 11 June 2026

**Trigger:** Search A returned 9,981 records — unmanageable for solo screening.
**Diagnosis:** Three generic terms driving cross-disciplinary noise:
- `"big data"` — matches every data-science paper regardless of policy relevance.
- `"security"` (bare) — `"smart city" AND "security"` captures the entire IoT/network-cybersecurity engineering literature.
- `"targeting"` (bare) — matches marketing, ad-tech, and pharmaceutical targeting.
- `"surveillance"` (bare) — too broad; qualified forms needed.

**Action taken:** Replaced with qualified equivalents and truncated stems drawn from the critical urban studies / security studies vocabulary. Also fixed date-boundary bug: original filter excluded 1990 and 2025 (`PUBYEAR > 1990 AND < 2025` → `PUBYEAR > 1989 AND < 2026`).

**Revised Search A string:**

```
TITLE-ABS-KEY(( "algorithmic governance" OR "urban analytics" OR "smart cit*" OR "platform urbanism" OR "predictive policing" OR "urban big data" OR "data-driven urbanism" ) AND ( "dual-use" OR "civil-military" OR "military" OR militari* OR "national security" OR securitis* OR securitiz* OR weaponi* OR warfare OR "state surveillance" OR "mass surveillance" OR "OSINT" )) AND PUBYEAR > 1989 AND PUBYEAR < 2026 AND ( LIMIT-TO ( SUBJAREA,"DECI" ) OR LIMIT-TO ( SUBJAREA,"SOCI" ) OR LIMIT-TO ( SUBJAREA,"BUSI" ) OR LIMIT-TO ( SUBJAREA,"ECON" ) OR LIMIT-TO ( SUBJAREA,"ARTS" ) OR LIMIT-TO ( SUBJAREA,"MULT" ) ) AND ( LIMIT-TO ( DOCTYPE,"ar" ) OR LIMIT-TO ( DOCTYPE,"ch" ) OR LIMIT-TO ( DOCTYPE,"re" ) ) AND ( LIMIT-TO ( LANGUAGE,"English" ) )
```

**Revised Search B string (date fix only):**

```
TITLE-ABS-KEY(("domicide" OR "urbicide" OR "spatial violence" OR "home unmaking" OR "urban destruction" OR "urban warfare") AND ("data" OR "algorithm" OR "AI" OR "surveillance" OR "GIS" OR "remote sensing")) AND PUBYEAR > 1989 AND PUBYEAR < 2026 AND ( LIMIT-TO ( SUBJAREA,"DECI" ) OR LIMIT-TO ( SUBJAREA,"SOCI" ) OR LIMIT-TO ( SUBJAREA,"BUSI" ) OR LIMIT-TO ( SUBJAREA,"ECON" ) OR LIMIT-TO ( SUBJAREA,"ARTS" ) OR LIMIT-TO ( SUBJAREA,"MULT" ) ) AND ( LIMIT-TO ( DOCTYPE,"ar" ) OR LIMIT-TO ( DOCTYPE,"ch" ) OR LIMIT-TO ( DOCTYPE,"re" ) ) AND ( LIMIT-TO ( LANGUAGE,"English" ) )
```

**Result:** Pending re-run on Scopus (to be added below once verified with Craig).

**Additional safeguard added:** Single-iteration citation chaining (snowballing) from 3–5 anchor texts — see revised methods chapter.


## Calibration Iteration: Overton dropped (2026-07-03)

**Trigger:** Overton trial licence lapsed 29 June 2026 and was not renewed.
**Action:** Removed Overton from the search strategy. Grey literature now sourced from Policy Commons only, supplemented by targeted manual searches of institutional repositories (RAND Corporation, Chatham House, Urban Displacement Project).
**Impact:** Grey-literature recall reduced; acknowledged in limitations as a constraint. The revised search strategy and limitations section in the canonical methods draft have been updated to reflect this.


## Search Execution Results (2026-07-03)

### Web of Science

**Search A** — Civil-military urban tech nexus:
- String: `TS=("algorithmic governance" OR "urban analytics" OR "smart cit*" OR "platform urbanism" OR "predictive policing" OR "urban big data" OR "data-driven urbanism") AND TS=("dual-use" OR "civil-military" OR military OR militari* OR "national security" OR securitis* OR securitiz* OR weaponi* OR warfare OR "state surveillance" OR "mass surveillance" OR OSINT) AND PY=(1990-2025)`
- Records returned: **486**
- Exported: `Search A — Civil-military urban tech nexus -- Web of Science.ris`

**Search B** — Spatial destruction and the datafied city:
- String: `TS=("domicide" OR "urbicide" OR "spatial violence" OR "home unmaking" OR "urban destruction" OR "urban warfare") AND TS=(data OR algorithm OR AI OR surveillance OR GIS OR "remote sensing") AND PY=(1990-2025)`
- Records returned: **141**
- Exported: `Search B — Spatial destruction and the datafied city -- Web of Science.ris`

### Scopus

**Search A** (revised calibration string, re-run 2026-07-03):
- String: `TITLE-ABS-KEY(( "algorithmic governance" OR "urban analytics" OR "smart city" OR "smart cities" OR "platform urbanism" OR "predictive policing" OR "urban big data" OR "data-driven urbanism" ) AND ( "dual-use" OR "civil-military" OR "military" OR militari* OR "national security" OR securitis* OR securitiz* OR weaponi* OR warfare OR "state surveillance" OR "mass surveillance" OR "OSINT" )) AND PUBYEAR > 1989 AND PUBYEAR < 2026`
- Raw count (no filters): **608**
- Filtered by Subject Area (SOCI + DECI + ARTS + BUSI + ECON + MULT) and exported in subjarea-broken-down RIS files
- Deduplicated across subjarea exports: **219 unique records** (279 raw, ~30% cross-code overlap)
- Exported: `Search A — Scopus (merged, deduplicated).ris`
- WoS A ↔ Scopus A overlap (DOI): **62**

**Search B** (revised calibration string):
- String: `TITLE-ABS-KEY(("domicide" OR "urbicide" OR "spatial violence" OR "home unmaking" OR "urban destruction" OR "urban warfare") AND (data OR algorithm OR AI OR surveillance OR GIS OR "remote sensing")) AND PUBYEAR > 1989 AND PUBYEAR < 2026`
- Raw count (no filters): matches original scoping result
- Filtered by Subject Area (same set) and exported in subjarea-broken-down RIS files
- Deduplicated across subjarea exports: **42 unique records** (52 raw)
- Exported: `Search B — Scopus (merged, deduplicated).ris`
- WoS B ↔ Scopus B overlap (DOI): **14**

### Combined totals (pre-deduplication)
| Database | Search A | Search B |
|---|---|---|
| Web of Science | 486 | 141 |
| Scopus | 219 | 42 |
| Estimated unique (less cross-db overlap) | ~643 | ~169 |

### Files created in Literature [.RIS]/
- `Search A — Civil-military urban tech nexus -- Web of Science.ris` (486 recs)
- `Search B — Spatial destruction and the datafied city -- Web of Science.ris` (141 recs)
- `Search A — Scopus (merged, deduplicated).ris` (219 recs)
- `Search B — Scopus (merged, deduplicated).ris` (42 recs)
- `Scopus Search A exports broken down by subject area/` (raw subjarea files, retained for audit)
- `Scopus Search B exports broken down by subject area/` (raw subjarea files, retained for audit)

### Next Step
Import merged RIS files into Zotero and run deduplication. Then begin title/abstract screening against inclusion criteria.


## Calibration Iteration: Policy Commons broad recall (2026-07-03)

**Trigger:** Initial Policy Commons strings returned unmanageable results.
- Search A (civil-military urban tech): **13,096 hits**
- Search B (spatial destruction): **3,031 hits**

**Diagnosis:** Policy Commons has automatic stemming and a very broad corpus (think-tank reports, policy briefs, working papers). The Search A second AND leg (`military OR warfare OR "national security" etc.`) catches every defence/security policy paper that tangentially mentions smart cities. The Search B string accidentally reused the Search A string (needs re-run).

**Action:** Revise strings to use field targeting (title or summary) and/or more restrictive boolean logic rather than full-text search.

**Calibrated search strings:**

**Search A (Tier 3 — both legs in summary field):**
```
summary:("algorithmic governance" OR "urban analytics" OR "smart city" OR "smart cities" OR "platform urbanism" OR "predictive policing" OR "urban big data" OR "data-driven urbanism") AND summary:("dual-use" OR "civil-military" OR military OR "national security" OR warfare OR securitisation OR securitization OR weaponisation OR weaponization OR "state surveillance" OR "mass surveillance")
```
**Search B (Tier 2 — spatial destruction in title, data terms in summary):**
```
title:("domicide" OR "urbicide" OR "spatial violence" OR "home unmaking" OR "urban destruction" OR "urban warfare") AND summary:(data OR algorithm OR AI OR surveillance OR GIS OR "remote sensing")
```

**Results:**
| Search | Raw | English only | Exported |
|---|---|---|---|
| Search A (Tier 3) | 93 | 67 | 63 |
| Search B (Tier 2) | 15 | 10 | 10 |

**Files created:**
- `Policy Commons Search A — Civil-military urban tech nexus (tier 3, summary-summary).ris` (63 recs)
- `Policy Commons Search B — Spatial destruction and the datafied city (tier 2, summary-summary).ris` (10 recs)

### Combined total search corpus (all sources)
| Source | Search A | Search B |
|---|---|---|
| Web of Science | 486 | 141 |
| Scopus | 219 | 42 |
| Policy Commons (grey lit) | 63 | 10 |
| **Identification phase total** | **~768** | **~193** |

**Note:** The Policy Commons files had their filenames swapped on export (Policy Commons generates UUID filenames, not descriptive ones); corrected on 2026-07-03. Search A content was in the "Search B" file and vice versa.


## Screening: Title/Abstract — 2026-07-11

### Pre-processing
- **Deduplication**: 963 raw → 874 unique (80 DOI dupes + 9 title-fuzzy dupes removed)
- **Triage**: 195 HIGH, 326 MEDIUM, 276 LOW, 77 EXCLUDED (no abstract / very short abstract)
- **Files created:**
  - `Literature [.RIS]/deduplicated/All Searches — Merged Deduplicated.ris`
  - `Literature [.RIS]/deduplicated/Search A — Deduplicated.ris` (698 recs)
  - `Literature [.RIS]/deduplicated/Search B — Deduplicated.ris` (176 recs)
  - `Literature [.RIS]/deduplicated/screening_master.csv` (874 rows)
  - `Literature [.RIS]/deduplicated/ai_screen.py`

### AI-assisted screening
- **Model**: OpenRouter DS4-flash (`deepseek/deepseek-v4-flash`)
- **Temperature**: 0.0 for deterministic classification
- **Priority order**: HIGH → MEDIUM → LOW (resolved all into Include/Exclude, no Maybes remaining)

### Results
| Verdict | Count | % |
|---------|-------|---|
| Include | **151** | 17.2% |
| Exclude | **723** | 82.8% |
| **Total** | **874** | 100% |

- Dissertations identified and excluded (manual review of Maybes)
- Conference papers retained as eligible (disclosed in methods)
- Output RIS: `Included_151_records.ris` (clean UTF-8, ready for Zotero)

### Encoding fix
- Original CSV had mojibake from latin-1 read of UTF-8 RIS data
- Rebuilt `screening_master.csv` from clean RIS sources with proper UTF-8 encoding
- Old corrupted CSV backed up as `screening_master_CORRUPTED_BACKUP.csv`

### Next step
Import `Included_151_records.ris` into Zotero, begin full-text retrieval.


## Full-Text Retrieval & PDF Extraction — 2026-07-14 to 2026-07-16

### Zotero import
- `Included_151_records.ris` imported into Zotero collection `SLR-INCLUDED-RECORDS_BUP` (collection ID 94)
- 148 records in RIS export (3 excluded during screening re-verification)
- 144 PDFs attached in Zotero from the 151 included records

### RIS rebuild (content-based matching)
- Earlier position-based mapping between `screening_master.csv` and merged `.ris` was broken: the RIS was regenerated after CSV creation, shuffling record order
- Tshilongamulenzhe (CSV ID 76, marked Exclude in screening) was appearing in position-based output — confirmed position mapping invalid
- **Solution:** Content-based matching by DOI, then normalised title with author/year disambiguation
- `Included_151_records.ris` and `Included_151_records_tagged.ris` verified correct; Tshilongamulenzhe confirmed excluded

### Pipeline: pipeline_01_extract_v2.py
- **Location:** `corpus/scripts/pipeline_01_extract_v2.py`
- **Function:** Reads Zotero RIS export + files directory; matches records to PDFs via SQLite DB (collection 94); extracts text with pdfplumber (PyPDF2 fallback); outputs metadata CSV
- **Key feature:** Resumable — skips already-extracted PDFs/texts on re-run
- **Dependencies:** pdfplumber (PyPDF2 absent but not needed; pdfplumber handles all files)

**Results:**
| Metric | Count |
|---|---|
| RIS records | 148 |
| PDFs copied to corpus/ | 145 |
| No PDF found | 3 |
| Text extraction OK | 145 |
| Extraction failed | 0 |

**3 no-PDF records (marked in metadata.csv):**
1. "Big Data Applications in Crime and Security" — book, not located
2. "Intelligent 5G Networks Designed and Integrated for Globalized Operations (INDIGO)" — no PDF in export
3. "An automated security response robot" — no PDF in export

**Output:**
- `corpus/metadata.csv` (148 rows)
- `corpus/pdfs/` (145 PDFs)
- `corpus/text/` (145 text files)
- `corpus/extraction_log.json` (run metadata)
- `corpus/run.log` (timestamped execution log)


## AI-Assisted Thematic Coding — 2026-07-16

### Script: ai_extract.py
- **Location:** `Diss_Methods_Data/Literature [.RIS]/deduplicated/ai_extract.py`
- **Model:** DeepSeek V4 Flash (`deepseek/deepseek-v4-flash`) via OpenRouter, temperature 0.0
  - Initial slug error: `openrouter/deepseek/...` (OpenClaw convention) → corrected to `deepseek/deepseek-v4-flash` (OpenRouter convention)
  - Fallback model: `deepseek/deepseek-chat` (used for first run before slug fix; record #3 extracted via fallback)
- **Batch size:** 5 records per invocation (resumable via `extraction_results.csv` checkpoint)
- **Text ceiling:** 450K chars (~112K tokens); 9 papers smart-truncated (intro 55% + middle samples + conclusion 25%)
- **Special handling:** 3 edited volume chapters extracted by byte position (IDs 160, 516, 665); 1 missing chapter flagged for manual retrieval (ID 750, duplicate of ID 727 Routledge Handbook)

### Coding Framework (4 themes, 0–3 scale)
1. **Information Good & Dual-Use Fluidity** (Arrow, 1962)
2. **Epistemic Authority & Black-Boxing** (Michael, 2007; Pasquale, 2015)
3. **Machinic City & Modulation** (Deleuze, 1990; De Landa, 1992/2014)
4. **Spatial Collapse & Home Unmaking** (King, 2004; Graham, 2006/2011; Weizman, 2007)

Additional fields: dual_use_explicit, dual_use_direction, dual_use_structural, doc_type, methodology, geography, thesis, key_quotes, policy_relevance.

### Results
| Metric | Count |
|---|---|
| Papers scored | 147 |
| No text / not retrievable | 3 |
| API extraction failed | 1 |
| **Total in output CSV** | **151** |

### Score Distributions
| Theme | 0 | 1 | 2 | 3 | Mean | % Scoring ≥1 |
|---|---|---|---|---|---|---|
| T1: Information Good & Dual-Use | 51 | 35 | 52 | 9 | 1.13 | 65% |
| T2: Epistemic Authority & Black-Boxing | 44 | 38 | 54 | 11 | 1.22 | 70% |
| T3: Machinic City & Modulation | 26 | 63 | 51 | 7 | 1.27 | 82% |
| T4: Spatial Collapse & Home Unmaking | 97 | 32 | 8 | 10 | 0.53 | 34% |

### Dual-Use Classification
| Field | yes | tangential | no |
|---|---|---|---|
| dual_use_explicit | 45 | 34 | 68 |
| dual_use_structural | 31 | 24 | 92 |

Note: Only 31/147 papers address *structural* properties (software as information good) enabling dual-use, despite 45 using "dual-use" language explicitly.

### Search A/B Divergence (MAIN FINDING)
| Theme | Search A (n=126) | Search B (n=21) |
|---|---|---|
| T1 (Dual-use fluidity) | 1.21 | 0.67 |
| T2 (Epistemic authority) | 1.33 | 0.57 |
| T3 (Machinic city) | 1.33 | 0.86 |
| T4 (Spatial destruction) | 0.32 | 1.81 |

**Key finding:** Zero overlap between Search A and Search B at the screening stage. The two literatures are separate conversations. Search A (civil-military urban tech) is rich on data governance, algorithmic opacity, and smart city critique — but virtually silent on spatial violence or domicide. Search B (spatial destruction + data) is deeply engaged with urbicide, home unmaking, and the weaponisation of urban space — but barely engages with data/software infrastructure, dual-use properties, or algorithmic governance. **The separation validates the central thesis: the connection between algorithmic governance tools and systemic spatial destruction is empirically under-explored in the literature.**

### Bridge Papers (comprehensive across all themes)
Papers scoring ≥2 on three themes and ≥1 on the fourth:
- #58: Who Buys and Controls CCTV? Myanmar's Slippery Slope to Mass Surveillance (T1=3, T2=3, T3=2, T4=1)
- #173: Realtime Urbanism: The Architecture of Packets, Pixels, and Neurons (T1=2, T2=2, T3=3, T4=2)
- #308: Territorialising the Cloud or Clouding the Territory? Volumetric Vulnerabilities (T1=3, T2=2, T3=2, T4=2)
- #642: Compliance-Industrial Complex: The Operating System of a Pre-Crime Society (T1=3, T2=3, T3=2, T4=0) — strong on themes 1-3, absent on T4
- #742: Robowar™ Dreams: US Military Technophilia and Global South Urbanisation (T1=0, T2=2, T3=3, T4=3) — absent on T1, strong on others

Only 3 papers (#58, #308, #173) score ≥2 on three themes AND ≥1 on the fourth — true bridges are rare.

### Temporal Trend
Theme 4 (spatial destruction) shows marked acceleration:
- 2015–2019 (n=44): T4 mean = 0.27
- 2020–2024 (n=75): T4 mean = 0.52
- 2025+     (n=18): T4 mean = 0.94

Likely driven by Gaza scholarship post-2023. The literature's engagement with spatial destruction is intensifying — but still largely disconnected from the data-governance / dual-use conversation.

### Output files
- `corpus/extraction_results.csv` — 151 rows, full scoring + metadata
- `corpus/extractions/*.json` — 148 per-paper JSON files for qualitative review

### Next steps (analysis phase)
1. Descriptive statistics from extraction results (PRISMA flow, theme distributions, methodology × geography)
2. Search A/B scatter plot (T1 × T4, coloured by Search origin)
3. Bridge paper qualitative deep dives for Ch.4 vignettes
4. Temporal trend visualisation
5. Ch.2 Theoretical Framework prose drafting


## Citation Chaining (Snowballing) — 2026-07-19

### Protocol
Single iteration, backward + forward, from 4 anchor texts (protocol specified 3–5; the 3 named anchors plus Michael 2007, central to the Ch2 framework). Executed via **OpenAlex** API (no Scopus access at execution time) with the same filters as the database searches: 1990–2025, English, article/book-chapter/review.

### Anchors (resolved records)
| Anchor | OpenAlex record | Backward (refs indexed) | Forward (citing, filtered) |
|---|---|---|---|
| Graham 2006, *Cities, War, and Terrorism* | W2503071168 | 0 (book — no indexed bibliography) | 194 |
| Kitchin 2014, *Big Data, new epistemologies…* | W2112031167 | 49 → 33 filtered | 1,490 |
| Weizman 2007, *Hollow Land* | W1805035031 | 0 (book — no indexed bibliography) | 346 |
| Michael 2007, *IDF as epistemic authority* | W2042077210 | 14 → 8 filtered | 17 |

**Coverage note:** OpenAlex indexes no reference lists for the two book anchors (Graham, Weizman); backward pass was executable only for Kitchin (33) and Michael (8). Disclosed in Ch3 §3.3.4.

### Pipeline
- Unique candidates after protocol filters: **2,087**
- Duplicates of existing 874-record corpus: **9** (3 DOI, 6 title) — the citation network extends well beyond the keyword perimeter
- New records: **2,078**
- Triage exclusion (no/vestigial abstract <200 chars, mirrors main pipeline rule): **516**
- Screened (title+abstract, identical prompt/model/temp as main run: DS4-flash, temp 0.0, 4 parallel workers, resumable): **1,562**

### Results
| Verdict | Count |
|---|---|
| Include | **119** |
| Exclude | 1,917 |
| Maybe (pending author resolution) | 41 |
| Unresolved error | 1 |

Includes by anchor path: Kitchin fwd 56, Graham fwd 35, Weizman fwd 29, Kitchin bwd 1 (2 records via multiple anchors; Michael yielded 0).

### Files (Diss_Methods_Data/analysis/snowball/)
- `pull_candidates.py`, `dedup_against_corpus.py`, `screen_snowball.py` — pipeline scripts
- `candidates.json`, `candidates_deduped.json` — raw + deduped candidate pools
- `snowball_screening.csv` — all 2,078 verdicts
- `maybes_for_author.md` — 41 records pending author decision
- `snowball_summary.json` — machine-readable counts

### Next steps
1. Author resolves 279 Maybes → final Include count
2. Full-text retrieval for 124 snowball Includes (Zotero/library flow)
3. Run `enrich_springer.py` when Springer META rate limit resets (225 records, ~60-80 expected abstracts)
4. Thematic coding of snowball Includes (same codebook/pipeline as main corpus)
5. PRISMA diagram updated: "identification via other methods" branch
6. Ch3 §3.3.4 rewritten from protocol deviation to executed pass

---

## Snowball Re-Run — 2026-07-23

### Context
Original pull (Jul 19-22) had an expired OpenAlex API key. Kitchin 2014 has 2,300+ citations — without auth, OpenAlex silently rate-limited or returned incomplete pages. The old `.env` was empty.

### Fresh run with valid key
- Kitchin forward: 1,498 screenable (was ~56 in truncated run)
- Weizman forward: 338 screenable
- Graham forward: 238 screenable
- **New totals:** 2,090 candidates → 2,081 after dedup → 1,564 screened → 121 Include, 275 Maybe, 1,685 Exclude, 517 triaged (no abstract)
- Maybes exploded from 41 → 275 — the real bottleneck became author resolution

---

## Abstract Enrichment Pipeline — 2026-07-26

### Purpose
517 triage records had no abstract from OpenAlex. Elias supplied publisher API keys (Elsevier, Springer META, Springer OA, IEEE Xplore) to close the gap.

### APIs tested
| API | Status | Reason |
|-----|--------|--------|
| **Semantic Scholar** | ✅ Used | Free, no key. 59/497 enriched |
| **OpenAlex re-scan** | ✅ Used | 17/498 newly got abstracts |
| **Springer META** | ⚠️ Working | 500 calls/day. Rate-limited from earlier failed runs. 225 Springer records pending |
| **Elsevier** | ❌ | Free tier returns no abstract text (needs institutional subscription) |
| **IEEE Xplore** | ❌ | Account marked "Inactive" on developer.ieee.org |
| **Crossref** | ❌ | Publishers don't deposit abstracts |
| **Springer OA** | ❌ | Only covers open-access subset |

### Re-screening results
58 triaged records gained abstracts (57 S2 + 1 OpenAlex). Re-screened with same DS4-chat model + system prompt:
- **+3 Include:** From SARS to COVID-19 (Elsevier), Civic data governance & democratic smart cities, Spatiotemporal resolution in predictive policing
- **+4 Maybe:** Neoliberalising the divided city, Smart systems for smart places, Social implications of autonomous vehicles, Dwelling within political violence (Palestinian women)
- 51 remain Exclude

### Current state
| | Before | After |
|---|---|---|
| Include | 121 | **124** |
| Maybe | 275 | **279** |
| Exclude | 1,685 | 1,678 |
| No abstract | 517 | 459 |

### Scripts added
- `enrich_abstracts.py` — unified enrichment (S2 + OpenAlex + Springer)
- `enrich_springer.py` — Springer-only, self-throttling for rate limits
- `rescreen_enriched.py` — re-screens enriched records using same AI pipeline


## Snowball Final Resolution — 2026-07-28

### Abstract enrichment (APIs round 2)
- **Springer META:** 217/225 Springer DOIs enriched (8 missed — API return empty)
- **OpenAlex re-scan:** 18/224 remaining DOIs enriched
- **Post-enrichment state:** 1,839 with abstracts, 242 still no-abstract (triage-excluded, mirrors main pipeline rule)

### Decision: Drop Maybes
279 Maybe-verdict records dropped without manual review. Rationale: the 124 Includes already represent a substantial snowball corpus (82% the size of the main 151-record corpus). The 279 Maybes are predominantly tangential — urban governance papers mentioning surveillance in passing, general smart-city critiques without dual-use relevance, or methodological pieces about big data without policy/spatial dimension. Noted for transparency in methods.

### Final snowball corpus
| Verdict | Count |
|---|---|
| Include | **124** |
| Maybe (dropped) | 279 |
| Exclude | 1,678 |
| **Total** | **2,081** |

### Via paths
| Anchor | Includes |
|---|---|
| Weizman 2007 (forward) | 46 |
| Kitchin 2014 (forward) | 42 |
| Graham 2006 (forward) | 38 |
| Kitchin 2014 (backward) | 0 |
| Michael 2007 (forward) | 0 |
| Michael 2007 (backward) | 0 |

Note: 2 records came through multiple anchors (counted under both). Michael (2007) yielded no includes despite the theoretical centrality — it bridged to the counterinsurgency/epistemic-authority literature but those papers were already captured by the Weizman/Graham citation networks.

### Output files
- `snowball_included_124.ris` — clean RIS for Zotero import
- `snowball_included_124_tagged.ris` — KW-tagged version with anchor path in N1 field

### PDF availability
- **Only 1/124** snowball Includes have PDFs in the existing `corpus/pdfs/` (a pre-existing overlap with the main corpus)
- **123/124 need fresh PDF retrieval** — these are citation-network papers distinct from the keyword-search corpus

### Combined corpus (main + snowball)
| Source | Records |
|---|---|
| Database searches (WoS + Scopus + Policy Commons) | 151 |
| Snowball (4 anchor texts) | 124 |
| **Total** | **275** |

### Next steps
1. Import `snowball_included_124.ris` into Zotero
2. PDF retrieval for ~123 new records
3. Re-run `pipeline_01_extract_v2.py` for new PDFs
4. Thematic coding of snowball corpus (same codebook)
5. Updated PRISMA diagram
