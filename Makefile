.PHONY: clean install build test lint mplayer docs

PYTHON=python3
RM=rm -f -v
PIP=pip3
NPM=npm

clean:
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete

install:
	$(PPI) install -r requirements.txt
	$(PYTHON) setup.py install

build:
	$(PIP) install wheel
	$(PYTHON) setup.py sdist bdist_wheel

test:
	$(PYTHON) -m tests -a

lint:
	$(PYTHON) scripts/lint.py

mplayer:
	$(PYTHON) MPlayer/MPlayer.py

docs:
	cd docs;$(NPM) run localhost

upload_mplayer:
	$(PYTHON) scripts/build_mplayer_zip.py
	curl --upload-file ./MPlayer.zip https://transfer.sh/MPlayer.zip
	rm MPlayer.zip
