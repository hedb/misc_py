.PHONY: all setup format lint pylint test save-check

# Default target to run all checks
all: save-check format lint test

# Check if files might be unsaved
save-check:
	@echo "⚠️  Make sure all files are saved before continuing! ⚠️"
	# @sleep 1

# Target to install development tools and project in editable mode
setup:
	uv pip install -e .[dev]

# Target to format the code
format:
	uv run ruff format .

# Target to run pylint separately
pylint:
	uv run pylint src tests

# Target to lint the code
lint: pylint
	uv run ruff check .
	uvx ty check

# Target to run tests (depends on setup to ensure imports work)
test: setup
	uv run pytest

# Target to run all checks
all: format lint test 