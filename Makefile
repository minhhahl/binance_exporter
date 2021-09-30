clear-pyc:
	find . -name "*.pyc" -exec rm -f {} \;

test:
	python -m unittest discover -s tests/ -p 'test_*.py'

coverage:
	 coverage run -m unittest discover -s tests/ -p 'test_*.py'; coverage report -m

run:
	python binance_exporter/exporter.py

install-requirements:
	pip install -r requirements.txt

lint:
	pylint binance_exporter/ -f colorized