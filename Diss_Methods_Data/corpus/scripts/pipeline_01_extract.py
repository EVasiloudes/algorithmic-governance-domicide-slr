#!/usr/bin/env python3
"""
pipeline_01_extract.py — Zotero → PDF dump → text extraction → metadata CSV

Pipeline step 1/3. Writes a run.log alongside the output directories so you
can tail -f it while it runs.

Usage:
    python3 Diss_Methods_Data/corpus/scripts/pipeline_01_extract.py
"""

import os, json, csv, sys, time
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(line_buffering=True)

REPO = Path("/Users/eliasvasnic/Obsidian Vaults/Elias Vasnic Obsidian Vault/Atoms/Public_Policy_&_Management/Courses/MSc PPM Dissertation - Repo")
CORPUS = REPO / "Diss_Methods_Data" / "corpus"
PDF_DIR = CORPUS / "pdfs"
TEXT_DIR = CORPUS / "text"
SCRIPTS_DIR = CORPUS / "scripts"
METADATA_PATH = CORPUS / "metadata.csv"
LOG_PATH = CORPUS / "extraction_log.json"
RUNLOG = CORPUS / "run.log"

COLLECTION_NAME = "SLR-INCLUDED-RECORDS"

def log(msg):
    """Write to both stdout and run.log."""
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(RUNLOG, "a") as f:
        f.write(line + "\n")

def connect_zotero():
    from pyzotero import Zotero
    zot = Zotero(0, 'user', local=True)
    zot.top(limit=1)  # verify
    return zot

def find_collection(zot, name):
    for c in zot.collections():
        if c['data']['name'] == name:
            return c['data']['key']
    raise ValueError(f"Collection '{name}' not found")

def sanitise_filename(title):
    safe = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in title)
    return (safe.strip().replace(' ', '_')[:200]) or "untitled"

