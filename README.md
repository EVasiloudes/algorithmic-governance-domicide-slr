# Algorithmic Governance, Urban Space, and Domicide

**A Systematic Literature Review of the Dual-Use of Urban Algorithmic Systems, 1990–2025**

Elias Vasiloudes Nikolaides — MSc Public Policy & Management, University of Glasgow
Dissertation (URBAN5080P), submitted August 2026. Supervisor: Craig Gurney.

## About

This dissertation investigates the structural dual-use of algorithmic urban governance
technologies: the capacity of a single data infrastructure to serve civilian urban
management and military spatial destruction alike, with no new procurement — only a
change of inputs. Following a modified PRISMA protocol, 874 database records and 1,839
citation-chained candidates were screened, yielding 275 included records (270 coded).
Coding across four axes — dual-use fluidity, epistemic authority, the machinic city,
spatial destruction — reveals a literature whose elements are documented but segregated:
the governance and destruction literatures run in parallel, with only five records
addressing algorithmically mediated urbicide.

## Repository structure

| Path | Contents |
|---|---|
| `final-draft/` | LaTeX source of the dissertation (`dissertation.tex`, `chapters/`, `refs.bib`, `figures/`), the compiled `dissertation.pdf`, and a `Makefile` (XeLaTeX + biber) |
| `Diss_Methods_Data/` | The systematic-review reproducibility package |
| `Diss_Methods_Data/SLR.log.md` | Full audit log: every search, screening run, and pipeline execution with timestamps and counts |
| `Diss_Methods_Data/Literature [.RIS]/` | Search exports (RIS), deduplication records, screening master, included-record lists |
| `Diss_Methods_Data/analysis/` | Screening/coding outputs (CSVs, JSON), snowball pipeline, synthesis files |
| `Diss_Methods_Data/corpus/scripts/` | PDF extraction and thematic-coding pipeline scripts |

## Data availability

Record metadata, screening verdicts, coding scores, scripts, prompts, and logs are
included in full. The extracted full texts and PDFs of the reviewed publications are
**not** redistributed here for copyright reasons; the included-record lists
(`Included_151_records.ris`, `analysis/snowball/snowball_included_124.ris`) identify
every record by DOI/title so the corpus can be reassembled from the sources.

## AI-use disclosure

AI assistance (a large-language-model classifier, DeepSeek V4 Flash, temperature 0.0)
was used for screening and coding support against a written codebook, with all outputs
reviewed and all final decisions retained by the author, as disclosed in the
dissertation's AI-Use Statement (Appendix A) and §3.4–3.5. The workflow was discussed
with and confirmed as compliant by the supervisor.

## Rebuilding the PDF

```sh
cd final-draft
make        # requires XeLaTeX + biber (TeX Live)
```
