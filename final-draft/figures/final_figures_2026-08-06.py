#!/usr/bin/env python3
"""Final-spec figures for dissertation, 2026-08-06.
All counts grounded in Diss_Methods_Data (screening_master.csv,
combined_coding_275.csv, prisma_flow_2026-07-29.svg)."""
import csv, collections, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import matplotlib.patheffects as pe
import numpy as np

HALO = [pe.withStroke(linewidth=3.2, foreground="white")]

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, "..", "..", "Diss_Methods_Data")
rows = list(csv.DictReader(open(os.path.join(ROOT, "analysis", "combined_coding_275.csv"))))
for r in rows:
    for t in range(1, 5):
        try: r[f"theme_{t}_score"] = float(r[f"theme_{t}_score"])
        except ValueError: r[f"theme_{t}_score"] = np.nan
    try: r["year_i"] = int(r["year"])
    except ValueError: r["year_i"] = None

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["DejaVu Serif"],
    "font.size": 10, "figure.dpi": 300, "savefig.dpi": 300,
})
PAL = {"A": "#4878CF", "B": "#D65F5F", "SN": "#6ACC65",
       "ink": "#222222", "soft": "#666666", "gold": "#B7791F"}

def save(fig, name):
    fig.savefig(os.path.join(BASE, name), bbox_inches="tight", facecolor="white")
    plt.close(fig); print("wrote", name)

# =================================================================
# Fig 2.1 — Theoretical framework schematic (Ch2, Craig: pp. 15–17)
# =================================================================
fig, ax = plt.subplots(figsize=(12, 7.2)); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

def box(x, y, w, h, fc, ec="#333333"):
    ax.add_patch(mp.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012",
                                   fc=fc, ec=ec, lw=1.3))

elements = [
    ("Arrow (1962)", "The economics of information goods:\nindivisible, costless to reuse —\nno economic friction in redeployment"),
    ("Deleuze (1990)", "Societies of control:\nmodulation replaces enclosure;\npower operates through code"),
    ("DeLanda (1992, 2014)", "The machinic city:\npopulation-level data as a single\nsubstrate for governance"),
    ("Michael (2007)", "Epistemic authority:\nthe authority to define truth is\nauthority over whom truth targets"),
    ("Urbicide canon", "King (2004); Graham (2004, 2006, 2011);\nWeizman (2007): spatial destruction\nas political rationality"),
]
n = len(elements)
top, bh, gap = 0.94, 0.15, 0.032
for i, (title, body) in enumerate(elements):
    y = top - bh - i * (bh + gap)
    fc = "#FDEAEA" if i == n - 1 else "#E8F0FB"
    box(0.02, y, 0.27, bh, fc)
    ax.text(0.155, y + bh - 0.028, title, ha="center", fontsize=10.5, fontweight="bold",
            path_effects=HALO)
    ax.text(0.155, y + (bh - 0.05) / 2, body, ha="center", va="center", fontsize=8.2,
            path_effects=HALO)
    arr = mp.FancyArrowPatch((0.295, y + bh / 2), (0.435, 0.50),
                             connectionstyle="arc3,rad=-0.18",
                             arrowstyle="-|>", mutation_scale=13,
                             color="#555555", lw=1.2)
    ax.add_patch(arr)

box(0.44, 0.335, 0.25, 0.33, "#FFF3D6")
ax.text(0.565, 0.615, "The dual-use substrate", ha="center", fontsize=11.5, fontweight="bold",
        path_effects=HALO)
ax.text(0.565, 0.475, "The same data infrastructure optimises\nthe city and renders it targetable.\nNo intrinsic property of the data\ndistinguishes welfare from warfare —\nonly a change of inputs.",
        ha="center", va="center", fontsize=9, path_effects=HALO)
arr = mp.FancyArrowPatch((0.70, 0.50), (0.755, 0.50), connectionstyle="arc3,rad=0.0",
                         arrowstyle="-|>", mutation_scale=14, color="#555555", lw=1.4)
ax.add_patch(arr)
box(0.76, 0.335, 0.21, 0.33, "#FDEAEA")
ax.text(0.865, 0.615, "The junction", ha="center", fontsize=11.5, fontweight="bold",
        path_effects=HALO)
