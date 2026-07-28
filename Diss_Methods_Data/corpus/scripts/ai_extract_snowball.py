#!/usr/bin/env python3
"""
Snowball AI-assisted full-text extraction and thematic coding script.

Reads each snowball-Included paper's full text, sends it to OpenRouter (DS4-flash)
with the same structured extraction prompt as the main pipeline, and writes
JSON results to a CSV + per-paper JSON files for human review.

Usage:
  1. Set OPENROUTER_API_KEY in a .env file next to this script
     (or in Diss_Methods_Data/Literature [.RIS]/deduplicated/.env).
  2. Run: python3 ai_extract_snowball.py

Pattern cloned from ai_extract.py — same API client, same resumability,
same rate limiting, same codebook.

Output:
  - Diss_Methods_Data/corpus/extraction_results_snowball.csv  (flat table)
  - Diss_Methods_Data/corpus/extractions_snowball/*.json      (per-paper)
"""

import os, sys, csv, time, re, json, argparse
from pathlib import Path

try:
    import requests
    from dotenv import load_dotenv
except ImportError:
    print("Missing dependencies. Run: pip install requests python-dotenv")
    sys.exit(1)

# ── Paths ──────────────────────────────────────────────────────────────────
REPO = Path("/Users/eliasvasnic/Obsidian Vaults/Elias Vasnic Obsidian Vault/"
            "Atoms/Public_Policy_&_Management/Courses/MSc PPM Dissertation - Repo")
CORPUS = REPO / "Diss_Methods_Data" / "corpus"
TEXT_DIR = CORPUS / "text_snowball"
METADATA_CSV = CORPUS / "metadata_snowball.csv"
SCREENING_CSV = REPO / "Diss_Methods_Data" / "analysis" / "snowball" / "snowball_screening.csv"
OUTPUT_CSV = CORPUS / "extraction_results_snowball.csv"
EXTRACTIONS_DIR = CORPUS / "extractions_snowball"

# ── Load .env ──────────────────────────────────────────────────────────────
# Try snowball dir first, then main pipeline dir
env_paths = [
    REPO / "Diss_Methods_Data" / "analysis" / "snowball" / ".env",
    REPO / "Diss_Methods_Data" / "Literature [.RIS]" / "deduplicated" / ".env",
]
env_loaded = False
for ep in env_paths:
    if ep.exists():
        load_dotenv(ep)
        env_loaded = True
        break

API_KEY = os.environ.get("OPENROUTER_API_KEY", "").strip().strip('"').strip("'")
if not API_KEY:
    print("ERROR: OPENROUTER_API_KEY not set in .env file")
    print(f"  Looked in: {', '.join(str(p) for p in env_paths)}")
    sys.exit(1)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-v4-flash"
FALLBACK_MODEL = "deepseek/deepseek-chat"
MAX_CHARS = 450000

