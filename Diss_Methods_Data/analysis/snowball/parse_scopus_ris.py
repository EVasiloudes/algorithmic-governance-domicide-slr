#!/usr/bin/env python3
"""Parse a Scopus RIS export, dedup against the 874 corpus + 2,087 OpenAlex
candidates, save net-new records, optionally screen them.
Usage: python3 parse_scopus_ris.py <ris-file> [--screen]
"""
import re, json, csv, sys, os

OUT = os.path.dirname(os.path.abspath(__file__))

TAG_RE = re.compile(r"^([A-Z0-9]{2})  - ?(.*)$")

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
    ris_path = sys.argv[1]
    do_screen = "--screen" in sys.argv

    recs = parse_ris(ris_path)
    print(f"RIS records: {len(recs)}")

    corpus_t, corpus_d = set(), set()
    master = os.path.join(OUT, "../../Literature [.RIS]/deduplicated/screening_master.csv")
    with open(master, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("doi"): corpus_d.add(norm_doi(row["doi"]))
            if row.get("title"): corpus_t.add(norm_title(row["title"]))

    cand = json.load(open(os.path.join(OUT, "candidates.json")))["records"]
    cand_t = {norm_title(r["title"]) for r in cand if r.get("title")}
    cand_d = {norm_doi(r["doi"]) for r in cand if r.get("doi")}

    # also dedup against earlier Scopus net-new batches
    prior_path = os.path.join(OUT, "scopus_netnew.json")
    if os.path.exists(prior_path):
        prior = json.load(open(prior_path))
        for r in prior:
            t = norm_title(r.get("TI") or r.get("title"))
            d = norm_doi(r.get("DO") or r.get("doi"))
            if t: cand_t.add(t)
            if d: cand_d.add(d)

    net_new = []
    for r in recs:
        t, d = norm_title(r.get("TI")), norm_doi(r.get("DO"))
        in_corpus = (d and d in corpus_d) or (t and t in corpus_t)
        in_cand = (d and d in cand_d) or (t and t in cand_t)
        status = "CORPUS-DUP" if in_corpus else ("OPENALEX-DUP" if in_cand else "** NET-NEW **")
        if status == "** NET-NEW **":
            net_new.append(r)
        print(f"[{status:15s}] {r.get('PY')} | {(r.get('TI') or '')[:60]}")

    batch_tag = os.path.basename(ris_path)[:20].replace(" ", "_")
    out_path = os.path.join(OUT, f"scopus_netnew_{batch_tag}.json")
    json.dump(net_new, open(out_path, "w"), indent=1)
    print(f"\nnet-new saved to {out_path}: {len(net_new)}")

    # merge into cumulative net-new store (for cross-batch dedup)
    cum_path = os.path.join(OUT, "scopus_netnew.json")
    cum = json.load(open(cum_path)) if os.path.exists(cum_path) else []
    cum.extend(net_new)
    json.dump(cum, open(cum_path, "w"), indent=1)

    if do_screen and net_new:
        sys.path.insert(0, OUT)
        from screen_snowball import call_model, MODEL, FALLBACK_MODEL
        results = []
        for r in net_new:
            title = r.get("TI", "")
            abstract = r.get("AB", "")
            if len(abstract) < 200:
                verdict, raw, model = "Exclude", "triage_no_abstract", "triage"
            else:
                text = f"Title: {title}\n\nAbstract: {abstract[:6000]}"
                verdict, raw = call_model(MODEL, text)
                model = MODEL
                if verdict is None:
                    verdict, raw = call_model(FALLBACK_MODEL, text)
                    model = FALLBACK_MODEL
            results.append({"title": title, "year": r.get("PY"), "doi": r.get("DO"),
                            "source": r.get("T2"), "abstract": abstract,
                            "verdict": verdict, "model": model})
            print(f"  [{verdict}] {title[:65]}")
        out2 = os.path.join(OUT, f"scopus_netnew_screened_{batch_tag}.json")
        json.dump(results, open(out2, "w"), indent=1)
        print(f"screened saved: {out2}")
        # append to cumulative screened store
        cs_path = os.path.join(OUT, "scopus_netnew_screened.json")
        cs = json.load(open(cs_path)) if os.path.exists(cs_path) else []
        cs.extend(results)
        json.dump(cs, open(cs_path, "w"), indent=1)

if __name__ == "__main__":
    main()
