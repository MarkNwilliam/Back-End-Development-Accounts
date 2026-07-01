install:
	pip install -r requirements.txt

test:
	nosetests

lint:
	flake8 service tests --max-line-length=120

pylint:
	pylint service tests --max-line-length=120

all: install lint test
