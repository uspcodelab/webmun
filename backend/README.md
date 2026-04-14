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
