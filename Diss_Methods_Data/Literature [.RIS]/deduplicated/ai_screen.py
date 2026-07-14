#!/usr/bin/env python3
"""
SLR AI-assisted title/abstract screening script.

Reads screening_master.csv, sends each record's abstract + inclusion criteria
to OpenRouter (DS4-flash), and writes back the model's verdict.

Usage:
  1. Set OPENROUTER_API_KEY in a .env file next to this script,
     or in an .env file in the script's working directory.
  2. Run: python3 ai_screen.py

Writes results directly into the CSV (INCLUDE? column).
Keeps your existing manual annotations if you've already started.
"""
import os, sys, csv, time, re, json, argparse
from pathlib import Path

try:
    import requests
    from dotenv import load_dotenv
except ImportError:
    print("Missing dependencies. Run: pip install requests python-dotenv")
    sys.exit(1)

# ── Config ─────────────────────────────────────────────────────────────────
RIS_DIR = Path(__file__).parent.resolve()
DEFAULT_CSV = RIS_DIR / "screening_master.csv"

# ── Load .env ──────────────────────────────────────────────────────────────
env_loaded = load_dotenv(RIS_DIR / ".env")
API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
# Use the alias for DS4 flash
MODEL = "deepseek/deepseek-v4-flash"
FALLBACK_MODEL = "deepseek/deepseek-chat"

# ── System prompt: the inclusion criteria ──────────────────────────────────
SYSTEM_PROMPT = """You are an expert systematic literature review screener. Your task is to classify research records for an SLR on the dual-use nature of algorithmic governance in urban contexts.

## Research scope
This SLR investigates how urban technology/data systems — designed ostensibly for civic purposes — become instruments of spatial destruction, surveillance, and social control (domicide/urbicide). The dual-use dynamic runs through the civil-military technology nexus in cities.

## Inclusion criteria (ALL must apply)
A paper should be INCLUDED if it:
1. Addresses an urban context (smart city, city governance, urban planning, urban space)
2. Engages with data-driven / algorithmic / tech-mediated dimensions (AI, algorithms, big data, surveillance tech, platforms, sensors, automation, smart systems)
3. AND connects to at least one of:
   - Civil-military dual-use (tech serving both civic and military/security functions)
   - Securitization of urban tech (surveillance, predictive policing, border tech in cities)
   - Spatial violence / destruction / displacement (domicide, urbicide, forced eviction, spatial cleansing)
   - Algorithmic governance / control in urban space (platform urbanism, data-driven management, modulation, algorithmic sorting)
   - Weaponization of information or urban infrastructure

## Exclusion criteria (ANY sufficient for exclusion)
- Pure engineering/technical with no socio-political analysis (sensor routing, radar, signal processing)
- Military hardware only with no urban governance link (ballistics, armour, weapons engineering)
- Pre-modern or ancient history
- Medical / trauma / combat casualty
- Non-urban contexts (wildfire, agriculture, marine)
- Patents or technical method descriptions
- Unrelated biology or natural science
- Non-English without substantive English abstract
- Press release or brochure (grey lit is fine if it's analysis/report)

## Output format
Respond with EXACTLY ONE line containing only: "Include", "Exclude", or "Maybe"
- Include: clearly meets inclusion criteria
- Exclude: clearly meets exclusion criteria or is irrelevant
- Maybe: unclear from abstract, could go either way; needs full-text review"""

