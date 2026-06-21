.PHONY: sync test lint typecheck run

sync:
	uv sync

test:
	uv run pytest

lint:
	uv run ruff check src tests

typecheck:
	uv run mypy

run:
	PYTHONPATH=src uv run python -m app.main
