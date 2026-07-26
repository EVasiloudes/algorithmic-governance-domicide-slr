#!/usr/bin/env python3
"""Springer-only abstract enrichment. Slow, self-throttling — resumes from
candidates_enriched.json. Waits 5s between calls to stay under rate limit."""
import json, urllib.request, urllib.parse, time, os, sys, ssl
import certifi

CUR = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context(cafile=certifi.where())
KEY = "a9480da046aa58aab43bc4ed7af35ef3"

def springer_abstract(doi_raw: str) -> str | None:
    doi = doi_raw.replace("https://doi.org/", "")
    url = (f"https://api.springernature.com/meta/v2/json"
           f"?q=doi:{urllib.parse.quote(doi)}&api_key={KEY}")
    req = urllib.request.Request(url, headers={"User-Agent": "SLR-Springer/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print(f"  RATE LIMITED at {time.strftime('%H:%M:%S')} — waiting 60s...", flush=True)
            time.sleep(60)
            return None  # skip this one, try next
        return None
    except Exception:
        return None
    records = data.get("records", [])
    if not records: return None
    a = records[0].get("abstract", "")
    return a if len(a) >= 50 else None

def main():
    with open(f"{CUR}/candidates_enriched.json") as f:
        data = json.load(f)
    
    kept = data["kept"]
    springers = [r for r in kept if r.get("doi") and "10.1007/" in r["doi"]
                 and (not r.get("abstract") or len(r["abstract"]) < 200)]
    
    if not springers:
        print("All Springer records already have abstracts!")
        return
    
    print(f"Springer records needing abstracts: {len(springers)}")
    
    enriched = 0
    rate_limited = 0
    for i, r in enumerate(springers):
        doi = r.get("doi", "")
        abstract = springer_abstract(doi)
        if abstract:
            r["abstract"] = abstract
            r["abstract_source"] = "springer-meta"
            enriched += 1
            rate_limited = 0
        elif abstract is None and rate_limited < 3:
            # Try again with increasing delay
            rate_limited += 1
            time.sleep(2 ** rate_limited)
            abstract = springer_abstract(doi)
            if abstract:
                r["abstract"] = abstract
                r["abstract_source"] = "springer-meta"
                enriched += 1
                rate_limited = 0
        
        if (i + 1) % 10 == 0:
            remaining = sum(1 for r in kept if r.get("doi") and "10.1007/" in r["doi"]
                          and (not r.get("abstract") or len(r["abstract"]) < 200))
            print(f"  {i+1}/{len(springers)} enriched={enriched} remaining={remaining}", flush=True)
        
        time.sleep(1.2)  # ~50 calls/minute, well under limit
    
    final = sum(1 for r in kept if (not r.get("abstract") or len(r["abstract"]) < 200))
    print(f"\nSpringer enriched this run: {enriched}")
    print(f"Total still no-abstract: {final}")
    
    with open(f"{CUR}/candidates_enriched.json", "w") as f:
        json.dump(data, f, indent=1)
    print("Saved candidates_enriched.json")

if __name__ == "__main__":
    main()
