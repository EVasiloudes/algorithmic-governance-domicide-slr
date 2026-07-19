#!/usr/bin/env python3
"""Second-pass retrieval via Unpaywall for records where OpenAlex OA failed.
Reads retrieval/retrieval_log.json, tries Unpaywall for non-ok records with DOIs,
downloads PDFs, extracts text. Updates retrieval_log.json statuses.
"""
import os, json, time, subprocess, re
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(OUT, "retrieval", "pdfs")
TXT_DIR = os.path.join(OUT, "retrieval", "text")
LOG = os.path.join(OUT, "retrieval", "retrieval_log.json")
EMAIL = "liase@openclaw.local"

def fetch(url, binary=False, timeout=90):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (snowball-unpaywall)"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read() if binary else json.load(r)
        except Exception:
            if attempt == 2:
                return None
            time.sleep(2 ** attempt * 3)

def safe_name(wid, title):
    t = re.sub(r"[^A-Za-z0-9]+", "_", (title or "")[:60]).strip("_")
    return f"{wid}_{t}"

def process(rec):
    doi = rec.get("doi")
    if not doi:
        rec["status"] = "no_doi"
        return rec
    d = fetch(f"https://api.unpaywall.org/v2/{doi}?email={EMAIL}")
    if not d:
        rec["status"] = "unpaywall_error"
        return rec
    loc = d.get("best_oa_location") or {}
    url = loc.get("url_for_pdf")
    if not url:
        # try other oa locations
        for l in d.get("oa_locations") or []:
            if l.get("url_for_pdf"):
                url = l["url_for_pdf"]
                break
    if not url:
        rec["status"] = "no_oa_pdf_unpaywall"
        return rec
    wid = rec["openalex_id"].rsplit("/", 1)[-1]
    name = safe_name(wid, rec["title"])
    pdf_path = os.path.join(PDF_DIR, name + ".pdf")
    txt_path = os.path.join(TXT_DIR, name + ".txt")
    data = fetch(url, binary=True, timeout=120)
    if not data or data[:4] != b"%PDF":
        rec["status"] = "unpaywall_download_failed"
        return rec
    with open(pdf_path, "wb") as f:
        f.write(data)
    try:
        r = subprocess.run(["pdftotext", "-q", pdf_path, txt_path],
                           capture_output=True, timeout=120)
        if r.returncode != 0 or not os.path.exists(txt_path):
            raise RuntimeError("pdftotext failed")
    except Exception as e:
        rec["status"] = f"extract_failed: {e}"
        return rec
    rec["status"] = "ok_unpaywall"
    rec["text_chars"] = os.path.getsize(txt_path)
    return rec

def main():
    with open(LOG) as f:
        log = json.load(f)
    todo = [r for r in log["records"] if r["status"] != "ok"]
    print(f"second pass on {len(todo)} records")
    done = 0
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = [ex.submit(process, r) for r in todo]
        for fut in as_completed(futs):
            done += 1
            if done % 20 == 0:
                print(f"  {done}/{len(todo)}", flush=True)
    from collections import Counter
    c = Counter(r["status"] for r in log["records"])
    print(dict(c))
    log["status_counts"] = dict(c)
    with open(LOG, "w") as f:
        json.dump(log, f, indent=1)

if __name__ == "__main__":
    main()
