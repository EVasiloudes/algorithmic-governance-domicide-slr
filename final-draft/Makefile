# Build the dissertation PDF
# Requires: xelatex, biber (BasicTeX at /usr/local/texlive/2025basic/bin/universal-darwin)

TEX = dissertation
ENGINE = xelatex

all: $(TEX).pdf

$(TEX).pdf: $(TEX).tex refs.bib
	PATH=/usr/local/texlive/2025basic/bin/universal-darwin:$$PATH $(ENGINE) -interaction=nonstopmode $(TEX)
	PATH=/usr/local/texlive/2025basic/bin/universal-darwin:$$PATH biber $(TEX)
	PATH=/usr/local/texlive/2025basic/bin/universal-darwin:$$PATH $(ENGINE) -interaction=nonstopmode $(TEX)
	PATH=/usr/local/texlive/2025basic/bin/universal-darwin:$$PATH $(ENGINE) -interaction=nonstopmode $(TEX)

clean:
	rm -f *.aux *.bbl *.bcf *.blg *.log *.out *.run.xml *.toc *.lof *.lot
	rm -f $(TEX).pdf

.PHONY: all clean
