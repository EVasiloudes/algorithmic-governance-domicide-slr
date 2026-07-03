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