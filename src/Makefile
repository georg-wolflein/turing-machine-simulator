.PHONY: all

all: dependencies build runtm

.PHONY: tests
tests:
	python3 -m tests.run_tests

.PHONY: data
data:
	python3 -m data.generate.paren
	python3 -m data.generate.binadd
	python3 -m data.generate.binaryunary
	python3 -m data.generate.subword

.PHONY: plot
plot: dependencies
	python3 -m data.plot
	python3 -m data.appendices

.PHONY: report
report:
	mkdir -p ../tex/images/graphs
	cp -r ../data/*.pdf ../tex/images/graphs
	cd tex && pdflatex main.tex
	cp text/main.pdf report.pdf

.PHONY: runtm
runtm:
	ln -sf runtm.py runtm
	chmod +x runtm

.PHONY: dependencies
dependencies:
	python3 -m pip install --user numpy cython pandas matplotlib

.PHONY: build
build:
	python3 setup.py build_ext --inplace

.PHONY: clean
clean:
	#rm -rf optimizations.c*