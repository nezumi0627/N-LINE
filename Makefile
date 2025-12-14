
# Variables
PYTHON = python
RYE = rye
MODULE = n_line

.PHONY: all help install dev start fmt check test clean

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

install: ## Install dependencies using rye
	$(RYE) sync

dev: ## Install dev dependencies
	$(RYE) sync --all-features

start: ## Run the application
	$(RYE) run $(PYTHON) -m $(MODULE)

fmt: ## Format code using rye (ruff)
	$(RYE) fmt

check: ## Check code style and linting errors
	$(RYE) check

fix: ## Fix linting errors automatically
	$(RYE) check --fix

clean: ## Clean up cache and temporary files
	rm -rf .ruff_cache
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf src/$(MODULE)/__pycache__
	rm -rf src/$(MODULE)/core/__pycache__
	rm -rf src/$(MODULE)/gui/__pycache__
