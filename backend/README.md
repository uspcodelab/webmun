# Backend folder

Prerequisites: uv

This project uses `uv` for package and project management. Ensure you have it installed. Via curl:
```bash 
curl -LsSf https://astral.sh/uv/install.sh | sh
```

# Setup 

`uv` automatically creates a virtual environment and install dependencies based on the `pyproject.toml`, for this, use:
```bash
uv sync
```

Then, to run development server:

```bash
uv run fastapi dev
```

# Linter & Formatter

Backend uses `ruff` for linter and code formatting. See more at [Ruff Docs](https://docs.astral.sh/ruff/). 

To format code: 

```bash 
uv run ruff format . # replace . with the directory you want to format 
```

To lint & check code for errors:

```bash 
uv run ruff check .
```

# Testing

This project borrows ideas from Test-Driven Development. In particular, try to create tests for a new functionality, and only then try to code it.
To run the test suite:

```bash
uv run pytest
```

We deeply recommend contributers to first lint and test their code before sending the commit. This way we make our codebase better. 

# AI usage 

AI usage is welcome here (although not too great if you want to really practice). Be careful to not commit any AI slop. 
Remember: you are responsible for what you commit, so be careful to at least understand what it being done.
