---
tags:
  - MSc_PPM
  - Dissertation_MSc
---

# AGENTS.md — Dissertation Project Conventions

Project: MSc Public Policy & Management dissertation (URBAN5080P, University of Glasgow).
Topic: Algorithmic governance, urban space, and domicide — a systematic literature review (SLR) of the dual-use nature of urban data technologies, 1990–2025.
Author: Elias Vasnic. Supervisor: Craig.

## Project layout

| Path | Role |
|---|---|
| `Formative Methods - Urban Studies Dissertation (revised).md` | **Canonical working draft** (intro + methods). Edit this one. |
| `Formative Methods - Urban Studies Dissertation.md` | Frozen formative submission (May 29, 2026). Do NOT edit. |
| `Diss_Methods_Data/SLR.log.md` | Append-only audit log of all search strings, counts, and calibration iterations. Never rewrite history in this file; add new dated sections. |
| `Diss_Methods_Data/` | Meeting agendas, correspondence drafts, SLR working data. |
| `Writing Plan v0.md` | Current writing plan and task decomposition. |
| `Dissertation Urban Studies URBAN5080P.md`, `Assessment URBAN5080P.md` | Course requirements / assessment criteria. Read-only reference. |
| Source-note files (DeLanda, Deleuze, Michael, etc.) | Reading notes. Read-only reference unless asked. |
| `img/`, `attachments/` | Assets. |

## Hard rules

1. **Never edit the frozen formative submission** (`Formative Methods - Urban Studies Dissertation.md`).
2. **`SLR.log.md` is append-only.** Every search-string change gets a new dated "Calibration Iteration" section with: trigger, diagnosis, action, full revised string, result count.
3. **No fabricated citations.** Every reference added to any chapter must correspond to a real, verifiable work. If uncertain, flag it as `[VERIFY]` rather than inventing details.
4. **British English** throughout (algorithmisation, weaponised, defence, utilise).
5. **The author's voice and argument take precedence.** Agents propose, edit, and verify; substantive intellectual claims are the author's. All agent-assisted text must be flagged for authorial review before being treated as final (see AI-use statement in the draft).
6. **Methodological integrity:** the SLR must remain auditable. Do not retroactively alter inclusion/exclusion criteria, search strings, or counts to fit desired results. Calibration is fine; it must be logged.

## Known environment quirks

- This vault is open in **Obsidian**, which intermittently rewrites files (whitespace/sync churn). `edit_file`-style exact-match edits frequently fail on files Obsidian has open. **Workaround:** re-read immediately before editing; if matches still fail, apply edits via a Python script run in the terminal (read → replace → write), then delete the script.
- Paths contain spaces and `&` — always quote paths in shell commands.
- Git: single worktree on `main`. Commit at meaningful checkpoints with descriptive messages. Do not create branches unless asked.

## Style for dissertation prose

- Academic register; confident but not overclaiming ("test" not "prove"; "indicates" not "demonstrates" unless warranted).
- Citations in author-date style matching the working reference list format.
- Keep the normative introduction and the open-diagnostic methodology bridged: the SLR *tests* the dual-use thesis, it does not assume it.
- Mermaid diagrams are used for the PRISMA flow and conceptual figures; keep them theme-neutral (no hardcoded colors).

## Key methodological commitments (do not silently contradict)

- Modified PRISMA 2020; completed flow diagram with real ns.
- Two-search strategy (A: high recall civil-military nexus; B: high precision spatial destruction), merged at deduplication. Zotero + Rayyan pipeline.
- Single-iteration backward+forward snowballing from 3–5 anchors (Graham 2006, Kitchin 2014, Weizman 2007 provisional); Wohlin (2014) citation.
- Date window 1990–2025 inclusive (`PUBYEAR > 1989 AND PUBYEAR < 2026` in Scopus).
- Single-reviewer mitigations: 10% pilot screen with supervisor; decision journal.
- Grey lit: Overton (trial-capped — see SLR.log.md and limitations) + Policy Commons; AACODS appraisal.
- Four acknowledged limitations (language, single-reviewer, grey-lit unevenness, Overton trial cap).