def _call_model(model: str, text: str, retries: int = 3) -> tuple[str, str] | None:
    """
    Try to classify with a given model. Returns (verdict, response_text) or None on 404.
    """
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        "temperature": 0.0,
        "max_tokens": 256,
        "top_p": 1.0,
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/EVasiloudes/sistema-ad-migration",
        "X-Title": "SLR-Screener",
    }

    for attempt in range(retries):
        try:
            resp = requests.post(OPENROUTER_URL, json=payload, headers=headers, timeout=60)

            # 404 = no endpoints — signal caller to try fallback model
            if resp.status_code == 404:
                return None

            resp.raise_for_status()
            data = resp.json()

            # DeepSeek V4 may return None content when thinking mode is active;
            # fall back to reasoning_content or raise to retry.
            msg = data["choices"][0]["message"]
            response_text = msg.get("content") or ""
            if not response_text:
                response_text = msg.get("reasoning_content") or ""
            if not response_text:
                raise ValueError("Empty response from model")
            response_text = response_text.strip()

            verdict_match = re.search(r'\b(Include|Exclude|Maybe)\b', response_text, re.IGNORECASE)
            if verdict_match:
                verdict = verdict_match.group(1).capitalize()
                if verdict == "Maybe":
                    verdict = "maybe"
                return verdict, response_text
            else:
                return "maybe", response_text

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
                return "error", msg
        except (KeyError, IndexError, json.JSONDecodeError, ValueError) as e:
            if attempt < retries - 1:
                wait = 2 ** attempt
                print(f"  ⚠ Parse error (attempt {attempt+1}/{retries}): {e}. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                return "error", str(e)

    return "error", f"All {retries} retries exhausted for {model}"


def classify_record(title: str, abstract: str, retries: int = 3) -> tuple[str, str]:
    """
    Returns (verdict, full_response_text)
    verdict is one of: "Include", "Exclude", "Maybe"
    """
    if not API_KEY:
        print("ERROR: OPENROUTER_API_KEY not set.")
        sys.exit(1)

    text = f"## Title\n{title}\n\n## Abstract\n{abstract}" if abstract else f"## Title\n{title}\n\n## Abstract\n[No abstract available]"

    result = _call_model(MODEL, text, retries)

    # 404 → try fallback model
    if result is None:
        print(f" ⚠ {MODEL} unavailable, trying {FALLBACK_MODEL}...", end="", flush=True)
        result = _call_model(FALLBACK_MODEL, text, retries)

    return result


def main():
    parser = argparse.ArgumentParser(description="AI-assisted SLR title/abstract screening")
    parser.add_argument("--csv", default=str(DEFAULT_CSV), help="Path to screening CSV")
    parser.add_argument("--batch", type=int, default=50, help="Batch size (records per run)")
    parser.add_argument("--start", type=int, default=1, help="Start from this row")
    parser.add_argument("--end", type=int, default=0, help="End at this row (0 = all)")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be processed but don't call API")
    parser.add_argument("--priority", choices=["HIGH", "MEDIUM", "LOW"], default=None,
                        help="Only process records with this priority")
    parser.add_argument("--no-wait", action="store_true", help="Skip rate-limit waits (risky)")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"Error: {csv_path} not found")
        sys.exit(1)

    # Read CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        all_rows = list(reader)          # keep ALL rows for full write-back
        fieldnames = reader.fieldnames

    if 'INCLUDE?' not in fieldnames:
        print("Error: CSV missing 'INCLUDE?' column")
        sys.exit(1)

    print(f"Loaded {len(all_rows)} records from {csv_path}")

    # Filter for processing only
    if args.priority:
        work_rows = [r for r in all_rows if r.get('priority', '') == args.priority]
        print(f"Filtered to {len(work_rows)} records with priority={args.priority}")
    else:
        work_rows = all_rows

    # Apply start/end bounds on work_rows
    start_idx = max(0, args.start - 1)  # IDs are 1-based
    end_idx = args.end if args.end > 0 else len(work_rows)
    rows_to_process = work_rows[start_idx:end_idx]

    print(f"Processing rows {start_idx + 1} to {min(end_idx, len(work_rows))} ({len(rows_to_process)} records)")
    print(f"Model: {MODEL}")
    print(f"API key: {API_KEY[:8]}...{API_KEY[-4:] if len(API_KEY) > 12 else ''}")

    if args.dry_run:
        print("\nDRY RUN — No API calls will be made. Would process:")
        for r in rows_to_process[:5]:
            print(f"  [{r['id']}] {r['title'][:80]}")
        if len(rows_to_process) > 5:
            print(f"  ... and {len(rows_to_process) - 5} more")
        sys.exit(0)

    # Check if we should skip already-annotated
    already_done = sum(1 for r in rows_to_process if r.get('INCLUDE?', '').strip())
    if already_done:
        print(f"  ({already_done} already have annotations — will skip those)")

    # Process
    results = {}
    stats = {"Include": 0, "Exclude": 0, "maybe": 0, "error": 0}

    for i, rec in enumerate(rows_to_process):
        rec_id = rec['id']
        existing = rec.get('INCLUDE?', '').strip()
        if existing:
            if existing in stats:
                stats[existing] += 1
            print(f"  [{rec_id}] ⏭ Already annotated: {existing}")
            continue

        title = rec.get('title', '').strip()
        abstract = rec.get('abstract', '').strip()

        # Show brief context
        print(f"  [{rec_id}] ({rec.get('priority','')}) {title[:80]}...", end="", flush=True)

        verdict, response_text = classify_record(title, abstract)

        results[rec_id] = verdict
        if verdict in stats:
            stats[verdict] += 1

        if verdict == "error":
            print(f" ❌ {response_text[:60]}")
        else:
            print(f" → {verdict}")

        # Rate limiting: be polite to OpenRouter
        if not args.no_wait and i < len(rows_to_process) - 1:
            time.sleep(0.3)  # ~3 req/s — should be fine for free/paid tier

    # Write back to CSV — always uses all_rows to preserve non-processed records
    checkpoint_counter = 0
    updated = 0
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for rec in all_rows:
            rid = rec['id']
            if rid in results:
                rec['INCLUDE?'] = results[rid]
                updated += 1
            writer.writerow(rec)
            checkpoint_counter += 1
            # Every 100 rows, flush
            if checkpoint_counter % 100 == 0:
                f.flush()

    print(f"\n{'='*50}")
    print(f"RESULTS — {len(results)} records processed, {updated} written to CSV")
    print(f"  Include: {stats['Include']}")
    print(f"  Exclude: {stats['Exclude']}")
    print(f"  Maybe:   {stats['maybe']}")
    print(f"  Error:   {stats['error']}")
    print(f"  Skipped (already annotated): {already_done}")
    print(f"\nCSV saved: {csv_path}")

if __name__ == "__main__":
    main()