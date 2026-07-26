#!/usr/bin/env python3
"""Enrich abstracts fast — one-pass, no-retry, save-on-each-batch.

Phase 1: Springer META → 10.1007/ DOIs
Phase 2: OpenAlex     → remaining DOIs
"""
import json, urllib.request, urllib.parse, time, os, sys, ssl
import certifi

CUR = os.path.dirname(os.path.abspath(__file__))
CTX = ssl.create_default_context(cafile=certifi.where())
MAILTO = "elias@densetheory.cc"

def _load_env(key_name):
    try:
        for line in open(os.path.join(CUR, ".env")):
            if line.startswith(f"{key_name}="):
                return line.strip().split("=", 1)[1]
    except OSError: pass
    return ""

OPENALEX_KEY = _load_env("OPENALEX_API_KEY")
SPRINGER_KEY = "a9480da046aa58aab43bc4ed7af35ef3"

def http_get(url: str, timeout=20) -> dict | None:
    """One-shot HTTP GET, return parsed JSON or None on any error."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "SLR-Enrich"})
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
            return json.load(r)
    except Exception:
        return None


def springer_abstract(doi_raw: str) -> str | None:
    doi = doi_raw.replace("https://doi.org/", "")
    url = (f"https://api.springernature.com/meta/v2/json"
           f"?q=doi:{urllib.parse.quote(doi)}"
           f"&api_key={SPRINGER_KEY}")
    data = http_get(url)
    if not data: return None
    records = data.get("records", [])
    if not records: return None
    a = records[0].get("abstract", "")
    return a if len(a) >= 50 else None


def openalex_abstract(doi_raw: str) -> str | None:
    doi = doi_raw.replace("https://doi.org/", "")
    url = (f"https://api.openalex.org/works/doi:{urllib.parse.quote(doi)}"
           f"?select=abstract_inverted_index&mailto={MAILTO}")
    if OPENALEX_KEY:
        url += f"&api_key={OPENALEX_KEY}"
    data = http_get(url, timeout=15)
    if not data: return None
    aii = data.get("abstract_inverted_index")
    if not aii: return None
    # Reconstruct
    pos2word = {}
    for word, positions in aii.items():
        for p in positions:
            pos2word[p] = word
    text = " ".join(pos2word[i] for i in sorted(pos2word.keys()))
    return text if len(text) >= 50 else None


def save(data, label=""):
    path = os.path.join(CUR, "candidates_enriched.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=1)
    if label:
        print(f"  [saved {label}]")


def main():
    print("Loading candidates_deduped.json ...")
    with open(os.path.join(CUR, "candidates_deduped.json")) as f:
        data = json.load(f)

    kept = data["kept"]
    no_abs = [r for r in kept if len(r.get("abstract") or "") < 200]
    springer = [r for r in no_abs if r.get("doi") and "10.1007/" in r["doi"]]
    others   = [r for r in no_abs if r.get("doi") and "10.1007/" not in r["doi"]]
    no_doi   = [r for r in no_abs if not r.get("doi")]

    print(f"No abstract: {len(no_abs)} → Springer: {len(springer)} | Others: {len(others)} | No DOI: {len(no_doi)}")

    # --- Phase 1: Springer ---
    n_springer = 0
    batch = []
    for i, r in enumerate(springer):
        doi = r.get("doi", "")
        abstract = springer_abstract(doi)
        if abstract:
            r["abstract"] = abstract
            r["abstract_source"] = "springer-meta"
            n_springer += 1
        batch.append(r)
        
        if (i + 1) % 25 == 0 or i == len(springer) - 1:
            eta = f"{i+1}/{len(springer)}"
            print(f"  Springer: {eta} enriched={n_springer}")
            save(data, f"springer-{i+1}")
        time.sleep(0.18)

    print(f"\nSpringer done: {n_springer}/{len(springer)} enriched")

    # --- Phase 2: OpenAlex on remaining no-abstract ---
    still = [r for r in kept if len(r.get("abstract") or "") < 200 and r.get("doi")]
    print(f"\nPhase 2: OpenAlex re-scan on {len(still)} remaining")
    n_oa = 0
    
    for i, r in enumerate(still):
        doi = r.get("doi", "")
        abstract = openalex_abstract(doi)
        if abstract:
            r["abstract"] = abstract
            r["abstract_source"] = "openalex-rescan"
            n_oa += 1
        
        if (i + 1) % 50 == 0 or i == len(still) - 1:
            print(f"  OpenAlex: {i+1}/{len(still)} enriched={n_oa}")
            save(data, f"oa-{i+1}")
        time.sleep(0.12)

    # --- Summary ---
    final_no_abs = sum(1 for r in kept if len(r.get("abstract") or "") < 200)
    print(f"\n{'='*55}")
    print(f"  Springer enriched:  {n_springer}")
    print(f"  OpenAlex enriched:  {n_oa}")
    print(f"  Total enriched:     {n_springer + n_oa}")
    print(f"  Was no-abstract:    {len(no_abs)}")
    print(f"  Still no-abstract:  {final_no_abs}")
    
    save(data, "final")
    print(f"Saved candidates_enriched.json")


if __name__ == "__main__":
    main()