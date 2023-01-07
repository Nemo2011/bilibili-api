.PHONY: build clean docs install lint onlinedocs test

PYTHON=python3
RM=rm -f -v
PIP=pip3
NPM=npm

bdist:
	$(PYTHON) setup.py bdist_wheel

build:
	$(PIP) install wheel
	$(PYTHON) setup.py sdist bdist_wheel

clean:
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete

docs:
	cd docs;$(NPM) run localhost

install:
	$(PIP) install -r requirements.txt
	$(PYTHON) setup.py install

lint:
	$(PYTHON) scripts/lint.py

onlinedocs:
	$(PYTHON) -m bilibili_api.tools.opendocs

sdist:
	$(PYTHON) setup.py sdist

test:
	$(PYTHON) -m tests -a
