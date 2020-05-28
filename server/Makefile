FLAGS=


pep8:
	# Use black to format all python files, then flake8 to check them.
	black . --exclude "/(\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|\.egg|_build|buck-out|build|dist)/"
	flake8 

run:
	python -m cephdissectionserver -c example/server.conf

test:
	pytest tests

clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name '@*' `
	rm -f `find . -type f -name '#*#' `
	rm -f `find . -type f -name '*.orig' `
	rm -f `find . -type f -name '*.rej' `
	rm -f .coverage
	rm -rf coverage
	rm -rf build
	rm -rf htmlcov
	rm -rf dist

.PHONY: pep8 run clean test