ax.text(0.865, 0.48, "Algorithmically\nmediated urbicide\n\n(RQ1 & RQ2)", ha="center", va="center",
        fontsize=9.5, path_effects=HALO)
ax.text(0.5, 0.16, "Benign urban management  on the one hand — social control, or worse, on the other",
        ha="center", fontsize=10.5, style="italic", color=PAL["ink"])
ax.text(0.5, 0.095, "One substrate, parameterised for welfare or warfare",
        ha="center", fontsize=9, style="italic", color=PAL["soft"])
ax.text(0.5, 0.985, "The five-element framework and the dual-use claim", ha="center",
        fontsize=13, fontweight="bold")
save(fig, "fig_2_1_framework_schematic.png")

# =================================================================
# Fig 3.1 — PRISMA 2020 flow, A4 landscape (Craig: p. 28)
# Counts verbatim from prisma_flow_2026-07-29.svg
# =================================================================
fig, ax = plt.subplots(figsize=(11.69, 8.27))  # A4 landscape
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

def pbox(x, y, w, h, lines, fc="#FFFFFF", fs=8.6, bold_first=False):
    ax.add_patch(mp.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.008",
                                   fc=fc, ec="#333333", lw=1.1))
    ax.text(x + w / 2, y + h / 2, "\n".join(lines), ha="center", va="center", fontsize=fs,
            linespacing=1.35)

def arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", lw=1.2, color="#333333"))

ax.text(0.5, 0.985, "PRISMA 2020 flow diagram — modified protocol", ha="center",
        fontsize=13, fontweight="bold")
ax.text(0.5, 0.955, "Algorithmic governance, urban space and domicide: a systematic literature review, 1990–2025",
        ha="center", fontsize=9.5, style="italic", color=PAL["soft"])

for y, lab in [(0.86, "Identification"), (0.52, "Screening"), (0.14, "Included")]:
    ax.text(0.028, y, lab, fontsize=10, fontweight="bold", rotation=90, va="center")

LX, LW = 0.07, 0.30     # left lane (databases)
RX, RW = 0.60, 0.33     # right lane (other methods)
pbox(LX, 0.80, LW, 0.14, ["Records identified from databases (n = 963):",
                          "Web of Science (n = 627); Scopus (n = 261);",
                          "Policy Commons (n = 73); other (n = 2)"], "#EEF4FF")
pbox(RX, 0.80, RW, 0.14, ["Records identified via other methods (n = 2,081)*:",
                          "citation searching of four anchor texts (Graham 2006;",
                          "Weizman 2007; Kitchin 2014; Michael 2007), backward +",
                          "forward, deduplicated against the main corpus"], "#EEF4FF")
pbox(LX, 0.60, LW, 0.10, ["Records screened, title/abstract (n = 874)",
                          "after 89 duplicates removed"], "#FFFFFF")
pbox(0.415, 0.60, 0.15, 0.10, ["Records excluded", "(n = 723)"], "#F6E9E9")
pbox(RX, 0.60, RW, 0.10, ["Records screened, title/abstract (n = 2,081)"], "#FFFFFF")
pbox(RX, 0.44, RW, 0.11, ["Records excluded (n = 1,957):",
                          "1,678 excluded + 279 borderline (\u201cmaybe\u201d)",
                          "excluded by documented decision"], "#F6E9E9")
pbox(LX, 0.44, LW, 0.10, ["Reports sought for retrieval (n = 151);",
                          "not retrieved (n = 4)"], "#FFFFFF")
pbox(LX, 0.28, LW, 0.10, ["Reports assessed at full text", "and coded (n = 147)"], "#FFFFFF")
pbox(RX, 0.28, RW, 0.10, ["Reports sought for retrieval (n = 124); not retrieved (n = 1);",
                          "assessed at full text and coded (n = 123)"], "#FFFFFF")
pbox(LX, 0.15, LW, 0.11, ["Studies included from database", "searching (n = 151; 147 coded)"], "#E9F6E9")
pbox(RX, 0.15, RW, 0.11, ["Studies included from citation", "searching (n = 124; 123 coded)"], "#E9F6E9")
pbox(0.37, 0.055, 0.26, 0.065, ["Total included (n = 275);",
                                "in thematic synthesis (n = 270)"], "#DFF0D8", fs=8.4)

