#!/usr/bin/env python3
"""Flag \\parencite/\\autocite calls where the author's surname already
appears in the immediately preceding prose — i.e. candidates for
\\citeyearpar (year+page only) instead of a full parenthetical citation."""

import re, sys, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIB = os.path.join(ROOT, "refs.bib")
TEXFILES = sorted(glob.glob(os.path.join(ROOT, "*.tex")) +
                  glob.glob(os.path.join(ROOT, "chapters", "*.tex")))

# --- parse bib: key -> list of surnames -------------------------------------
key2auth = {}
cur_key, cur_field, buf = None, None, ""
def flush():
    global buf
    if cur_key and cur_field == "author":
        # surnames = text before the comma in each "Last, First and Last, First"
        parts = [a.strip() for a in re.split(r"\s+and\s+", buf)]
        surs = []
        for p in parts:
            if "," in p:
                surs.append(p.split(",", 1)[0].strip())
            else:
                toks = p.split()
                if toks:
                    surs.append(toks[-1])
        # strip braces/diacritics wrappers
        surs = [re.sub(r"[{}\\'\"`^~.]", "", s) for s in surs if s]
        key2auth[cur_key] = surs
    buf = ""

for line in open(BIB, encoding="utf-8"):
    m = re.match(r"@\w+\{([^,]+),", line)
    if m:
        flush(); cur_key, cur_field = m.group(1).strip(), None
        continue
    m = re.match(r"\s*(\w+)\s*=\s*[\{\"](.*)", line)
    if m:
        flush()
        cur_field = m.group(1).lower()
        buf = m.group(2)
        continue
    if buf:
        buf += " " + line.strip()
flush()

# --- scan tex for citations --------------------------------------------------
CITE_RE = re.compile(r"\\(parencite|autocite|citep)\b(\[[^\]]*\])?\{([^}]+)\}")
WORD_WINDOW = 12

hits = []
for path in TEXFILES:
    text = open(path, encoding="utf-8").read()
    # drop comments
    text = re.sub(r"(?<!\\)%.*", "", text)
    for m in CITE_RE.finditer(text):
        keys = [k.strip() for k in m.group(3).split(",")]
        before = text[max(0, m.start()-400):m.start()]
        words = re.findall(r"[A-Za-zÀ-ÿ'’\-]+", before)[-WORD_WINDOW:]
        window_txt = " ".join(words).lower()
        dup = []
        for k in keys:
            surs = key2auth.get(k)
            if not surs:
                continue
            # any author surname (first two authors cover "X and Y" cases)
            for s in surs[:2]:
                if len(s) > 3 and s.lower() in window_txt:
                    dup.append(f"{k}({s})")
                    break
        if dup:
            line_no = text.count("\n", 0, m.start()) + 1
            ctx = " ".join(words[-8:])
            hits.append((os.path.relpath(path, ROOT), line_no,
                         m.group(1), ", ".join(dup), ctx))

if not hits:
    print("No duplicate author-in-prose citations found.")
else:
    print(f"{len(hits)} candidate(s):\n")
    for f, ln, cmd, dup, ctx in hits:
        print(f"{f}:{ln}  \\{cmd}  [{dup}]")
        print(f"    …{ctx} \u2026\n")