def main():
    log("=" * 60)
    log("SLR Pipeline 01: Zotero → PDF Dump → Text Extraction")
    log(f"Started: {datetime.now().isoformat()}")
    log("=" * 60)

    for d in [PDF_DIR, TEXT_DIR, SCRIPTS_DIR]:
        d.mkdir(parents=True, exist_ok=True)
    # Clear old run log
    RUNLOG.write_text("")

    log("Connecting to Zotero...")
    zot = connect_zotero()
    log("✓ Connected")

    coll_key = find_collection(zot, COLLECTION_NAME)
    log(f"✓ Collection: {COLLECTION_NAME} (key: {coll_key})")

    log("Fetching references...")
    refs = zot.collection_items_top(coll_key)
    log(f"✓ {len(refs)} references")

    stats = {'total': len(refs), 'valid': 0, 'removed': 0, 'no_pdf': 0,
             'extraction_ok': 0, 'extraction_failed': 0, 'errors': []}
    results = []

    for idx, ref in enumerate(refs, 1):
        d = ref['data']
        key = d['key']
        title = d.get('title', 'UNTITLED')
        date = d.get('date', '')
        doi = d.get('DOI', '')
        item_type = d['itemType']

        log(f"[{idx:3d}/{len(refs)}] {title[:80]}")

        children = zot.children(key)

        # Check removal notes + provenance
        removal_reason = None
        provenance = None
        for child in children:
            cd = child['data']
            if cd['itemType'] == 'note':
                nt = cd['note'].lower()
                if 'remove' in nt or 'removed' in nt:
                    removal_reason = cd['note']
                if 'provenance' in nt:
                    if 'policy commons' in nt:
                        provenance = 'policy_commons'
                    elif 'web of science' in nt:
                        provenance = 'wos'
                    elif 'scopus' in nt:
                        provenance = 'scopus'

        if removal_reason:
            stats['removed'] += 1
            results.append({'zotero_key': key, 'title': title, 'doi': doi, 'date': date,
                           'item_type': item_type, 'provenance': provenance, 'status': 'removed',
                           'has_pdf': False, 'pdf_key': None, 'pdf_filename': None,
                           'text_path': None, 'extraction_ok': None, 'note': removal_reason[:300]})
            log("  ⛔ REMOVED")
            continue

        # Find PDF attachment
        pdf_key = None
        pdf_filename = None
        for child in children:
            cd = child['data']
            if (cd['itemType'] == 'attachment'
                and cd.get('contentType') == 'application/pdf'
                and cd.get('linkMode') == 'imported_file'):
                pdf_key = cd['key']
                pdf_filename = cd.get('filename', 'unknown.pdf')
                break

        if not pdf_key:
            stats['no_pdf'] += 1
            results.append({'zotero_key': key, 'title': title, 'doi': doi, 'date': date,
                           'item_type': item_type, 'provenance': provenance, 'status': 'no_pdf',
                           'has_pdf': False, 'pdf_key': None, 'pdf_filename': None,
                           'text_path': None, 'extraction_ok': False, 'note': 'No PDF attachment'})
            log("  📄 NO PDF")
            continue

        # Download PDF
        safe_name = sanitise_filename(title)
        pdf_filename_disk = f"{safe_name}.pdf"
        pdf_path = PDF_DIR / pdf_filename_disk

        try:
            zot.dump(pdf_key, pdf_filename_disk, str(PDF_DIR))
            stats['valid'] += 1
        except Exception as e:
            stats['errors'].append(f"{key}: download failed: {e}")
            results.append({'zotero_key': key, 'title': title, 'doi': doi, 'date': date,
                           'item_type': item_type, 'provenance': provenance, 'status': 'download_failed',
                           'has_pdf': True, 'pdf_key': pdf_key, 'pdf_filename': pdf_filename,
                           'text_path': None, 'extraction_ok': False, 'note': f'download failed: {e}'})
            log(f"  ✖ DOWNLOAD FAILED: {e}")
            continue

        # Extract text
        text_path = TEXT_DIR / f"{safe_name}.txt"
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
                # Try PyPDF2 as fallback
                try:
                    from PyPDF2 import PdfReader
                    reader = PdfReader(str(pdf_path))
                    full_text = "\n\n".join(p.extract_text() or "" for p in reader.pages)
                except ImportError:
                    pass

            text_path.write_text(full_text, encoding='utf-8')
            stats['extraction_ok'] += 1
            log(f"  ✓ PDF + {len(full_text):,} chars → text")
        except Exception as e:
            stats['extraction_failed'] += 1
            stats['errors'].append(f"{key}: extraction failed: {e}")
            log(f"  ✖ EXTRACTION FAILED: {e}")
            full_text = ""

        results.append({'zotero_key': key, 'title': title, 'doi': doi, 'date': date,
                       'item_type': item_type, 'provenance': provenance, 'status': 'valid',
                       'has_pdf': True, 'pdf_key': pdf_key, 'pdf_filename': pdf_filename,
                       'text_path': str(text_path.relative_to(REPO)),
                       'extraction_ok': len(full_text.strip()) >= 50, 'note': ''})

    # Write metadata CSV
    fieldnames = ['zotero_key', 'title', 'doi', 'date', 'item_type', 'provenance',
                  'status', 'has_pdf', 'pdf_key', 'pdf_filename', 'text_path', 'extraction_ok', 'note']
    with open(METADATA_PATH, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(results)

    # Write log
    log_data = {'timestamp': datetime.now().isoformat(), 'collection': COLLECTION_NAME,
                'stats': stats, 'metadata_path': str(METADATA_PATH.relative_to(REPO)),
                'pdf_dir': str(PDF_DIR.relative_to(REPO)), 'text_dir': str(TEXT_DIR.relative_to(REPO))}
    with open(LOG_PATH, 'w') as f:
        json.dump(log_data, f, indent=2)

    log("=" * 60)
    log("SUMMARY")
    log(f"  Total references:       {stats['total']}")
    log(f"  Valid (with PDF):       {stats['valid']}")
    log(f"  Removed:                {stats['removed']}")
    log(f"  No PDF:                 {stats['no_pdf']}")
    log(f"  Text extracted OK:      {stats['extraction_ok']}")
    log(f"  Extraction failed:      {stats['extraction_failed']}")
    if stats['errors']:
        log(f"  Errors ({len(stats['errors'])}):")
        for e in stats['errors'][:5]:
            log(f"    - {e}")
    log(f"\n  Metadata: {METADATA_PATH}")
    log(f"  PDFs:     {PDF_DIR}/")
    log(f"  Texts:    {TEXT_DIR}/")
    log(f"  Run log:  {RUNLOG}")

if __name__ == '__main__':
    main()