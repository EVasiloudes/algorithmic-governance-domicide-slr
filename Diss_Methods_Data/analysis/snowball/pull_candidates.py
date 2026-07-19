#!/usr/bin/env python3
"""Snowball iteration 1: backward + forward citation chaining via OpenAlex.
Anchors: Graham 2006, Kitchin 2014, Weizman 2007, Michael 2007.
Protocol filters (same as main searches): 1990-2025, English, article/chapter/review.
"""
import json, time, urllib.request, urllib.parse, sys, os

MAILTO = "liase@openclaw.local"
BASE = "https://api.openalex.org/works"
OUT = os.path.dirname(os.path.abspath(__file__))

def _load_key():
    try:
        for line in open(os.path.join(OUT, ".env")):
            if line.startswith("OPENALEX_API_KEY="):
                return line.strip().split("=", 1)[1]
    except OSError:
        pass
    return ""

API_KEY = _load_key()

def get(url):
    sep = "&" if "?" in url else "?"
    url = f"{url}{sep}mailto={MAILTO}"
    if API_KEY:
        url += f"&api_key={API_KEY}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (snowball-slr)"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            wait = 2 ** attempt * 5
            print(f"  retry {attempt+1} after {e} (wait {wait}s)", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(f"failed: {url}")

def resolve_by_doi(doi):
    return get(f"{BASE}/doi:{urllib.parse.quote(doi)}")

def resolve_by_title(title, year=None):
    q = urllib.parse.quote(title)
    filt = f"publication_year:{year}" if year else None
    url = f"{BASE}?search={q}&per-page=5"
    if filt:
        url += f"&filter={filt}"
    res = get(url)
    return res["results"][0] if res["results"] else None

FIELDS = "id,doi,display_name,publication_year,type,language,abstract_inverted_index,authorships,primary_location"

def fetch_works_by_ids(ids):
    """Batch-fetch full records for OpenAlex IDs (backward pass)."""
    out = []
    for i in range(0, len(ids), 50):
        chunk = [x.rsplit("/", 1)[-1] for x in ids[i:i+50]]
        filt = urllib.parse.quote("openalex_id:" + "|".join(chunk))
        res = get(f"{BASE}?filter={filt}&per-page=50&select={FIELDS}")
        out.extend(res["results"])
        time.sleep(0.3)
    return out

def fetch_cited_by(anchor_id):
    """Cursor-paginate forward citations with protocol filters."""
    out, cursor = [], "*"
    filt = urllib.parse.quote(
        f"cites:{anchor_id},publication_year:1990-2025,language:en,"
        f"type:article|book-chapter|review")
    while True:
        res = get(f"{BASE}?filter={filt}&per-page=200&cursor={urllib.parse.quote(cursor)}&select={FIELDS}")
        out.extend(res["results"])
        cursor = res["meta"].get("next_cursor")
        if not cursor or not res["results"]:
            break
        time.sleep(0.3)
    return out

ANCHORS = [
    ("Graham 2006", "10.1002/9780470753033", None, None),
    ("Kitchin 2014", "10.1177/2053951714528481", None, None),
    ("Weizman 2007", None, "Hollow Land: Israel's Architecture of Occupation", "2007"),
    ("Michael 2007", "10.1080/01402390701343417", None, None),
]

summary = {}
all_candidates = {}

for name, doi, title, year in ANCHORS:
    print(f"\n=== {name} ===")
    a = resolve_by_doi(doi) if doi else resolve_by_title(title, year)
    if not a:
        print(f"  !! could not resolve {name}")
        continue
    aid = a["id"].rsplit("/", 1)[-1]
    print(f"  resolved: {a['display_name'][:80]} ({a.get('publication_year')}) [{aid}]")
    print(f"  refs: {len(a.get('referenced_works', []))}, cited_by: {a.get('cited_by_count')}")

    # Backward pass: referenced works, filtered to protocol window/language/type
    refs_raw = a.get("referenced_works", [])
    refs = fetch_works_by_ids(refs_raw) if refs_raw else []
    refs_filt = [w for w in refs
                 if w.get("publication_year") and 1990 <= w["publication_year"] <= 2025
                 and w.get("language") == "en"
                 and w.get("type") in ("article", "book-chapter", "review")]
    print(f"  backward: {len(refs_raw)} refs -> {len(refs_filt)} after protocol filters")

    # Forward pass
    fw = fetch_cited_by(aid)
    print(f"  forward: {len(fw)} citing works after protocol filters")

    summary[name] = {"anchor_id": aid, "resolved_title": a["display_name"],
                     "refs_total": len(refs_raw), "backward_filtered": len(refs_filt),
                     "forward_filtered": len(fw)}
    for w in refs_filt:
        all_candidates.setdefault(w["id"], {"work": w, "via": set()})
        all_candidates[w["id"]]["via"].add(f"{name}:backward")
    for w in fw:
        all_candidates.setdefault(w["id"], {"work": w, "via": set()})
        all_candidates[w["id"]]["via"].add(f"{name}:forward")

print(f"\n=== TOTAL unique candidates: {len(all_candidates)} ===")

# Serialise
def slim(w):
    abs_idx = w.get("abstract_inverted_index") or {}
    abstract = ""
    if abs_idx:
        pos2tok = {}
        for tok, positions in abs_idx.items():
            for p in positions:
                pos2tok[p] = tok
        abstract = " ".join(pos2tok[i] for i in sorted(pos2tok))
    auth = w.get("authorships") or []
    first_author = (auth[0]["author"]["display_name"] if auth and auth[0].get("author") else "")
    src = ((w.get("primary_location") or {}).get("source") or {}).get("display_name", "")
    return {"openalex_id": w["id"], "doi": w.get("doi"), "title": w.get("display_name"),
            "year": w.get("publication_year"), "type": w.get("type"),
            "first_author": first_author, "source": src, "abstract": abstract}

records = [{**slim(v["work"]), "via": sorted(v["via"])} for v in all_candidates.values()]
with open(os.path.join(OUT, "candidates.json"), "w") as f:
    json.dump({"summary": summary, "n_candidates": len(records), "records": records}, f, indent=1)
print(json.dumps(summary, indent=1))
