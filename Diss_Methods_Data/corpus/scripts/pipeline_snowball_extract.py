#!/usr/bin/env python3
"""
pipeline_snowball_extract.py — Snowball RIS export → PDF → text → metadata CSV

Reads from the SNOWBALLED-RECORDS Zotero export + files directory.
Uses the Zotero SQLite database to map RIS records to their PDF files.

Usage:
    python3 pipeline_snowball_extract.py
"""

import os, json, csv, sys, re, shutil, sqlite3
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(line_buffering=True)

# ── Paths ──────────────────────────────────────────────────────────────────
REPO = Path("/Users/eliasvasnic/Obsidian Vaults/Elias Vasnic Obsidian Vault/Atoms/Public_Policy_&_Management/Courses/MSc PPM Dissertation - Repo")
CORPUS = REPO / "Diss_Methods_Data" / "corpus"
PDF_DIR = CORPUS / "pdfs_snowball"
TEXT_DIR = CORPUS / "text_snowball"
METADATA_PATH = CORPUS / "metadata_snowball.csv"
LOG_PATH = CORPUS / "extraction_log_snowball.json"
RUNLOG = CORPUS / "run_snowball.log"

EXPORT_DIR = REPO / "Diss_Methods_Data" / "{exported from Zotero}" / "SNOWBALLED-RECORDS{export from Zotero}"
RIS_FILE = next(EXPORT_DIR.glob("*.ris"), None)
FILES_DIR = EXPORT_DIR / "files"

# Zotero DB — snowball collection = 95
ZOTERO_DB = Path.home() / "Zotero" / "zotero.sqlite"
COLLECTION_ID = 95


# ── Helpers ────────────────────────────────────────────────────────────────
def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(RUNLOG, "a") as f:
        f.write(line + "\n")


def sanitise_filename(title):
    safe = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in title)
    return (safe.strip().replace(' ', '_')[:200]) or "untitled"


