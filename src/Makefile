.PHONY: all

all: dependencies build runtm
	

.PHONY: runtm
runtm:
	ln -sf runtm.py runtm
	chmod +x runtm

.PHONY: dependencies
dependencies:
	python3 -m pip install --user numpy cython

.PHONY: build
build:
	python3 setup.py build_ext --inplace

.PHONY: clean
clean:
	#rm -rf optimizations.c*