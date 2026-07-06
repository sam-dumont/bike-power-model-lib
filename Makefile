# bike-power-model — developer tasks. Everything runs through `uv`.
# `uv` is the only prerequisite: https://docs.astral.sh/uv/

.DEFAULT_GOAL := help
.PHONY: help sync test offline lint format format-check check build wheel-smoke audit gitleaks clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

sync: ## Install the project + dev dependencies into the uv venv
	uv sync --extra dev

test: ## Run the test suite with coverage
	uv run pytest --cov=bike_power_model --cov-report=term-missing

offline: ## Run the suite with sockets blocked (the offline gate)
	uv run pytest --disable-socket

lint: ## Lint with ruff
	uv run ruff check src/ tests/ scripts/

format: ## Auto-format with ruff
	uv run ruff format src/ tests/ scripts/

format-check: ## Check formatting without writing
	uv run ruff format --check src/ tests/ scripts/

check: lint format-check test offline ## Everything CI runs, locally

build: ## Build sdist + wheel into dist/
	uv build

wheel-smoke: build ## Build then import-test the wheel in an isolated env
	uv run --isolated --no-project \
		--with dist/bike_power_model-*.whl \
		python scripts/wheel_smoke.py

audit: ## Dependency CVE audit against the locked tree
	uv export --frozen --no-emit-project --format requirements-txt -o audit-requirements.txt
	uvx pip-audit -r audit-requirements.txt
	@rm -f audit-requirements.txt

gitleaks: ## Scan the full git history for secrets (needs the gitleaks binary)
	@command -v gitleaks >/dev/null 2>&1 \
		&& gitleaks git --no-banner \
		|| echo "gitleaks not installed: 'brew install gitleaks' (CI runs it via the gitleaks Action)"

clean: ## Remove build + cache artefacts
	rm -rf dist build *.egg-info .pytest_cache .coverage htmlcov audit-requirements.txt
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
