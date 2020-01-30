all:
	$(MAKE) -C timeline
	$(MAKE) -C bootseq
	pandoc \
		-t beamer \
		--pdf-engine=xelatex \
		--template=template.latex \
		-fmarkdown-implicit_figures \
		-V fontfamily="sourcesanspro" \
		-V logo="img/fosdem_logo.png" \
		-V background-image=img/bg169.jpg \
		-V classoption:aspectratio=169 \
		-V geometry:"hmargin=1.85cm, nomarginpar" \
		-o slides169.pdf \
		slides.md

43:
	$(MAKE) -C timeline
	$(MAKE) -C bootseq
	pandoc \
		-t beamer \
		--pdf-engine=xelatex \
		--template=template.latex \
		-fmarkdown-implicit_figures \
		-V fontfamily="sourcesanspro" \
		-V logo="img/fosdem_logo.png" \
		-V background-image=img/bg.jpg \
		-V classoption:aspectratio=43 \
		-V geometry:"hmargin=1.85cm, nomarginpar" \
		-o slides.pdf \
		slides.md
