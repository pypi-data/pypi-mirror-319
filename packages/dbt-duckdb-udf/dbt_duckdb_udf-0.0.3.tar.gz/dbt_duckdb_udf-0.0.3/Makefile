clean:
	rm -rf dist/ build/ *.egg-info/
build:clean
	python -m build
upload:build
	python -m twine upload --repository pypi dist/*