# ── System prompt ──────────────────────────────────────────────────────────
# Identical to the main pipeline — see ai_extract.py for full rationale.
SYSTEM_PROMPT = """You are an expert research assistant extracting structured data for a systematic literature review on the DUAL-USE NATURE OF ALGORITHMIC GOVERNANCE IN URBAN CONTEXTS.

## Research scope
This SLR investigates how urban technology/data systems — designed ostensibly for civic governance — become instruments of spatial destruction, surveillance, and social control. The central claim: algorithmic governance tools are *structurally* dual-use in ways that physical infrastructure is not, because software/data has near-zero marginal cost of reproduction and frictionless transferability between civilian and military domains.

## Your task
Read the provided paper text and extract structured information against the coding framework below. Be precise and evidence-based. Only code what the paper actually discusses, not what you infer. If a theme is absent, score it 0. If the text is truncated or incomplete, note this and do your best — set scores to null only if the content is genuinely insufficient to judge.

## Coding Framework

### Theme 1: Information Good & Dual-Use Fluidity
**Theorist:** Arrow (1962) — information goods have near-zero marginal cost, are non-rivalrous, and transfer frictionlessly across domains.

**Indicators (score higher for more matches):**
- Discusses the economic/material properties of software/data that distinguish it from physical infrastructure
- Addresses dual-use or technology transfer between civilian and military/security domains
- Mentions repurposing, reparameterisation, or redeployment of civilian urban tech for military/security functions
- Discusses data sharing, interoperability, or integration between civilian urban systems and military/security systems
- Engages with the "dual-use" concept explicitly or through related terms (dual-purpose, civil-military convergence, technology transfer)

**Scoring:**
- 0 = Not addressed
- 1 = Tangential mention (e.g., single sentence noting dual-use possibility)
- 2 = Substantive engagement (dedicated section or sustained argument about dual-use/transfer)
- 3 = Central argument (the paper's primary contribution is about dual-use properties, technology transfer, or civil-military convergence of urban tech)

### Theme 2: Epistemic Authority & Black-Boxing
**Theorists:** Michael (2007) — data confers epistemic authority that bypasses democratic deliberation; Pasquale (2015) — algorithmic opacity.

**Indicators:**
- Discusses algorithmic opacity, black-boxing, or lack of transparency in urban governance systems
- Addresses the epistemic authority of data-driven systems (who defines reality through data?)
- Engages with surveillance as a knowledge-producing function, not just monitoring
- Discusses the "God's Eye View" of remote sensing/surveillance — asymmetric knowledge production
- Addresses democratic deficit, accountability gaps, or bypassing of deliberation through algorithmic decision-making
- Mentions machine learning bias, training data politics, or the constructed nature of algorithmic "truth"

**Scoring:** 0–3 (same scale as Theme 1)

### Theme 3: Machinic City & Modulation
**Theorists:** Deleuze (1990) — control societies operate through continuous modulation, not visible discipline; De Landa (1992/2014) — cities as machinic assemblages, programmable fields.

**Indicators:**
- Conceptualises the city as a programmable, algorithmic, or data-driven system
- Discusses continuous modulation of urban populations through data (traffic, movement, behaviour)
- Addresses the shift from visible institutional power to ambient/algorithmic control
- Engages with "smart city" as a mode of governance, not just infrastructure
- Discusses population-level data analytics as a mode of urban management
- Mentions automated decision-making, real-time urban dashboards, or algorithmic sorting of urban populations

**Scoring:** 0–3

### Theme 4: Spatial Collapse & Home Unmaking
**Theorists:** King (2004) — home as ontological dwelling; Graham (2006/2011) — new military urbanism, cities as battlespace; Weizman (2007) — vertical sovereignty, Forensic Architecture.

**Indicators:**
- Discusses spatial destruction, domicide, urbicide, or the deliberate destruction of urban space
- Addresses the weaponisation of civilian infrastructure or urban data for targeting
- Engages with home unmaking, displacement, forced eviction, or spatial cleansing
- Discusses urban warfare, the city as battlespace, or militarised urban policing
- Mentions Forensic Architecture, counter-forensics, or documentation of spatial violence
- Addresses vertical sovereignty (drones, aerial surveillance, volumetric control of urban space)

**Scoring:** 0–3

## Additional extraction fields

### Dual-use assessment
- **dual_use_explicit**: Does the paper explicitly discuss dual-use? ("yes" = uses the term or concept directly; "tangential" = discusses related transfer but doesn't name it; "no" = no dual-use discussion)
- **dual_use_direction**: If dual-use is discussed, what is the direction of the technology transfer described? ("civil_to_military", "military_to_civil", "both", "neither")
- **dual_use_structural**: Does the paper address the *structural* properties that make dual-use possible (e.g., software properties, data portability, interoperability standards)? ("yes", "no", "tangential")

### Methodology and geography
- **doc_type**: journal_article, book_chapter, policy_report, conference_paper, grey_lit, thesis, edited_volume, other
- **methodology**: empirical_qualitative, empirical_quantitative, empirical_mixed, theoretical, review, policy_analysis, case_study, other
- **geography**: region/country/context discussed, or "global" if no specific geography

### Summary and evidence
- **thesis**: One-sentence summary of the paper's main argument or contribution (max 200 chars)
- **key_quotes**: Up to 3 direct quotes from the text that capture the paper's position on any of the four themes. Include enough surrounding context to make each quote meaningful. Prefer quotes that address dual-use, algorithmic governance, urban destruction, or theoretical claims about data/technology.
- **policy_relevance**: Brief note on any policy implications or recommendations discussed, or "None"

## Output format
Respond with EXACTLY a valid JSON object (no markdown code fences, no commentary, no trailing text) with these fields:

{
  "title": "Full title as it appears in the text",
  "year": "YYYY or null",
  "doi": "DOI string or null",
  "doc_type": "journal_article|book_chapter|policy_report|conference_paper|grey_lit|thesis|edited_volume|other",
  "methodology": "empirical_qualitative|empirical_quantitative|empirical_mixed|theoretical|review|policy_analysis|case_study|other",
  "geography": "region/country or 'global'",
  "thesis": "One-sentence summary (max 200 chars)",
  "theme_1_score": 0,
  "theme_1_justification": "Evidence from text or 'Not addressed'",
  "theme_2_score": 0,
  "theme_2_justification": "Evidence from text or 'Not addressed'",
  "theme_3_score": 0,
  "theme_3_justification": "Evidence from text or 'Not addressed'",
  "theme_4_score": 0,
  "theme_4_justification": "Evidence from text or 'Not addressed'",
  "dual_use_explicit": "yes|no|tangential",
  "dual_use_direction": "civil_to_military|military_to_civil|both|neither",
  "dual_use_structural": "yes|no|tangential",
  "key_quotes": ["Quote 1 with context", "Quote 2", "Quote 3"],
  "policy_relevance": "Brief note or 'None'",
  "notes": "Any caveats: truncated text, edited volume, very short paper, etc."
}

## Important rules
- ONLY output the JSON object. No markdown code fences (no ```json), no explanatory text before or after.
- Be conservative with scores. A score of 3 means the theme is CENTRAL to the paper's primary argument. Most papers will score 1 or 2 on most themes.
- For key_quotes, use EXACT text from the paper. Do not paraphrase. Wrap in quotes.
- If the text is an edited volume with multiple chapters, note this in "notes" and extract based on the visible chapters.
- If a field cannot be determined from the available text, use null for that field."""


