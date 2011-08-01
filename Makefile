TEX = env TEXINPUTS=:$(CURDIR)/packages/aastex52:$(CURDIR)/packages/astronat/apj:$(CURDIR)/packages/signalflowlibrary: pdflatex -file-line-error -halt-on-error -shell-escape
BIBTEX = env BSTINPUTS=:$(CURDIR)/packages/astronat/apj: TEXINPUTS=:$(CURDIR)/packages/aastex52:$(CURDIR)/packages/astronat/apj: bibtex

PREREQS = \
	figures/envelope.png figures/snr_in_time.png figures/loc_in_time.png figures/tmpltbank.png figures/lloid-diagram.pdf early_warning_poster.tex macros.tex references.bib

all: early_warning_slides.pdf early_warning_poster.pdf

early_warning_slides.pdf: early_warning_slides.tex
	$(TEX) -draftmode early_warning_slides
	#$(BIBTEX) early_warning_slides
	#$(TEX) -draftmode early_warning_slides
	$(TEX) early_warning_slides

early_warning_poster.pdf: $(PREREQS)
	$(TEX) -draftmode early_warning_poster
	$(BIBTEX) early_warning_poster
	$(TEX) -draftmode early_warning_poster
	$(TEX) early_warning_poster

figures/lloid-diagram.pdf: figures/diagram.tex macros.tex
	$(MAKE) -C figures $(@F)

figures/envelope.png: envelope.py matplotlibrc
	python $< $@

figures/snr_in_time.png: snr_in_time.py matplotlibrc
	python $< $@

figures/loc_in_time.png: localization_uncertainty.py matplotlibrc
	python $< $@

figures/tmpltbank.png: plot_bank.py matplotlibrc data/tmpltbank.xml data/tmpltbank-pruned.xml
	python $< $@

clean:
	rm -f early_warning_poster.{aux,out,log,bbl,blg,pdf} figures/tmpltbank.png figures/envelope.png figures/loc_in_time.png figures/snr_in_time.png
