.PHONY: help test lint clean

PYTHON=python3
PIP=pip3

.DEFAULT: help
help:
	@echo "make test"
	@echo "       run tests"
	@echo "make lint"
	@echo "       run pylint and mypy"
	@echo "make run"
	@echo "       run project"
	@echo "make clean"
	@echo "       clean python cache files"
	@echo "make doc"
	@echo "       build sphinx documentation"

prepare:
	${PYTHON} install.py
	${PIP} install -r requirements.txt
	${PIP} install wheel

install:
	${PYTHON} setup.py install

build:
	${PYTHON} setup.py sdist bdist_wheel

test: 
	${PYTHON} -m tests -a

lint: 
	${PYTHON} -m pylint


clean-pyc:
	@find . -name '*.pyc' -delete
	@find . -name '__pycache__' -type d | xargs rm -fr
	@find . -name '.pytest_cache' -type d | xargs rm -fr

clean:clean-pyc
	@echo "## Clean all data."
