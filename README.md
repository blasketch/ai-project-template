# ai-project-template

Copier template that generates a Python Clean Architecture project
with configurable layers: FastAPI, async SQLAlchemy, and Typer CLI.

## Usage

```bash
copier copy gh:user/ai-project-template path/to/new-project
```

## What's Generated

- 4-layer `src/` layout with import-linter enforcement
- pydantic-settings configuration with secret handling
- structlog structured logging
- Quality gates: Ruff, MyPy strict, pre-commit parity
- 3-tier pytest: unit, integration (testcontainers), e2e
- Multi-stage Docker image and Compose dev environment
- MkDocs Material documentation site