def parse_ris(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        content = f.read()

    raw_records = re.split(r'(?=^TY  -)', content, flags=re.MULTILINE)
    records = []

    for raw in raw_records:
        if not raw.strip():
            continue
        rec = {}
        current_tag = None
        current_value = []

        for line in raw.splitlines():
            line = line.rstrip()
            if not line:
                continue
            if line.startswith("  ") and current_tag:
                current_value.append(line.strip())
                continue
            m = re.match(r'^([A-Z0-9]{2,4})  - (.+)$', line)
            if m:
                if current_tag:
                    val = " ".join(current_value) if current_value else ""
                    if current_tag == "AU":
                        rec.setdefault("authors", []).append(val)
                    elif current_tag == "KW":
                        rec.setdefault("keywords", []).append(val)
                    else:
                        rec[current_tag] = val
                current_tag = m.group(1)
                current_value = [m.group(2)]
            elif current_tag:
                current_value.append(line.strip())

        if current_tag:
            val = " ".join(current_value) if current_value else ""
            if current_tag == "AU":
                rec.setdefault("authors", []).append(val)
            elif current_tag == "KW":
                rec.setdefault("keywords", []).append(val)
            else:
                rec[current_tag] = val

        if rec.get("TY"):
            records.append(rec)

    return records


def _normalise(s):
    s = s.lower().strip()
    s = re.sub(r'\s+', ' ', s)
    s = s.replace(':', '').replace(',', '').replace('.', '').replace('"', '').replace("'", "")
    return s[:200]


def build_pdf_lookup():
    """Build title → (itemID, pdf_filename) lookup from Zotero DB for snowball collection."""
    db_tmp = Path("/tmp/zotero_snowball_lookup.sqlite")
    shutil.copy2(str(ZOTERO_DB), str(db_tmp))
    conn = sqlite3.connect(str(db_tmp))
    c = conn.execute("""
        SELECT i.itemID, idv.value, ia.path
        FROM items i
        JOIN collectionItems cmi ON i.itemID = cmi.itemID AND cmi.collectionID = ?
        JOIN itemAttachments ia ON i.itemID = ia.parentItemID
        JOIN itemData id ON i.itemID = id.itemID AND id.fieldID = (SELECT fieldID FROM fields WHERE fieldName = 'title')
        JOIN itemDataValues idv ON id.valueID = idv.valueID
        WHERE ia.contentType = 'application/pdf'
        ORDER BY i.itemID
    """, (COLLECTION_ID,))
    rows = c.fetchall()
    conn.close()

    lookup = {}
    for item_id, title, path_str in rows:
        norm = _normalise(title)
        pdf_filename = path_str.replace("storage:", "", 1) if path_str.startswith("storage:") else path_str
        lookup.setdefault(norm, []).append((item_id, pdf_filename))

    return lookup


def find_pdf_for_record(rec, files_dir, pdf_lookup):
    title = rec.get("TI", rec.get("T1", ""))
    norm_title = _normalise(title)

    # 1. Exact title match from DB lookup
    if norm_title in pdf_lookup:
        for item_id, pdf_filename in pdf_lookup[norm_title]:
            subdir = files_dir / str(item_id)
            pdf_path = subdir / pdf_filename
            if pdf_path.exists():
                return pdf_path
            if subdir.is_dir():
                pdfs = list(subdir.glob("*.pdf"))
                if pdfs:
                    return pdfs[0]

    # 2. Fuzzy match
    authors = rec.get("authors", [])
    year = rec.get("PY", rec.get("Y1", ""))[:4]
    author_surname = authors[0].split(",")[0].strip().lower() if authors else ""

    best_score = 0
    best_pdf = None
    for subdir in files_dir.iterdir():
        if not subdir.is_dir():
            continue
        for f in subdir.iterdir():
            if f.suffix.lower() != ".pdf":
                continue
            name = f.stem.lower()
            score = 0
            if author_surname and author_surname in name:
                score += 5
            if year and year in name:
                score += 2
            title_words = set(norm_title.split()) - {
                "the", "a", "an", "of", "in", "and", "to", "for", "on",
                "is", "with", "from", "by", "at", "its", "or", "as",
                "be", "this", "that", "not", "are", "was", "but", "has"
            }
            name_words = set(name.replace('-', ' ').split())
            common = title_words & name_words
            score += len(common)
            if score > best_score:
                best_score = score
                best_pdf = f

    if best_pdf and best_score >= 3:
        return best_pdf
    return None


def extract_text_from_pdf(pdf_path):
    try:
        import pdfplumber
        text_content = []
        with pdfplumber.open(str(pdf_path)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text_content.append(t)
        full_text = "\n\n".join(text_content)
        if len(full_text.strip()) < 50:
            raise ValueError("Too little text extracted")
        return full_text
    except Exception:
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(str(pdf_path))
            return "\n\n".join(p.extract_text() or "" for p in reader.pages)
        except ImportError:
            return ""


# ── Main ───────────────────────────────────────────────────────────────────
def main():
    log("=" * 60)
    log("SNOWBALL Pipeline: RIS Export → PDF → Text Extraction")
    log(f"Started: {datetime.now().isoformat()}")
    log(f"Export source: {EXPORT_DIR}")
    log("=" * 60)

    for d in [PDF_DIR, TEXT_DIR]:
        d.mkdir(parents=True, exist_ok=True)
    RUNLOG.write_text("")

    log("Building PDF lookup from Zotero database (collection 95)...")
    pdf_lookup = build_pdf_lookup()
    db_item_count = sum(len(v) for v in pdf_lookup.values())
    log(f"✓ {db_item_count} PDF entries in lookup table")

    log(f"Parsing RIS: {RIS_FILE.name}...")
    records = parse_ris(RIS_FILE)
    log(f"✓ {len(records)} records found")

    stats = {
        "total": len(records), "valid": 0, "no_pdf": 0,
        "extraction_ok": 0, "extraction_failed": 0, "errors": [],
    }
    results = []

    for idx, rec in enumerate(records, 1):
        title = rec.get("TI", rec.get("T1", "UNTITLED"))
        authors = rec.get("authors", [])
        year = rec.get("PY", rec.get("Y1", ""))[:4]
        doi = rec.get("DO", "")
        item_type = rec.get("TY", "")
        abstract = rec.get("N2", rec.get("AB", ""))
        keywords = rec.get("keywords", [])

        safe_name = sanitise_filename(title)
        log(f"[{idx:3d}/{len(records)}] {title[:80]}")

        pdf_src = find_pdf_for_record(rec, FILES_DIR, pdf_lookup)

        if not pdf_src or not pdf_src.exists():
            stats["no_pdf"] += 1
            results.append({
                "title": title, "authors": "; ".join(authors), "year": year,
                "doi": doi, "item_type": item_type, "abstract": abstract,
                "keywords": "; ".join(keywords),
                "status": "no_pdf", "pdf_filename": None,
                "text_path": None, "extraction_ok": False, "note": "No PDF found in export",
            })
            log("  📄 NO PDF")
            continue

        pdf_filename_disk = f"{safe_name}.pdf"
        pdf_dst = PDF_DIR / pdf_filename_disk
        if not pdf_dst.exists():
            shutil.copy2(str(pdf_src), str(pdf_dst))
        stats["valid"] += 1
        log(f"  ✓ PDF ({pdf_src.stat().st_size / 1024:.0f} KB)")

        text_path = TEXT_DIR / f"{safe_name}.txt"
        if text_path.exists() and text_path.stat().st_size > 0:
            existing_text = text_path.read_text(encoding="utf-8")
            if existing_text.strip() != "EXTRACTION_FAILED" and len(existing_text.strip()) >= 50:
                stats["extraction_ok"] += 1
                log(f"  ✓ Text already extracted: {len(existing_text):,} chars")
                extraction_ok = True
            else:
                stats["extraction_failed"] += 1
                extraction_ok = False
        else:
            try:
                full_text = extract_text_from_pdf(pdf_dst)
                if len(full_text.strip()) >= 50:
                    text_path.write_text(full_text, encoding="utf-8")
                    stats["extraction_ok"] += 1
                    log(f"  ✓ Text: {len(full_text):,} chars")
                    extraction_ok = True
                else:
                    stats["extraction_failed"] += 1
                    text_path.write_text(full_text or "EXTRACTION_FAILED\n", encoding="utf-8")
                    extraction_ok = False
                    log(f"  ⚠ Text too short ({len(full_text.strip())} chars)")
            except Exception as e:
                stats["extraction_failed"] += 1
                stats["errors"].append(f"{safe_name}: extraction failed: {e}")
                text_path.write_text("EXTRACTION_FAILED\n", encoding="utf-8")
                extraction_ok = False
                log(f"  ✖ EXTRACTION FAILED: {e}")

        results.append({
            "title": title, "authors": "; ".join(authors), "year": year,
            "doi": doi, "item_type": item_type, "abstract": abstract,
            "keywords": "; ".join(keywords),
            "status": "valid",
            "pdf_filename": pdf_filename_disk,
            "text_path": str(text_path.relative_to(REPO)),
            "extraction_ok": extraction_ok,
            "note": "",
        })

    # ── Write metadata CSV ──────────────────────────────────────────────
    fieldnames = ["title", "authors", "year", "doi", "item_type", "abstract",
                  "keywords", "status", "pdf_filename", "text_path",
                  "extraction_ok", "note"]
    with open(METADATA_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(results)

    # ── Write log ───────────────────────────────────────────────────────
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "pipeline": "pipeline_snowball_extract",
        "source": str(EXPORT_DIR),
        "ris_file": RIS_FILE.name,
        "stats": stats,
        "metadata_path": str(METADATA_PATH.relative_to(REPO)),
        "pdf_dir": str(PDF_DIR.relative_to(REPO)),
        "text_dir": str(TEXT_DIR.relative_to(REPO)),
    }
    with open(LOG_PATH, "w") as f:
        json.dump(log_data, f, indent=2)

    # ── Summary ─────────────────────────────────────────────────────────
    log("=" * 60)
    log("SUMMARY")
    log(f"  Total RIS records:      {stats['total']}")
    log(f"  PDFs copied:            {stats['valid']}")
    log(f"  No PDF found:           {stats['no_pdf']}")
    log(f"  Text extracted OK:      {stats['extraction_ok']}")
    log(f"  Extraction failed:      {stats['extraction_failed']}")
    if stats["errors"]:
        log(f"  Errors ({len(stats['errors'])}):")
        for e in stats["errors"][:5]:
            log(f"    - {e}")
    log(f"\n  Metadata: {METADATA_PATH}")
    log(f"  PDFs:     {PDF_DIR}/")
    log(f"  Texts:    {TEXT_DIR}/")
    log(f"  Run log:  {RUNLOG}")
    log("=" * 60)


if __name__ == "__main__":
    main()
