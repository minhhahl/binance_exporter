all: install-requirements-dev lint test coverage run

clear-pyc:
	find . -name "*.pyc" -exec rm -f {} \;

test:
	python -m unittest discover -s tests/ -p 'test_*.py'

coverage:
	 coverage run -m unittest discover -s tests/ -p 'test_*.py'; coverage report -m

coverage-html:
	 coverage run -m unittest discover -s tests/ -p 'test_*.py'; coverage html

run:
	python -m binance_exporter.exporter

debug:
	python -m binance_exporter.exporter -l DEBUG

install-requirements:
	pip install -r requirements.txt

install-requirements-dev:
	pip install -r requirements-dev.txt

lint:
	pylint binance_exporter/ -f colorized --errors-only

lint-all:
	pylint binance_exporter/ -f colorized