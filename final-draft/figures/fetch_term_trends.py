#!/usr/bin/env python3
"""Fetch OpenAlex publication-count time series (1990-2025) for key terms,
save raw JSON, and draw fig_3_2_literature_trends.png."""
import json, os, ssl, time, urllib.request, urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, "..", "..", "Diss_Methods_Data", "analysis")
ENV = os.path.join(ROOT, "snowball", ".env")
KEY = ""
for line in open(ENV):
    if line.startswith("OPENALEX_API_KEY="):
        KEY = line.split("=", 1)[1].strip()

TERMS = {
    "smart cities": "smart cities",
    "algorithmic governance": "algorithmic governance",
    "predictive policing": "predictive policing",
    "urbicide": "urbicide",
    "domicide": "domicide",
}
ctx = ssl.create_default_context()
try:
    import certifi; ctx = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    pass

def fetch(term):
    q = urllib.parse.urlencode({
        "filter": f"title_and_abstract.search:{term},publication_year:1990-2025",
        "group_by": "publication_year", "per-page": 200,
        **({"api_key": KEY} if KEY else {"mailto": "elias@densetheory.cc"}),
    })
    url = f"https://api.openalex.org/works?{q}"
    with urllib.request.urlopen(url, context=ctx, timeout=60) as r:
        return json.load(r)

out = {}
for label, term in TERMS.items():
    try:
        d = fetch(term)
        years = {int(g["key"]): g["count"] for g in d.get("group_by", [])}
        out[label] = {"term": term, "total": d["meta"]["count"], "years": years}
        print(f"{label}: total={d['meta']['count']}")
    except Exception as e:
        print(f"{label}: FAILED {e}")
    time.sleep(1)

raw_path = os.path.join(ROOT, "openalex_term_trends_2026-08-06.json")
json.dump({"fetched": "2026-08-06", "source": "OpenAlex works, title_and_abstract.search, 1990-2025",
           "data": out}, open(raw_path, "w"), indent=1)
print("saved", raw_path)

# ---- chart ----
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "serif", "font.serif": ["DejaVu Serif"],
                     "font.size": 10, "figure.dpi": 300, "savefig.dpi": 300})
COLORS = {"smart cities": "#4878CF", "algorithmic governance": "#6ACC65",
          "predictive policing": "#B8860B", "urbicide": "#D65F5F", "domicide": "#9467BD"}
xs = list(range(1990, 2026))
fig, ax = plt.subplots(figsize=(10.5, 5.6))
for label, d in out.items():
    ys = [d["years"].get(x, 0) for x in xs]
    ax.plot(xs, ys, lw=2, color=COLORS[label],
            label=f"\u201c{d['term']}\u201d (n = {d['total']:,})")
ax.set_yscale("log")
ax.set_xlim(1990, 2025); ax.set_xlabel("Publication year")
ax.set_ylabel("Works per year (log scale)")
ax.set_title("Key-term publication volume, 1990–2025 (OpenAlex, title/abstract match)")
ax.legend(fontsize=8.6, frameon=False, loc="upper left")
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.25, lw=0.5)
ax.annotate("smart-city wave\n(post-2010)", xy=(2012, out.get("smart cities", {}).get("years", {}).get(2012, 100)),
            xytext=(1996, 3000), fontsize=8.4, color="#4878CF",
            arrowprops=dict(arrowstyle="->", color="#4878CF", lw=0.9))
fig.savefig(os.path.join(BASE, "fig_3_3_literature_trends.png"), bbox_inches="tight", facecolor="white")
print("wrote fig_3_3_literature_trends.png")
