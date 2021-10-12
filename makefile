.PHONY: test build
test:
	PYTHONPATH=. pytest
build:
	python -m build
	twine check dist/*
test-upload:
	twine upload --repository testpypi dist/*
upload:
	twine upload dist/*