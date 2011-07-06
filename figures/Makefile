TEX = env TEXINPUTS=:../packages/signalflowlibrary: pdflatex -file-line-error -halt-on-error -shell-escape
FIGURES = lloid-diagram downsample-symbol upsample-symbol adder-symbol fir-symbol

all: $(foreach X,$(FIGURES),$X.pdf)

.INTERMEDIATE: diagram.pdf

diagram.pdf: diagram.tex ../macros.tex
	$(TEX) diagram

$(foreach X,$(FIGURES),$X.pdf): diagram.pdf
	true # noop
clean:
	rm -f $(foreach X,$(FIGURES),$X.{dpth,log,pdf,eps,dvi}) diagram.{pdf,aux,auxlock,log}