arrow(LX + LW / 2, 0.80, LX + LW / 2, 0.70)                      # identified -> screened
arrow(LX + LW, 0.65, 0.415, 0.65)                                # screened -> excluded
arrow(LX + LW / 2, 0.60, LX + LW / 2, 0.54)                      # screened -> sought
arrow(LX + LW / 2, 0.44, LX + LW / 2, 0.38)                      # sought -> assessed
arrow(LX + LW / 2, 0.28, LX + LW / 2, 0.26)                      # assessed -> included
arrow(RX + RW / 2, 0.80, RX + RW / 2, 0.70)                      # other identified -> screened
arrow(RX + RW / 2, 0.60, RX + RW / 2, 0.55)                      # screened -> excluded
arrow(RX + RW / 2, 0.44, RX + RW / 2, 0.38)                      # excluded lane continues to assessed
arrow(RX + RW / 2, 0.28, RX + RW / 2, 0.26)                      # assessed -> included
arrow(LX + LW / 2, 0.15, 0.47, 0.11)                             # DB included -> total
arrow(RX + RW / 2, 0.15, 0.55, 0.11)                             # snowball included -> total

ax.text(0.5, 0.028, "AI-assisted screening (DeepSeek V4 Flash, temperature 0.0), human-verified protocol; all final decisions retained by the author.\n"
        "* Anchor yields (includes): Weizman 2007 forward 46; Kitchin 2014 forward 42; Graham 2006 forward 38; Michael 2007: 0.  "
        "Databases searched 3 July 2026; citation searching completed 28 July 2026.",
        ha="center", va="top", fontsize=7.6, color=PAL["soft"], linespacing=1.5)
save(fig, "fig_3_1_prisma_flow_landscape.png")

# =================================================================
# Fig 3.2 — Publication-year distribution of the coded corpus (§3.3.1)
# =================================================================
A  = [r for r in rows if r["via_or_origin"] == "A"]
B  = [r for r in rows if r["via_or_origin"] == "B"]
SN = [r for r in rows if r["corpus"] == "snowball"]
xs = list(range(1998, 2026))  # earliest record 1998; window to 2025
def year_counts(sub):
    c = collections.Counter(r["year_i"] for r in sub if r["year_i"] and r["year_i"] <= 2025)
    return [c.get(x, 0) for x in xs]
ya, yb, ys = year_counts(A), year_counts(B), year_counts(SN)

fig, ax = plt.subplots(figsize=(10.5, 5.4))
ax.bar(xs, ya, label="Search A — civil–military urban technology nexus (n = 128)", color=PAL["A"])
ax.bar(xs, yb, bottom=ya, label="Search B — spatial destruction and the datafied city (n = 23)", color=PAL["B"])
bottoms = [a + b for a, b in zip(ya, yb)]
ax.bar(xs, ys, bottom=bottoms, label="Citation chaining (n = 124)", color=PAL["SN"])
ax.set_xlim(1997.2, 2025.8)
ax.set_xlabel("Publication year"); ax.set_ylabel("Included records")
ax.set_title("The coded corpus by publication year, 1998–2025 (n = 271 in-window)")
ax.legend(fontsize=8.8, frameon=False)
ax.spines[["top", "right"]].set_visible(False)
tot = [a + b + s for a, b, s in zip(ya, yb, ys)]
pk = xs[int(np.argmax(tot))]
ax.annotate("post-2015 concentration:\n"
            f"{sum(t for x, t in zip(xs, tot) if x >= 2015)} of {sum(tot)} in-window records",
            xy=(pk, max(tot)), xytext=(2004, max(tot) * 0.88), fontsize=8.8,
            arrowprops=dict(arrowstyle="->", color=PAL["soft"]))
ax.text(0.005, -0.16, "Four in-press records dated 2026 fall outside the identification window and are omitted from this chart.",
        transform=ax.transAxes, fontsize=7.8, color=PAL["soft"])
save(fig, "fig_3_2_publication_trends.png")

# =================================================================
# Fig 5.1 — Mean theme scores by search strategy (Ch4/5)
# Matches dissertation text: A n=126 (T4 0.32); B n=21 (T4 1.81, T1 0.67)
# =================================================================
def means(sub):
    out, ns = [], []
    for t in range(1, 5):
        v = [r[f"theme_{t}_score"] for r in sub if not np.isnan(r[f"theme_{t}_score"])]
        out.append(sum(v) / len(v)); ns.append(len(v))
    return out, ns
