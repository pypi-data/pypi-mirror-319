.PHONY: build clean install publish check-dist

PYTHON := python3
PIP := $(PYTHON) -m pip

build:
	$(PYTHON) -m build

clean:
	rm -rf dist/ build/ *.egg-info/

install:
	$(PIP) install -e .

check-dist:
	$(PYTHON) -m twine check dist/*

publish: clean build check-dist
	$(PYTHON) -m twine upload dist/*

dev-setup:
	$(PIP) install build twine

test-publish: clean build check-dist
	$(PYTHON) -m twine upload --repository testpypi dist/* 