TEX = env TEXINPUTS=:$(CURDIR)/packages/aastex52:$(CURDIR)/packages/astronat/apj:$(CURDIR)/packages/signalflowlibrary: pdflatex -file-line-error -halt-on-error -shell-escape
BIBTEX = env BSTINPUTS=:$(CURDIR)/packages/astronat/apj: TEXINPUTS=:$(CURDIR)/packages/aastex52:$(CURDIR)/packages/astronat/apj: bibtex

PREREQS = \
	figures/envelope.pdf figures/snr_in_time.pdf figures/loc_in_time.pdf figures/tmpltbank.pdf figures/lloid-diagram.pdf early_warning_poster.tex references.bib

early_warning_poster.pdf: $(PREREQS)
	$(TEX) -draftmode early_warning_poster
	$(BIBTEX) early_warning_poster
	$(TEX) -draftmode early_warning_poster
	$(TEX) early_warning_poster

figures/lloid-diagram.pdf: figures/diagram.tex
	$(MAKE) -C figures $(@F)

figures/envelope.pdf: envelope.py
	python $^ $@

figures/snr_in_time.pdf: snr_in_time.py
	python $^ $@

figures/loc_in_time.pdf: localization_uncertainty.py
	python $^ $@

clean:
	rm -f early_warning_poster.{aux,out,log,bbl,blg,pdf} time_slices.{tex,pdf} figures/envelope.pdf figures/loc_in_time.pdf figures/snr_in_time.pdf
