#!/usr/bin/env python3
"""Reprocess ALL Scopus RIS exports from source: parse, union-dedup against
corpus + OpenAlex candidates + each other, then screen any record not already
screened (parallel, resumable via scopus_screening_all.csv).
Usage: python3 screen_scopus_all.py ris1 ris2 [ris3 ...]
"""
import os, re, csv, json, sys, time, threading
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT = os.path.dirname(os.path.abspath(__file__))
TAG_RE = re.compile(r"^([A-Z0-9]{2})  - ?(.*)$")
CSV_PATH = os.path.join(OUT, "scopus_screening_all.csv")

def parse_ris(path):
    recs, cur = [], {}
    for line in open(path, encoding="utf-8"):
        m = TAG_RE.match(line.rstrip("\n"))
        if not m:
            continue
        tag, val = m.group(1), m.group(2)
        if tag == "TY":
            cur = {"TY": val}
        elif tag == "ER":
            recs.append(cur)
            cur = {}
        else:
            cur[tag] = val if tag not in cur else cur[tag] + "; " + val
    return recs

def norm_title(t):
    t = (t or "").lower()
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()

def norm_doi(d):
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", (d or "").strip().lower())

def main():
    ris_files = sys.argv[1:]
    corpus_t, corpus_d = set(), set()
    with open(os.path.join(OUT, "../../Literature [.RIS]/deduplicated/screening_master.csv"),
              newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("doi"): corpus_d.add(norm_doi(row["doi"]))
            if row.get("title"): corpus_t.add(norm_title(row["title"]))

    cand = json.load(open(os.path.join(OUT, "candidates.json")))["records"]
    cand_t = {norm_title(r["title"]) for r in cand if r.get("title")}
    cand_d = {norm_doi(r["doi"]) for r in cand if r.get("doi")}

    # union of all scopus records, within-union dedup
    seen_t, seen_d = set(), set()
    union = []
    total_raw = 0
    for path in ris_files:
        recs = parse_ris(path)
        total_raw += len(recs)
        for r in recs:
            t, d = norm_title(r.get("TI")), norm_doi(r.get("DO"))
            if (d and d in seen_d) or (t and t in seen_t):
                continue
            seen_t.add(t); seen_d.add(d)
            r["_src"] = os.path.basename(path)
            union.append(r)

    n_corpus_dup = n_cand_dup = 0
    net_new = []
    for r in union:
        t, d = norm_title(r.get("TI")), norm_doi(r.get("DO"))
        if (d and d in corpus_d) or (t and t in corpus_t):
            n_corpus_dup += 1
        elif (d and d in cand_d) or (t and t in cand_t):
            n_cand_dup += 1
        else:
            net_new.append(r)

    print(f"raw: {total_raw} | union unique: {len(union)} | corpus-dups: {n_corpus_dup} | openalex-dups: {n_cand_dup} | NET-NEW: {len(net_new)}")

    # already screened?
    done = set()
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                done.add(norm_title(row["title"]))
    todo = [r for r in net_new if norm_title(r.get("TI")) not in done]
    print(f"already screened: {len(net_new) - len(todo)} | to screen now: {len(todo)}")

    if todo:
        sys.path.insert(0, OUT)
        from screen_snowball import call_model, MODEL, FALLBACK_MODEL, MIN_ABS
        write_header = not os.path.exists(CSV_PATH)
        lock = threading.Lock()

        def classify(r):
            title = r.get("TI", "")
            abstract = r.get("AB", "")
            if len(abstract) < MIN_ABS:
                return [title, r.get("PY", ""), r.get("DO", ""), r.get("T2", ""),
                        r["_src"], "triage_no_abstract", "Exclude", "triage", ""]
            text = f"Title: {title}\n\nAbstract: {abstract[:6000]}"
            verdict, raw = call_model(MODEL, text)
            model = MODEL
            if verdict is None:
                verdict, raw = call_model(FALLBACK_MODEL, text)
                model = FALLBACK_MODEL
            return [title, r.get("PY", ""), r.get("DO", ""), r.get("T2", ""),
                    r["_src"], "screened", verdict, model, raw[:500]]

        with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if write_header:
                w.writerow(["title", "year", "doi", "source_journal", "src_file",
                            "triage", "verdict", "model", "raw_response"])
            n = 0
            with ThreadPoolExecutor(max_workers=4) as ex:
                futs = {ex.submit(classify, r): r for r in todo}
                for fut in as_completed(futs):
                    row = fut.result()
                    with lock:
                        w.writerow(row)
                        f.flush()
                    n += 1
                    if n % 20 == 0:
                        print(f"  {n}/{len(todo)}", flush=True)

    # final tally
    from collections import Counter
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        c = Counter(row["verdict"] for row in csv.DictReader(f))
    print("SCOPUS SCREENING TOTALS:", dict(c))

if __name__ == "__main__":
    main()
