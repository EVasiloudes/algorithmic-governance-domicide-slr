#!/usr/bin/env python3
"""Retry error rows in scopus_screening_all.csv once."""
import csv, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from screen_snowball import call_model, MODEL, FALLBACK_MODEL
from parse_scopus_ris import parse_ris
import glob

OUT = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(OUT, "scopus_screening_all.csv")
rows = list(csv.DictReader(open(path)))

# build title -> abstract lookup from all RIS files
abs_map = {}
for ris in glob.glob("/data/data/com.termux/files/home/.openclaw/media/inbound/scopus_export_*.ris"):
    for r in parse_ris(ris):
        abs_map[(r.get("TI") or "").strip()] = r.get("AB") or ""

fixed = 0
for row in rows:
    if row["verdict"] != "error":
        continue
    abstract = abs_map.get(row["title"].strip(), "")
    if len(abstract) < 200:
        row["verdict"], row["model"], row["raw_response"] = "Exclude", "triage", "triage_no_abstract_on_retry"
        fixed += 1
        continue
    text = f"Title: {row['title']}\n\nAbstract: {abstract[:6000]}"
    verdict, raw = call_model(MODEL, text)
    model = MODEL
    if verdict is None:
        verdict, raw = call_model(FALLBACK_MODEL, text)
        model = FALLBACK_MODEL
    if verdict != "error":
        row["verdict"], row["model"], row["raw_response"] = verdict, model, raw[:500]
        fixed += 1
        print(f"fixed -> [{verdict}] {row['title'][:60]}")

with open(path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print(f"fixed {fixed}")
