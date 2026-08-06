#!/usr/bin/env python3
"""Draft figures for Craig meeting 2026-08-06. All DRAFT quality."""
import csv, collections, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "..", "..", "Diss_Methods_Data", "analysis", "combined_coding_275.csv")
rows = list(csv.DictReader(open(DATA)))
for r in rows:
    for t in range(1, 5):
        try: r[f"theme_{t}_score"] = float(r[f"theme_{t}_score"])
        except: r[f"theme_{t}_score"] = np.nan
    try: r["year_i"] = int(r["year"])
    except: r["year_i"] = None

plt.rcParams.update({"font.family": "serif", "font.size": 11, "figure.dpi": 150})
C = {"gov": "#4878CF", "dest": "#D65F5F", "acc": "#6ACC65", "grey": "#888888"}

def stamp(fig):
    fig.text(0.99, 0.01, "DRAFT 2026-08-06", ha="right", fontsize=8, color="red", alpha=0.7)

# ---------------------------------------------------------------- G1: Ch2 framework schematic
fig, ax = plt.subplots(figsize=(11, 6.5)); ax.axis("off")
def box(x, y, w, h, title, body, fc="#f2f2f2", ec="#333"):
    ax.add_patch(mp.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02", fc=fc, ec=ec, lw=1.4))
    ax.text(x+w/2, y+h-0.055, title, ha="center", fontsize=11, fontweight="bold")
    ax.text(x+w/2, y+h/2-0.06, body, ha="center", va="center", fontsize=8.5)
elems = [
    ("Arrow (1962)", "Information as an\nindivisible good —\ncostless reuse", "#e8f0fb"),
    ("Deleuze (1990)", "Societies of control —\nmodulation, not\nenclosure", "#e8f0fb"),
    ("DeLanda (1992,\n2014)", "The machinic city —\npopulation-level data\nas substrate", "#e8f0fb"),
    ("Michael (2007)", "Epistemic authority —\nwho may know and\ndecide", "#e8f0fb"),
    ("Urbicide canon\nKing; Graham;\nWeizman", "Spatial destruction\nas political\nrationality", "#fdeaea"),
]
for i, (t, b, fc) in enumerate(elems):
    box(0.02, 0.86 - i*0.21, 0.24, 0.17, t, b, fc)
    ax.annotate("", xy=(0.47, 0.5), xytext=(0.27, 0.945 - i*0.21),
                arrowprops=dict(arrowstyle="-|>", color="#555", lw=1.2))
box(0.47, 0.36, 0.24, 0.28, "Dual-use substrate",
    "The same data infrastructure\noptimises the city and\nmakes it targetable —\nno intrinsic property\ndistinguishes the modes", "#fff3d6")
ax.annotate("", xy=(0.82, 0.5), xytext=(0.72, 0.5), arrowprops=dict(arrowstyle="-|>", color="#555", lw=1.2))
box(0.82, 0.36, 0.16, 0.28, "The junction",
    "Algorithmically\nmediated\nurbicide\n\n(RQ1 & RQ2)", "#fdeaea")
ax.text(0.5, 0.13, "Benign urban management  ⟷  social control — or worse", ha="center",
        fontsize=12, style="italic", color="#333")
ax.text(0.5, 0.06, "One substrate, parameterised for welfare or warfare", ha="center",
        fontsize=9.5, color="#666")
stamp(fig); fig.savefig(os.path.join(BASE, "draft_G1_framework_schematic.png"), bbox_inches="tight"); plt.close(fig)

# ---------------------------------------------------------------- G2: PRISMA-style flow, landscape
fig, ax = plt.subplots(figsize=(13.5, 7.5)); ax.axis("off")  # A4 landscape ratio
def pbox(x, y, w, h, lines, fc="#f7f7f7", fs=10):
    ax.add_patch(mp.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015", fc=fc, ec="#333", lw=1.3))
    ax.text(x+w/2, y+h/2, "\n".join(lines), ha="center", va="center", fontsize=fs)
def arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", lw=1.3, color="#333"))
ax.text(0.055, 0.97, "Identification", fontsize=11, fontweight="bold", rotation=90, va="top")
ax.text(0.055, 0.55, "Screening", fontsize=11, fontweight="bold", rotation=90, va="center")
ax.text(0.055, 0.16, "Included", fontsize=11, fontweight="bold", rotation=90, va="center")
pbox(0.10, 0.80, 0.26, 0.16, ["Records identified — Search A+B", "(civil–military nexus / destruction", "of the datafied city), 1990–2025"])
pbox(0.40, 0.80, 0.24, 0.16, ["Records after deduplication", "(n = 874)"], "#eef4ff")
pbox(0.69, 0.80, 0.28, 0.16, ["Citation chaining from anchor texts", "(Graham 2006; Weizman 2007;", "Kitchin 2014) — snowball candidates"])
pbox(0.40, 0.48, 0.24, 0.16, ["Records screened", "on title/abstract (n = 874)"])
pbox(0.72, 0.50, 0.25, 0.12, ["Records excluded (n = 723)"], "#f6e9e9")
pbox(0.40, 0.13, 0.24, 0.16, ["Included — database searches", "(n = 151)"], "#e9f6e9")
pbox(0.69, 0.13, 0.28, 0.16, ["Included — citation chaining", "(n = 124)"], "#e9f6e9")
pbox(0.13, 0.13, 0.20, 0.16, ["Coded corpus", "(n = 275)"], "#dff0d8", fs=11)
arrow(0.36, 0.88, 0.40, 0.88); arrow(0.52, 0.80, 0.52, 0.64)
arrow(0.64, 0.56, 0.72, 0.56); arrow(0.52, 0.48, 0.52, 0.29)
arrow(0.83, 0.80, 0.83, 0.29); arrow(0.40, 0.21, 0.33, 0.21); arrow(0.69, 0.21, 0.33, 0.21)
ax.text(0.5, 0.02, "Modified PRISMA 2020 flow — draft figures, verify against screening_master.csv", ha="center", fontsize=8.5, color="#666")
stamp(fig); fig.savefig(os.path.join(BASE, "draft_G2_prisma_flow_landscape.png"), bbox_inches="tight"); plt.close(fig)

# ---------------------------------------------------------------- G3: citation-trend / recency (§3.3.1)
yrs = [r["year_i"] for r in rows if r["year_i"]]
cnt = collections.Counter(yrs)
xs = list(range(1990, 2026))
main = [cnt.get(y, 0) for y in xs]
sn = collections.Counter(r["year_i"] for r in rows if r["corpus"]=="snowball" and r["year_i"])
mn = collections.Counter(r["year_i"] for r in rows if r["corpus"]=="main" and r["year_i"])
fig, ax = plt.subplots(figsize=(11, 5.2))
ax.bar(xs, [mn.get(y,0) for y in xs], label="Database searches (n=151)", color=C["gov"])
ax.bar(xs, [sn.get(y,0) for y in xs], bottom=[mn.get(y,0) for y in xs], label="Citation chaining (n=124)", color=C["acc"])
ax.set_xlim(1989, 2026); ax.set_xlabel("Publication year"); ax.set_ylabel("Included records")
ax.set_title("Included records by year, 1990–2025 — recency spike in the coded corpus (DRAFT)")
ax.legend(); ax.spines[["top","right"]].set_visible(False)
ax.annotate("post-2015 spike", xy=(2018, max(main)*0.9), fontsize=9, color="#333")
stamp(fig); fig.savefig(os.path.join(BASE, "draft_G3_publication_trends.png"), bbox_inches="tight"); plt.close(fig)

# ---------------------------------------------------------------- G4: Ch5 findings — theme × corpus
labels = ["T1 Dual-use\nfluidity", "T2 Epistemic\nauthority", "T3 Machinic\ncity", "T4 Spatial\ndestruction"]
gov = [r for r in rows if r["corpus"]=="main"]; de = [r for r in rows if r["corpus"]=="snowball"]
m_gov = [np.nanmean([r[f"theme_{t}_score"] for r in gov]) for t in range(1,5)]
m_de  = [np.nanmean([r[f"theme_{t}_score"] for r in de]) for t in range(1,5)]
fig, ax = plt.subplots(figsize=(9.5, 5.5))
im = ax.imshow([m_gov, m_de], cmap="RdYlGn", vmin=0, vmax=2, aspect="auto")
ax.set_xticks(range(4), labels); ax.set_yticks([0,1], [f"Database searches\n(n={len(gov)})", f"Citation chaining\n(n={len(de)})"])
for i, vals in enumerate([m_gov, m_de]):
    for j, v in enumerate(vals):
        ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontweight="bold", fontsize=12)
ax.set_title("Mean theme scores by search strategy — two literatures running in parallel (DRAFT)")
fig.colorbar(im, ax=ax, shrink=0.8, label="Mean coding score (0–2)")
stamp(fig); fig.savefig(os.path.join(BASE, "draft_G4_theme_by_strategy_heatmap.png"), bbox_inches="tight"); plt.close(fig)

# ---------------------------------------------------------------- G5: Ch6 map — the junction the literature hasn't built
fig, ax = plt.subplots(figsize=(11, 6.5)); ax.axis("off")
ax.add_patch(mp.Ellipse((0.30, 0.55), 0.44, 0.62, fc="#dbe7fa", ec="#4878CF", lw=2, alpha=0.85))
ax.add_patch(mp.Ellipse((0.70, 0.55), 0.44, 0.62, fc="#fadcdc", ec="#D65F5F", lw=2, alpha=0.85))
ax.text(0.22, 0.78, "Algorithmic urban\ngovernance literature", ha="center", fontsize=12, fontweight="bold", color="#2c5282")
ax.text(0.78, 0.78, "Spatial destruction /\nurbicide literature", ha="center", fontsize=12, fontweight="bold", color="#9c2b2b")
ax.text(0.20, 0.52, "optimisation • sensing\nplatforms • control\nsmart-city pilots", ha="center", fontsize=9.5, color="#333")
ax.text(0.80, 0.52, "domicide • urbicide\ntargeting • siege\nForensic Architecture", ha="center", fontsize=9.5, color="#333")
ax.text(0.50, 0.55, "THE JUNCTION\nalgorithmically\nmediated urbicide\n\n5 records of 275", ha="center", va="center", fontsize=11, fontweight="bold", color="#7b341e",
        bbox=dict(boxstyle="round,pad=0.4", fc="#fff3d6", ec="#b7791f", lw=1.5))
ax.text(0.50, 0.18, "Zero overlap between the two search strategies at screening (874 records)", ha="center", fontsize=10, style="italic")
ax.text(0.50, 0.11, "The map is the finding: the literature's elements are well-documented but segregated", ha="center", fontsize=10, style="italic")
stamp(fig); fig.savefig(os.path.join(BASE, "draft_G5_the_junction_map.png"), bbox_inches="tight"); plt.close(fig)

print("done:", [f for f in sorted(os.listdir(BASE)) if f.startswith("draft_")])
