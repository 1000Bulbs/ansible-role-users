.DEFAULT_GOAL := help

.PHONY: install-pip-upgrade install-lint-deps install-format-deps install-hooks-deps install-hooks \
        test-hooks uninstall-hooks lint format check install-molecule-deps test install-ci-deps ci \
        setup help

install-pip-upgrade:
	python3 -m pip install --upgrade pip

install-lint-deps: install-pip-upgrade  ## Install lint dependencies
	pip install pre-commit ruff yamllint ansible-lint
	npm install -g markdownlint-cli2

install-format-deps: install-pip-upgrade  ## Install format dependencies
	pip install ruff

install-hooks-deps: install-lint-deps install-format-deps  ## Install pre-commit dependencies
	pip install pre-commit

install-hooks: install-hooks-deps  ## Register pre-commit Git hook
	pre-commit install

test-hooks:  ## Run all pre-commit hooks on all files
	pre-commit run --all-files

uninstall-hooks:  ## Uninstall pre-commit hook from .git/hooks
	pre-commit uninstall

lint:  ## Run lint checks (ruff, yamllint, ansible-lint, markdownlint-cli2)
	ruff check .
	yamllint .
	ansible-lint .
	markdownlint-cli2 "**/*.md"

format:  ## Run format checks (ruff)
	ruff format .

check: lint format ## Run lint and format checks

install-molecule-deps: install-pip-upgrade  ## Install molecule dependencies
	pip install -r requirements.txt

test:  ## Run molecule tests
	molecule test

install-ci-deps: ## Install CI dependencies
	@if [ "$$(uname)" = "Darwin" ]; then \
		brew install act; \
	else \
		echo "Skipping install: macOS not detected."; \
	fi

ci: ## Run GitHub Actions locally with act
	@if command -v act >/dev/null 2>&1; then \
		act; \
	else \
		echo "'act' not found. Run 'make install-ci-deps' to install it."; \
	fi

setup: install-hooks install-molecule-deps install-ci-deps ## Install all dependencies and setup environment

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "%-20s %s\n", $$1, $$2}'