# ── Helpers ────────────────────────────────────────────────────────────────
def _normalise(s):
    s = s.lower().strip()
    s = re.sub(r'\s+', ' ', s)
    s = s.replace(':', '').replace(',', '').replace('.', '').replace('"', '').replace("'", "")
    return s[:200]


def truncate_text(text, max_chars=MAX_CHARS):
    text = text.strip()
    if len(text) <= max_chars:
        return text, False

    intro_chars = int(max_chars * 0.55)
    conclusion_chars = int(max_chars * 0.25)
    middle_budget = max_chars - intro_chars - conclusion_chars

    intro = text[:intro_chars]
    conclusion = text[-conclusion_chars:]

    middle_text = text[intro_chars:len(text) - conclusion_chars]
    paragraphs = middle_text.split('\n\n')

    if len(paragraphs) > 20:
        step = max(1, len(paragraphs) // 15)
        sampled = [p.strip() for i, p in enumerate(paragraphs)
                   if i % step == 0 and p.strip()]
        middle_sample = '\n\n'.join(sampled)
    else:
        middle_sample = middle_text

    if len(middle_sample) > middle_budget:
        middle_sample = middle_sample[:middle_budget]

    truncated = (
        intro + "\n\n"
        "[... TEXT TRUNCATED — middle section sampled ...]\n\n"
        + middle_sample + "\n\n"
        "[... continued ...]\n\n"
        + conclusion
    )
    return truncated[:max_chars], True


def find_text_file(title, text_dir, metadata_map):
    norm_title = _normalise(title)
    if norm_title in metadata_map:
        path = metadata_map[norm_title]
        full_path = REPO / path
        if full_path.exists():
            return full_path

    for f in text_dir.glob("*.txt"):
        if _normalise(f.stem) == norm_title:
            return f

    title_words = set(norm_title.split()) - {
        "the", "a", "an", "of", "in", "and", "to", "for", "on",
        "is", "with", "from", "by", "at", "its", "or", "as",
        "be", "this", "that", "not", "are", "was", "but", "has"
    }
    best_score, best_file = 0, None
    for f in text_dir.glob("*.txt"):
        f_words = set(_normalise(f.stem).replace('_', ' ').split())
        score = len(title_words & f_words)
        if score > best_score:
            best_score, best_file = score, f
    return best_file if best_file and best_score >= 4 else None


def load_metadata_map():
    if not METADATA_CSV.exists():
        print(f"Warning: {METADATA_CSV} not found")
        return {}
    mapping = {}
    with open(METADATA_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row.get('title', '')
            text_path = row.get('text_path', '')
            if title and text_path and row.get('extraction_ok', '').lower() == 'true':
                mapping[_normalise(title)] = text_path
    return mapping


def load_snowball_includes():
    """Load Include-verdict records from snowball_screening.csv."""
    if not SCREENING_CSV.exists():
        print(f"Error: {SCREENING_CSV} not found")
        sys.exit(1)
    with open(SCREENING_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        all_rows = list(reader)
    # Return only Include verdicts, keyed by openalex_id
    return {r['openalex_id']: r for r in all_rows if r.get('verdict', '').strip() == 'Include'}


def load_existing_results():
    if not OUTPUT_CSV.exists():
        return {}
    existing = {}
    with open(OUTPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            oid = row.get('openalex_id', '')
            if oid:
                existing[oid] = row
    return existing


def _call_model(model, text, retries=3):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        "temperature": 0.0,
        "max_tokens": 4096,
        "top_p": 1.0,
        "response_format": {"type": "json_object"},
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/EVasiloudes/sistema-ad-migration",
        "X-Title": "SLR-Snowball-Extractor",
    }

    for attempt in range(retries):
        try:
            resp = requests.post(OPENROUTER_URL, json=payload, headers=headers, timeout=120)
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            data = resp.json()
            msg = data["choices"][0]["message"]
            response_text = msg.get("content") or msg.get("reasoning_content") or ""
            if not response_text.strip():
                raise ValueError("Empty response from model")
            response_text = response_text.strip()
            if response_text.startswith("```"):
                response_text = re.sub(r'^```(?:json)?\s*', '', response_text)
                response_text = re.sub(r'\s*```$', '', response_text)
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                m = re.search(r'\{.*\}', response_text, re.DOTALL)
                if m:
                    return json.loads(m.group(0))
                raise
        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response') and e.response is not None and e.response.status_code == 404:
                return None
            detail = ""
            if hasattr(e, 'response') and e.response is not None:
                try:
                    detail = e.response.text[:300]
                except Exception:
                    pass
            msg = f"{e}" + (f" | {detail}" if detail else "")
            if attempt < retries - 1:
                wait = 2 ** attempt
                print(f"  ⚠ Request failed (attempt {attempt+1}/{retries}): {msg}. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"  ✖ All retries exhausted: {msg}")
                return None
        except (KeyError, IndexError, json.JSONDecodeError, ValueError) as e:
            if attempt < retries - 1:
                wait = 2 ** attempt
                print(f"  ⚠ Parse error (attempt {attempt+1}/{retries}): {e}. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"  ✖ All retries exhausted (parse): {e}")
                return None
    return None


def extract_record(openalex_id, via, title, text_content):
    text_to_send, was_truncated = truncate_text(text_content)

    user_msg = f"""## Paper Metadata
- Snowball anchor: {via}
- OpenAlex ID: {openalex_id}

## Full Text
{text_to_send}"""

    if was_truncated:
        user_msg += "\n\n[Note: This text was truncated from a larger source. Code based on available content.]"

    result = _call_model(MODEL, user_msg)
    if result is None:
        print(f"  ⚠ {MODEL} unavailable, trying {FALLBACK_MODEL}...", end="", flush=True)
        result = _call_model(FALLBACK_MODEL, user_msg)

    if result is not None:
        result['via'] = via
        result['text_truncated'] = was_truncated

    return result


# ── CSV output ─────────────────────────────────────────────────────────────
EXTRACTION_FIELDNAMES = [
    "openalex_id", "via", "title",
    "year", "doi", "doc_type", "methodology", "geography",
    "thesis",
    "theme_1_score", "theme_1_justification",
    "theme_2_score", "theme_2_justification",
    "theme_3_score", "theme_3_justification",
    "theme_4_score", "theme_4_justification",
    "dual_use_explicit", "dual_use_direction", "dual_use_structural",
    "key_quotes", "policy_relevance",
    "text_truncated", "notes",
]


def write_results_csv(all_results, path):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=EXTRACTION_FIELDNAMES,
                                extrasaction='ignore')
        writer.writeheader()
        for r in all_results:
            row = dict(r)
            if isinstance(row.get('key_quotes'), list):
                row['key_quotes'] = " || ".join(row['key_quotes'])
            writer.writerow(row)


def write_json_extraction(result, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_id = str(result.get('openalex_id', 'unknown')).replace('https://openalex.org/', '')
    safe_title = re.sub(r'[^a-zA-Z0-9_\- ]', '',
                        result.get('title', 'untitled'))[:80].strip()
    filename = f"{safe_id}_{safe_title}.json".replace(' ', '_')
    with open(output_dir / filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)


# ── Main ───────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="AI-assisted snowball full-text extraction and thematic coding")
    parser.add_argument("--batch", type=int, default=10,
                        help="Batch size (records per run)")
    parser.add_argument("--start", type=int, default=0,
                        help="Start from this index (0-based)")
    parser.add_argument("--end", type=int, default=0,
                        help="End at this index (0 = all)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would be processed without calling API")
    parser.add_argument("--no-wait", action="store_true",
                        help="Skip rate-limit waits")
    args = parser.parse_args()

    print("Loading snowball Includes from snowball_screening.csv...")
    includes = load_snowball_includes()
    print(f"  {len(includes)} Include records")

    metadata_map = load_metadata_map()
    print(f"  {len(metadata_map)} records in metadata map")

    existing = load_existing_results()
    print(f"  {len(existing)} already extracted")

    all_results = list(existing.values()) if existing else []

    # Determine work queue — skip already extracted
    to_process = []
    for oid, rec in includes.items():
        if oid in existing:
            continue
        to_process.append(rec)

    if args.end > 0:
        to_process = to_process[args.start:args.end]
    elif args.start > 0:
        to_process = to_process[args.start:]

    print(f"\nWill process {len(to_process)} records (batch: {args.batch})")
    print(f"Model: {MODEL}")
    print(f"Text ceiling: {MAX_CHARS//1000}K chars (~{MAX_CHARS//4//1000}K tokens)")

    if args.dry_run:
        print("\nDRY RUN — No API calls:")
        for r in to_process[:10]:
            print(f"  [{r['openalex_id'][:30]}...] {r['title'][:80]}")
        if len(to_process) > 10:
            print(f"  ... and {len(to_process) - 10} more")
        sys.exit(0)

    already = sum(1 for r in includes if r in existing)
    if already:
        print(f"  ({already} already extracted — skipping)")

    stats = {"processed": 0, "found_text": 0, "no_text": 0,
             "extracted": 0, "failed": 0}

    for i, rec in enumerate(to_process):
        oid = rec['openalex_id']
        via = rec.get('via', '')
        title = rec.get('title', '').strip()
        year = rec.get('year', '')
        doi = rec.get('doi', '')

        print(f"\n[{oid[:40]}...] {title[:80]}")

        text_path = find_text_file(title, TEXT_DIR, metadata_map)
        if not text_path:
            print(f"  ✖ No text file found")
            stats["no_text"] += 1
            all_results.append({
                "openalex_id": oid, "via": via,
                "title": title,
                "year": year if year else None,
                "doi": doi if doi else None,
                "notes": "No text file found in corpus",
            })
            write_results_csv(all_results, OUTPUT_CSV)
            continue

        stats["found_text"] += 1
        text_size = text_path.stat().st_size
        print(f"  ✓ Text: {text_size:,} bytes ({text_path.name})")

        try:
            text_content = text_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            try:
                text_content = text_path.read_text(encoding='latin-1')
            except Exception as e:
                print(f"  ✖ Cannot read: {e}")
                stats["failed"] += 1
                continue

        token_est = len(text_content) // 4
        will_truncate = len(text_content) > MAX_CHARS
        status = "⚠ TRUNCATED" if will_truncate else "✓ fits"
        print(f"  ~{token_est:,} tokens — {status}")

        print(f"  → Sending to {MODEL}...", end="", flush=True)
        result = extract_record(oid, via, title, text_content)

        if result is None:
            print(" ✖ FAILED")
            stats["failed"] += 1
            all_results.append({
                "openalex_id": oid, "via": via,
                "title": title,
                "year": year if year else None,
                "doi": doi if doi else None,
                "notes": "API extraction failed after all retries",
            })
        else:
            result["openalex_id"] = oid
            stats["extracted"] += 1

            scores = [
                result.get('theme_1_score', 0) or 0,
                result.get('theme_2_score', 0) or 0,
                result.get('theme_3_score', 0) or 0,
                result.get('theme_4_score', 0) or 0,
            ]
            print(f" ✓ T1={scores[0]} T2={scores[1]} T3={scores[2]} T4={scores[3]}")

            all_results.append(result)
            write_json_extraction(result, EXTRACTIONS_DIR)

        write_results_csv(all_results, OUTPUT_CSV)
        stats["processed"] += 1

        if args.batch and stats["processed"] >= args.batch:
            print(f"\n  Batch limit ({args.batch}) reached. Run again to continue.")
            break

        if not args.no_wait and i < len(to_process) - 1:
            time.sleep(0.5)

    # ── Summary ────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"EXTRACTION SUMMARY (SNOWBALL)")
    print(f"  Processed this run:     {stats['processed']}")
    print(f"  Text files found:       {stats['found_text']}")
    print(f"  No text file:           {stats['no_text']}")
    print(f"  Successfully extracted: {stats['extracted']}")
    print(f"  Extraction failed:      {stats['failed']}")
    print(f"  Previously extracted:   {already}")
    print(f"  Total in output CSV:    {len(all_results)}")
    print(f"\n  Output CSV: {OUTPUT_CSV}")
    print(f"  JSON files:  {EXTRACTIONS_DIR}/")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