mA, nA = means(A); mB, nB = means(B); mS, nS = means(SN)
labels = ["Theme 1\nDual-use fluidity", "Theme 2\nEpistemic authority",
          "Theme 3\nMachinic city", "Theme 4\nSpatial destruction"]
row_names = [f"Search A: governance\n(n = {nA[0]})", f"Search B: destruction\n(n = {nB[0]})",
             f"Citation chaining\n(n = {nS[0]})"]
data = np.array([mA, mB, mS])

fig, ax = plt.subplots(figsize=(9.8, 4.9))
im = ax.imshow(data, cmap="RdYlGn", vmin=0, vmax=2, aspect="auto")
ax.set_xticks(range(4), labels, fontsize=9)
ax.set_yticks(range(3), row_names, fontsize=9.5)
for i in range(3):
    for j in range(4):
        ax.text(j, i, f"{data[i, j]:.2f}", ha="center", va="center",
                fontweight="bold", fontsize=12, color="#222222")
ax.set_title("Mean coding scores by search strategy — two literatures running in parallel", pad=12)
cb = fig.colorbar(im, ax=ax, shrink=0.85); cb.set_label("Mean coding score (0 = absent, 2 = central)", fontsize=8.5)
ax.set_xticks(np.arange(-0.5, 4, 1), minor=True); ax.set_yticks(np.arange(-0.5, 3, 1), minor=True)
ax.grid(which="minor", color="white", lw=2.5); ax.tick_params(which="both", length=0)
save(fig, "fig_5_1_theme_by_strategy.png")

# =================================================================
# Fig 6.1 — The junction the literature has not built (Ch6 "map")
# Grounded: T4-G cluster = 5 records, all but one 2021+ (Graham 2008 the precursor)
# =================================================================
fig, ax = plt.subplots(figsize=(11.5, 6.8)); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
ax.add_patch(mp.Ellipse((0.285, 0.60), 0.46, 0.58, fc="#DBE7FA", ec=PAL["A"], lw=2, alpha=0.9))
ax.add_patch(mp.Ellipse((0.715, 0.60), 0.46, 0.58, fc="#FADCDC", ec=PAL["B"], lw=2, alpha=0.9))
ax.text(0.285, 0.845, "Algorithmic urban governance", ha="center", fontsize=12, fontweight="bold", color="#2C5282", path_effects=HALO)
ax.text(0.715, 0.845, "Spatial destruction and urbicide", ha="center", fontsize=12, fontweight="bold", color="#9C2B2B", path_effects=HALO)
ax.text(0.17, 0.60, "Search A  (n = 128)\n\noptimisation, sensing,\nplatforms, control\n\nT4 mean 0.32",
        ha="center", va="center", fontsize=9.5, color=PAL["ink"], path_effects=HALO)
ax.text(0.83, 0.60, "Search B  (n = 23)\n\ndomicide, targeting,\nsiege, reconstruction\n\nT4 mean 1.81",
        ha="center", va="center", fontsize=9.5, color=PAL["ink"], path_effects=HALO)
ax.text(0.5, 0.60, "THE JUNCTION\nalgorithmically\nmediated urbicide\n\n5 records of the coded 270,\nall but one since 2021",
        ha="center", va="center", fontsize=10.5, fontweight="bold", color="#7B341E",
        bbox=dict(boxstyle="round,pad=0.45", fc="#FFF3D6", ec=PAL["gold"], lw=1.6))
ax.text(0.5, 0.30, "Zero overlapping records between Search A and Search B at screening (874 records).",
        ha="center", fontsize=10, style="italic")
ax.text(0.5, 0.235, "The literature's elements are well documented but segregated — the map is the finding.",
        ha="center", fontsize=10, style="italic")
ax.text(0.5, 0.175, "Citation chaining (n = 124) bridges the two bodies but does not close the junction.",
        ha="center", fontsize=9, color=PAL["soft"])
ax.text(0.5, 0.975, "The systematic map: a junction the literature has not yet built", ha="center",
        fontsize=13, fontweight="bold")
save(fig, "fig_6_1_junction_map.png")

print("all figures regenerated")
