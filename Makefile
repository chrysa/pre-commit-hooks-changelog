build:
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf build dist pre_commit_hooks_changelog.egg-info .mypy_cache

deploy: clean build pypi pypi-test
	git push

install:
	pip3 install -e .
	pre-commit install

pypi:
	pip3 install -e .[push]
	python3 -m twine upload dist/*

pypi-test:
	pip3 install -e .[push]
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

test:
	pip3 install -e .[test]
