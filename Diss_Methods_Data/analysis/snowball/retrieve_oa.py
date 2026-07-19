#!/usr/bin/env python3
"""Retrieve open-access full texts for snowball Include records.
Fetches OA locations from OpenAlex, downloads PDFs, extracts text (pdfplumber).
Output: retrieval/pdfs/, retrieval/text/, retrieval/retrieval_log.json
"""
import os, csv, json, time, sys, re
import urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(OUT, "retrieval", "pdfs")
TXT_DIR = os.path.join(OUT, "retrieval", "text")
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(TXT_DIR, exist_ok=True)

def _load_key():
    try:
        for line in open(os.path.join(OUT, ".env")):
            if line.startswith("OPENALEX_API_KEY="):
                return line.strip().split("=", 1)[1]
    except OSError:
        pass
    return ""
API_KEY = _load_key()

FIELDS = "id,doi,display_name,publication_year,open_access,best_oa_location,locations"

def oa_get(url, binary=False, timeout=90):
    if API_KEY and "api.openalex.org" in url:
        sep = "&" if "?" in url else "?"
        url += f"{sep}api_key={API_KEY}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (snowball-retrieval)"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read() if binary else json.load(r)
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt * 3)

def safe_name(wid, title):
    t = re.sub(r"[^A-Za-z0-9]+", "_", (title or "")[:60]).strip("_")
    return f"{wid}_{t}"

def process(rec):
    wid = rec["openalex_id"].rsplit("/", 1)[-1]
    log = {"openalex_id": rec["openalex_id"], "title": rec["title"], "doi": rec.get("doi")}
    try:
        w = oa_get(f"https://api.openalex.org/works/{wid}?select={FIELDS}")
        log["is_oa"] = w.get("open_access", {}).get("is_oa", False)
        # collect candidate pdf urls: best_oa first, then all OA locations
        urls = []
        boa = w.get("best_oa_location") or {}
        if boa.get("pdf_url"): urls.append(boa["pdf_url"])
        for loc in w.get("locations") or []:
            if loc.get("is_oa") and loc.get("pdf_url") and loc["pdf_url"] not in urls:
                urls.append(loc["pdf_url"])
        log["pdf_urls_tried"] = len(urls)
        if not urls:
            log["status"] = "no_oa_pdf"
            return log
        name = safe_name(wid, rec["title"])
        pdf_path = os.path.join(PDF_DIR, name + ".pdf")
        if not os.path.exists(pdf_path):
            data = None
            for u in urls:
                try:
                    data = oa_get(u, binary=True, timeout=120)
                    if data and data[:4] == b"%PDF":
                        break
                    data = None
                except Exception:
                    continue
            if not data:
                log["status"] = "download_failed"
                return log
            if len(data) > 60 * 1024 * 1024:
                log["status"] = "too_large"
                return log
            with open(pdf_path, "wb") as f:
                f.write(data)
        # extract text (pdftotext primary, pypdf fallback)
        txt_path = os.path.join(TXT_DIR, name + ".txt")
        if not os.path.exists(txt_path):
            try:
                import subprocess
                r = subprocess.run(["pdftotext", "-q", pdf_path, txt_path],
                                   capture_output=True, timeout=120)
                if r.returncode != 0 or not os.path.exists(txt_path):
                    raise RuntimeError("pdftotext failed, trying pypdf")
            except Exception:
                try:
                    from pypdf import PdfReader
                    text = "\n\n".join((p.extract_text() or "") for p in PdfReader(pdf_path).pages)
                    with open(txt_path, "w", encoding="utf-8") as f:
                        f.write(text)
                except Exception as e:
                    log["status"] = f"extract_failed: {e}"
                    return log
            try:
                log["text_chars"] = os.path.getsize(txt_path)
            except OSError:
                log["text_chars"] = 0
        log["status"] = "ok"
        return log
    except Exception as e:
        log["status"] = f"error: {e}"
        return log

def main():
    rows = list(csv.DictReader(open(os.path.join(OUT, "snowball_screening.csv"))))
    includes = [r for r in rows if r["verdict"] == "Include"]
    print(f"includes: {len(includes)}")
    logs = []
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(process, r): r for r in includes}
        done = 0
        for fut in as_completed(futs):
            logs.append(fut.result())
            done += 1
            if done % 20 == 0:
                print(f"  {done}/{len(includes)}", flush=True)
    from collections import Counter
    c = Counter(l["status"] for l in logs)
    print(dict(c))
    with open(os.path.join(OUT, "retrieval", "retrieval_log.json"), "w") as f:
        json.dump({"n_includes": len(includes), "status_counts": dict(c), "records": logs}, f, indent=1)

if __name__ == "__main__":
    main()
