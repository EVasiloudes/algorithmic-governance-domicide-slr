#!/usr/bin/env python3
"""Snowball screening: classify deduped candidates against the SLR inclusion
criteria using the SAME system prompt, model, and temperature as the main
title/abstract screening pipeline (ai_screen.py).

Input:  candidates_deduped.json (kept records)
Output: snowball_screening.csv  (resumable — skips rows already present)

Triage: records with no/vestigial abstract (<200 chars) are excluded at triage,
mirroring the main pipeline's 77-record no-abstract exclusion.
"""
import os, csv, json, time, re, sys, threading
import urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

WORKERS = 4
write_lock = threading.Lock()

OUT = os.path.dirname(os.path.abspath(__file__))
API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-v4-flash"
FALLBACK_MODEL = "deepseek/deepseek-chat"
MIN_ABS = 200

SYSTEM_PROMPT = open(os.path.join(OUT, "screening_prompt.txt")).read()

def call_model(model, text, retries=3):
    payload = {"model": model,
               "messages": [{"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": text}],
               "temperature": 0.0, "max_tokens": 256, "top_p": 1.0}
    req = urllib.request.Request(OPENROUTER_URL,
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {API_KEY}",
                 "Content-Type": "application/json",
                 "X-Title": "SLR-Snowball-Screener"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                data = json.load(r)
            msg = data["choices"][0]["message"]
            txt = (msg.get("content") or msg.get("reasoning_content") or "").strip()
            if not txt:
                raise ValueError("empty response")
            m = re.search(r'\b(Include|Exclude|Maybe)\b', txt, re.IGNORECASE)
            return (m.group(1).capitalize() if m else "Maybe"), txt
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None, "404"
            wait = 2 ** attempt * 3
            print(f"  HTTP {e.code}, retry in {wait}s", file=sys.stderr)
            time.sleep(wait)
        except Exception as e:
            wait = 2 ** attempt * 3
            print(f"  err {e}, retry in {wait}s", file=sys.stderr)
            time.sleep(wait)
    return "error", "retries exhausted"

def main():
    if not API_KEY:
        sys.exit("OPENROUTER_API_KEY not set")
    with open(os.path.join(OUT, "candidates_deduped.json")) as f:
        kept = json.load(f)["kept"]

    csv_path = os.path.join(OUT, "snowball_screening.csv")
    done = set()
    if os.path.exists(csv_path):
        with open(csv_path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                done.add(row["openalex_id"])
    write_header = not os.path.exists(csv_path)

    triage_excl = [r for r in kept if len(r.get("abstract") or "") < MIN_ABS]
    to_screen = [r for r in kept if len(r.get("abstract") or "") >= MIN_ABS]
    print(f"kept: {len(kept)} | triage-excluded (no/short abstract): {len(triage_excl)} | to screen: {len(to_screen)} | already done: {len(done)}")

    remaining = [r for r in to_screen if r["openalex_id"] not in done]

    def classify(r):
        text = f"Title: {r['title']}\n\nAbstract: {r['abstract'][:6000]}"
        verdict, raw = call_model(MODEL, text)
        model_used = MODEL
        if verdict is None:  # 404 -> fallback
            verdict, raw = call_model(FALLBACK_MODEL, text)
            model_used = FALLBACK_MODEL
        return [r["openalex_id"], r.get("doi") or "", r["title"], r.get("year"),
                r.get("type"), r.get("first_author"), r.get("source"),
                "|".join(r["via"]), "screened", verdict, model_used, raw[:500]]

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(["openalex_id", "doi", "title", "year", "type",
                        "first_author", "source", "via", "triage", "verdict", "model", "raw_response"])
        n = 0
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            futures = {ex.submit(classify, r): r for r in remaining}
            for fut in as_completed(futures):
                row = fut.result()
                with write_lock:
                    w.writerow(row)
                    f.flush()
                n += 1
                if n % 50 == 0:
                    print(f"  progress: {n}/{len(remaining)} screened this run", flush=True)
        # log triage exclusions
        for r in triage_excl:
            if r["openalex_id"] in done:
                continue
            w.writerow([r["openalex_id"], r.get("doi") or "", r["title"], r.get("year"),
                        r.get("type"), r.get("first_author"), r.get("source"),
                        "|".join(r["via"]), "excluded_no_abstract", "Exclude", "triage", ""])
        f.flush()
    print("DONE")

if __name__ == "__main__":
    main()
