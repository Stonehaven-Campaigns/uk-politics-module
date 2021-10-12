.PHONY: test build
test:
	PYTHONPATH=. pytest
build:
	python -m build --sdist
	python -m build --wheel
	twine check dist/*
test-upload:
	twine upload --repository testpypi dist/*
upload:
	twine upload dist/*