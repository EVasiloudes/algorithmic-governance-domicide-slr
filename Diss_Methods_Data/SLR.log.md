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
