---
tags:
  - MSc_PPM
  - Dissertation_MSc
---

# Appendix A — AI-Assisted Research Methods

**Status:** Draft · **Date:** 28 July 2026 · **Note:** This appendix does not count toward the word limit.

---

## A.1 Overview

This dissertation used artificial intelligence at four stages: screening, citation-chaining, full-text extraction, and thematic coding. AI was used for mechanical, well-defined tasks at scale and, under close direction, for drafting assistance; every agent-drafted passage was reviewed and substantially rewritten by the author, and all screening verdicts, coding judgements, analytical claims, and the final text are the author's responsibility (see the AI-Use Statement in the dissertation). The AI pipeline was designed to be deterministic (temperature 0.0), resumable, and auditable — every run was logged with timestamps, and all intermediate outputs (screening CSVs, extraction JSONs, metadata tables) are retained in the project repository.

This appendix discloses the tools, configurations, and decisions involved, in accordance with the University of Glasgow's guidance on AI in research and the emerging norms of transparent AI use in systematic reviewing (e.g. PRISMA-AI reporting extensions).

---

## A.2 Research Environment

The project was conducted on a personal machine (macOS 13.7, x64) running a persistent AI assistant — **OpenClaw** (v2026.7.1) — configured with the model `deepseek/deepseek-v4-flash` via the OpenRouter API gateway (interactive sessions additionally used other frontier models, e.g. Moonshot AI's Kimi K3, for drafting and verification support). OpenClaw functioned as an orchestration layer: it read project files, executed Python pipelines, called external APIs, and wrote outputs back to the filesystem. The author reviewed all AI outputs before accepting them into the analysis.

Writing and note-taking were done in **Obsidian** (v1.x) with community plugins. The most methodologically significant was **Smart Connections** (v5.0.0, Brian Petro), which generates local embeddings from the Obsidian vault and surfaces semantically related notes. Smart Connections was used during the drafting and revision process to locate relevant references, link related concepts across chapters, and audit citation coverage. It operates entirely locally — no vault content is sent to external servers — using the `bge-micro-v2` embedding model, which runs on-device.

Reference management was handled by **Zotero** (v7.x), with PDFs stored locally and indexed by the pipeline scripts described below.

---

## A.3 Pipeline Architecture

The pipeline comprised five Python scripts and a SQLite bridge to Zotero's internal database. All scripts are archived in `Diss_Methods_Data/` with full source code.

### A.3.1 AI screening — `ai_screen.py` + `screen_snowball.py`

**Purpose:** Classify records against the inclusion/exclusion criteria (§3.4.2).

**Model:** DeepSeek V4 Flash (`deepseek/deepseek-v4-flash`) via OpenRouter. Fallback: DeepSeek V4 Chat (`deepseek/deepseek-chat`). Temperature 0.0; `max_tokens` 256; `top_p` 1.0.

**Prompt:** A single system prompt containing the full inclusion and exclusion criteria, with instructions to respond with exactly one word: "Include", "Exclude", or "Maybe". The prompt is archived at `analysis/snowball/screening_prompt.txt` and embedded in `Literature [.RIS]/deduplicated/ai_screen.py`. The snowball screener used the identical prompt, model, and parameters.

**Workflow:** Records were processed in priority bands (HIGH → MEDIUM → LOW). The main pipeline ran sequentially; the snowball screener used four parallel threads for throughput. Both were resumable — records with existing verdicts were skipped on re-run. Borderline cases ("Maybe") were logged and resolved by the author against the written criteria, not by further AI calls.

### A.3.2 Abstract enrichment — `enrich_springer.py` + `enrich_abstracts.py`

**Purpose:** Recover missing abstracts for records excluded at triage for having no abstract or a vestigial abstract (<200 characters).

**APIs used:**
- **Springer META API** (Springer Nature) — primary source for Springer Nature DOIs (prefix `10.1007/`). Self-throttling (1.2 s delay between calls, ~50 calls/minute) to respect rate limits. 217 of 225 Springer DOIs recovered.
- **OpenAlex API** — re-scan of all remaining DOIs for abstracts not indexed in the original OpenAlex pull. 18 of 224 recovered.
- **Semantic Scholar API** — earlier pass (July 26) recovered 59 of 497 missing abstracts.

**Note on failed APIs:** Elsevier's free API tier returns no abstract text without an institutional subscription. IEEE Xplore developer access was inactive. Crossref does not deposit abstracts for most publishers. These were evaluated and set aside.

### A.3.3 PDF extraction — `pipeline_01_extract_v2.py`

**Purpose:** Copy PDFs from Zotero storage to a local corpus directory, extract full text, and build a metadata table.

**Process:**
1. Reads a Zotero RIS export and the Zotero SQLite database directly (`zotero.sqlite`) to map each RIS record to its PDF attachment by title match.
2. Copies matched PDFs to `corpus/pdfs/` and extracts text using `pdfplumber` (primary) with `PyPDF2` as fallback.
3. Writes extracted text to `corpus/text/` and metadata (title, authors, year, DOI, type, PDF filename, extraction status) to `corpus/metadata.csv`.
4. Logs every run to `corpus/extraction_log.json` and `corpus/run.log`.

The script is resumable — already-extracted files are skipped on re-run.

### A.3.4 Thematic coding — `ai_extract.py`

**Purpose:** Score each paper against the four-theme coding framework (§3.5) on a 0–3 scale.

**Model:** Same as screening (DeepSeek V4 Flash, temperature 0.0, `max_tokens` 4096).

**Batching:** Papers processed in batches of 5 per API call (resumable via `corpus/extraction_results.csv` checkpoint). Long texts (>450K characters) were smart-truncated: 55% from the introduction, 25% from the conclusion, with middle sections sampled proportionally. 9 of 147 papers were truncated under this rule.

**Output:** Each paper produced a structured JSON file (`corpus/extractions/*.json`) containing: theme scores, dual-use classification (explicit/direction/structural), document type, methodology, geography, thesis summary, key quotes, policy relevance, and notes. The JSON files were retained for qualitative review and audit.

### A.3.5 Citation chaining — `pull_candidates.py` + `dedup_against_corpus.py`

**Purpose:** Execute backward and forward citation chaining from four anchor texts via the OpenAlex API.

**Process:**
1. Resolved each anchor to its OpenAlex work ID.
2. Pulled all backward references (where indexed) and forward citations, filtered by year (1990–2025), language (English), and document type (article, book chapter, review).
3. Deduplicated against the existing 874-record corpus by DOI, then by fuzzy title matching.
4. Output: `analysis/snowball/candidates.json` → `candidates_deduped.json` → `candidates_enriched.json`.

---

## A.4 Model Parameters and Determinism

| Parameter | Value | Rationale |
|---|---|---|
| Model (primary) | `deepseek/deepseek-v4-flash` | Fast, cost-effective, sufficient for classification tasks |
| Model (fallback) | `deepseek/deepseek-chat` | Used when primary unavailable (404) |
| Temperature | 0.0 | Deterministic output — same input always produces same verdict |
| `max_tokens` (screening) | 256 | Sufficient for single-word verdict |
| `max_tokens` (extraction) | 4096 | Accommodates full JSON output for 4-theme coding |
| `top_p` | 1.0 | No nucleus sampling — deterministic at temperature 0 |
| Batch size (screening) | 1 record per call | Ensures independence of verdicts |
| Batch size (extraction) | 5 records per call | Balances throughput and rate limits |
| Workers (snowball) | 4 parallel threads | 2,081 records — sequential would take ~10 h |
| Rate limit (screening) | 0.3 s delay (~3 req/s) | Polite to OpenRouter free tier |
| Rate limit (Springer) | 1.2 s delay (~50 req/min) | Under Springer META 500/day quota |

---

## A.5 APIs and Data Sources

| API | Purpose | Access tier |
|---|---|---|
| **OpenAlex** | Citation chaining, abstract re-scan | Free, polite pool (mailto) |
| **Springer META** | Abstract enrichment for Springer DOIs | API key (500 calls/day) |
| **Semantic Scholar** | Abstract enrichment (early pass) | Free, no key |
| **Unpaywall** | OA status checking for PDF retrieval | Free |
| **OpenRouter** | LLM gateway for DeepSeek models | API key (pay-as-you-go) |

**Note on Overton:** The formative protocol specified Overton for grey-literature discovery. The University of Glasgow trial licence lapsed on 29 June 2026 and was not renewed. Grey literature was instead sourced from Policy Commons and targeted manual searches of institutional repositories (RAND, Chatham House, Urban Displacement Project). This is disclosed in §3.3.1 and §3.6.

**Note on Elsevier API:** Evaluated for abstract enrichment; the free tier returns metadata but no abstract text without an institutional subscription. Set aside.

**Note on IEEE Xplore API:** Developer account marked "Inactive" on developer.ieee.org. Could not be activated in time. Set aside.

---

## A.6 Local Embedding and Semantic Search

Beyond the pipeline scripts, the author used **Smart Connections** (v5.0.0) in Obsidian for local semantic search across the project vault. Smart Connections generates vector embeddings from note content using the locally running `bge-micro-v2` model, stored locally in the vault's `.smart-env/` directory. The author used this during drafting to:

- Locate relevant references when the exact title was not recalled
- Surface thematically related notes across chapter drafts
- Audit citation coverage against the coding framework

No vault content is sent to external servers: the embedding model runs on-device. Smart Connections is open-source (GPL-3.0) and the embedding model is specified in the plugin's `manifest.json`.

---

## A.7 Human Oversight and Responsibility

AI was used to execute well-defined, mechanical tasks at scale: classifying records against written criteria, extracting text from PDFs, and scoring papers against a structured codebook. All of the following were performed by the author alone:

- Formulating the research questions and search strategy
- Calibrating search strings through scoping iterations
- Writing the inclusion/exclusion criteria and coding framework
- Resolving all "Maybe" screening verdicts
- Reviewing random samples of AI screening verdicts and coding scores for calibration (§3.6)
- Identifying and excluding doctoral dissertations
- Selecting bridge papers for qualitative deep dives
- Interpreting the results and writing the analysis
- Reviewing, revising, and substantially rewriting all agent-drafted text before inclusion

The AI did not participate in any interpretive, analytical, or creative decision. Its role was strictly instrumental — performing at scale what would otherwise have required an impractical amount of manual labour for a single-author project.

---

## A.8 Reproducibility

All scripts, prompts, configuration files, intermediate outputs, and logs are retained in the project repository at:

```
Diss_Methods_Data/
├── Literature [.RIS]/deduplicated/     # ai_screen.py, ai_extract.py, .env
├── analysis/snowball/                   # pull_candidates.py, dedup_against_corpus.py,
│                                        # enrich_springer.py, enrich_abstracts.py,
│                                        # screen_snowball.py, screening_prompt.txt,
│                                        # candidates*.json, snowball_screening.csv,
│                                        # snowball_included_124.ris, retrieval/
└── corpus/                              # pipeline_01_extract_v2.py, metadata.csv,
                                         # extraction_log.json, run.log,
                                         # pdfs/, text/, extractions/
```

The SLR log (`SLR.log.md`) records every run with timestamps, counts, and errors. The project vault (Obsidian) is backed up and version-controlled.

---

## A.9 Software Versions

| Software | Version | Role |
|---|---|---|
| OpenClaw | 2026.7.1-2 | AI orchestration layer |
| OpenRouter API | — | LLM gateway |
| DeepSeek V4 Flash | `deepseek/deepseek-v4-flash` | Primary model for screening & coding |
| DeepSeek V4 Chat | `deepseek/deepseek-chat` | Fallback model |
| Python | 3.13 | Pipeline scripting |
| pdfplumber | latest | PDF text extraction |
| Zotero | 7.x | Reference management |
| Obsidian | 1.x | Note-taking & drafting |
| Smart Connections | 5.0.0 | Local semantic search (Obsidian plugin) |
| `bge-micro-v2` | — | Local embedding model (Smart Connections) |
| macOS | 13.7.8 (x64) | Host operating system |

---

## A.10 Declaration

The author declares that:

1. AI was used for screening, extraction, coding, and directed drafting assistance as described above and in the dissertation's AI-Use Statement.
2. All AI outputs were reviewed and verified by the author.
3. The author takes full responsibility for all screening verdicts, coding judgements, and the content of this dissertation.
4. All agent-drafted text was reviewed and substantially edited by the author before inclusion; no AI-generated text was incorporated without authorial review.
5. This appendix was drafted by the AI assistant (OpenClaw) at the author's direction, reviewed and edited by the author, and is included for transparency in accordance with University of Glasgow guidance on AI in research.

---

*End of Appendix A.*
