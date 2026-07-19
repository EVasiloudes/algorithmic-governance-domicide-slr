#!/usr/bin/env python3
"""Dedup snowball candidates against the existing 874-record screened corpus.
Match: DOI (normalised) -> normalised title (+year guard).
"""
import csv, json, re, os

OUT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(OUT, "../../.."))
MASTER = os.path.join(REPO, "Diss_Methods_Data/Literature [.RIS]/deduplicated/screening_master.csv")

def norm_doi(d):
    if not d: return ""
    d = d.strip().lower()
    d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d)
    return d

def norm_title(t):
    if not t: return ""
    t = t.lower()
    t = re.sub(r"<[^>]+>", " ", t)          # strip html tags
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

# Load existing corpus
corpus_dois, corpus_titles = {}, {}
with open(MASTER, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        d = norm_doi(row.get("doi"))
        t = norm_title(row.get("title"))
        if d: corpus_dois[d] = row["id"]
        if t: corpus_titles[t] = row["id"]

with open(os.path.join(OUT, "candidates.json")) as f:
    data = json.load(f)
records = data["records"]

kept, dropped = [], []
for rec in records:
    d, t = norm_doi(rec.get("doi")), norm_title(rec.get("title"))
    hit = None
    if d and d in corpus_dois: hit = ("doi", corpus_dois[d])
    elif t and t in corpus_titles: hit = ("title", corpus_titles[t])
    if hit:
        rec["dup_of_corpus_id"] = hit[1]
        rec["dup_method"] = hit[0]
        dropped.append(rec)
    else:
        kept.append(rec)

with open(os.path.join(OUT, "candidates_deduped.json"), "w") as f:
    json.dump({"summary": data["summary"],
               "n_candidates": len(records),
               "n_dropped_as_duplicates": len(dropped),
               "n_kept": len(kept),
               "kept": kept,
               "dropped": dropped}, f, indent=1)

print(f"candidates: {len(records)}")
print(f"duplicates of existing corpus: {len(dropped)}  (doi: {sum(1 for r in dropped if r['dup_method']=='doi')}, title: {sum(1 for r in dropped if r['dup_method']=='title')})")
print(f"NEW records to screen: {len(kept)}")
# quick triage stats
no_abs = sum(1 for r in kept if not r.get("abstract"))
print(f"  of which lacking abstract: {no_abs}")
by_via = {}
for r in kept:
    for v in r["via"]: by_via[v] = by_via.get(v, 0) + 1
for k, v in sorted(by_via.items()): print(f"  via {k}: {v}")
