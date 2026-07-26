#!/usr/bin/env python3
"""Re-screen snowball records that were triaged as no_abstract but now have
abstracts from enrichment (S2/OpenAlex). Updates snowball_screening.csv in-place."""
import os, csv, json, time, re, sys, ssl, urllib.request
import certifi

CUR = os.path.dirname(os.path.abspath(__file__))

# Load OpenRouter key
def _load_key():
    # Deduplicated .env has OPENROUTER
    env_path = "/Users/eliasvasnic/Obsidian Vaults/Elias Vasnic Obsidian Vault/Atoms/Public_Policy_&_Management/Courses/MSc PPM Dissertation - Repo/Diss_Methods_Data/Literature [.RIS]/deduplicated/.env"
    try:
        for line in open(env_path):
            if "OPENROUTER_API_KEY" in line:
                val = line.strip().split("=", 1)[1].strip().strip('"').strip("'")
                if val: return val
    except OSError: pass
    return ""

API_KEY = _load_key()
if not API_KEY: sys.exit("No OpenRouter API key found")

MODEL = "deepseek/deepseek-chat"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = open(os.path.join(CUR, "screening_prompt.txt")).read()

def call_model(text):
    payload = {"model": MODEL,
               "messages": [{"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": text}],
               "temperature": 0.0, "max_tokens": 256}
    for attempt in range(3):
        try:
            req = urllib.request.Request(OPENROUTER_URL,
                data=json.dumps(payload).encode(),
                headers={"Authorization": f"Bearer {API_KEY}",
                         "Content-Type": "application/json",
                         "X-Title": "SLR-ReScreener"})
            with urllib.request.urlopen(req, timeout=90,
                context=ssl.create_default_context(cafile=certifi.where())) as r:
                data = json.load(r)
            msg = data["choices"][0]["message"]
            txt = (msg.get("content") or msg.get("reasoning_content") or "").strip()
            m = re.search(r'\b(Include|Exclude|Maybe)\b', txt, re.IGNORECASE)
            return (m.group(1).capitalize() if m else "Maybe"), txt
        except Exception as e:
            time.sleep(2 ** attempt * 3)
    return "error", "retries exhausted"

def main():
    # Load enriched candidates
    with open(os.path.join(CUR, "candidates_enriched.json")) as f:
        enriched_list = json.load(f)["kept"]
    
    enriched_lookup = {}
    for r in enriched_list:
        eid = r.get("openalex_id") or r.get("id")
        if eid: enriched_lookup[eid] = r
    
    # Load screening CSV
    csv_path = os.path.join(CUR, "snowball_screening.csv")
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row for row in reader]
    
    idx_id = header.index("openalex_id")
    idx_triage = header.index("triage")
    idx_verdict = header.index("verdict")
    idx_model = header.index("model")
    idx_raw = header.index("raw_response")
    
    # Find triaged records that now have abstracts
    to_rescreen = []
    for row in rows:
        oaid = row[idx_id]
        if row[idx_triage] != "excluded_no_abstract":
            continue
        er = enriched_lookup.get(oaid)
        if er and er.get("abstract") and len(er.get("abstract", "")) >= 200:
            to_rescreen.append((row, er))
    
    print(f"Records to re-screen: {len(to_rescreen)}")
    if not to_rescreen:
        print("Nothing to do.")
        return
    
    included, maybes, excluded = 0, 0, 0
    for i, (row, er) in enumerate(to_rescreen):
        title = er.get("title", "")
        abstract = er.get("abstract", "")[:6000]
        text = f"Title: {title}\n\nAbstract: {abstract}"
        
        verdict, raw = call_model(text)
        row[idx_triage] = "screened"
        row[idx_verdict] = verdict
        row[idx_model] = MODEL
        row[idx_raw] = raw[:500]
        
        if verdict == "Include":
            included += 1
            print(f"  [{i+1}/{len(to_rescreen)}] ★ INCLUDE | {title[:70]}")
        elif verdict == "Maybe":
            maybes += 1
            print(f"  [{i+1}/{len(to_rescreen)}] ↔ Maybe  | {title[:70]}")
        else:
            excluded += 1
            if i < 5 or verdict != "Exclude":
                print(f"  [{i+1}/{len(to_rescreen)}] — {verdict}  | {title[:70]}")
        
        if (i+1) % 20 == 0:
            print(f"  ... {i+1} done (Incl:{included}, Maybe:{maybes}, Excl:{excluded})")
        time.sleep(1.0)
    
    print(f"\nRe-screening complete:")
    print(f"  Include: {included}")
    print(f"  Maybe:   {maybes}")
    print(f"  Exclude: {excluded}")
    
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"Saved: {csv_path}")

if __name__ == "__main__":
    main()