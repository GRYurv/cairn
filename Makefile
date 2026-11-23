.PHONY: test lint index example

test:
	python -m pytest -q

lint:
	python -m cairn lint examples/vault

example:
	python -m cairn index examples/vault --out site
	@echo "wrote site/index.html"
