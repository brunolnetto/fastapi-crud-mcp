# Justfile for FastAPI Project

# Create dependencies environment
env:
    uv venv

# Install project dependencies
sync:
    uv sync

# Run the FastAPI development server
serve:
    .venv/bin/python -m uvicorn backend.server.main:app --reload

# Run tests using pytest
test:
    .venv/bin/python -m pytest --cov=backend/server --cov-report=term-missing

# Format code using black
format:
    ruff check --fix .

# Clean up generated files
clean:
    rm -rf __pycache__ .pytest_cache

# Run the development environment (install, run, and watch for changes)
dev:
    just env
    just sync
    just serve

