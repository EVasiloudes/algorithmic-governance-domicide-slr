# Build the dissertation PDF
# Requires: lualatex (or pdflatex), biber

TEX = dissertation
ENGINE = lualatex

all: $(TEX).pdf

$(TEX).pdf: $(TEX).tex refs.bib
	$(ENGINE) $(TEX)
	biber $(TEX)
	$(ENGINE) $(TEX)
	$(ENGINE) $(TEX)

clean:
	rm -f *.aux *.bbl *.bcf *.blg *.log *.out *.run.xml *.toc *.lof *.lot
	rm -f $(TEX).pdf

.PHONY: all clean
