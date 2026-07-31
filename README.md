# WebMUN

USPCodeLab project for managing and hosting real time Model United Nations 

# Prerequisites

This project stack is composed of:
- React 19 + Vite 8 as the frontend stack 
- Tailwind, Shadcn as UI libraries
- Python 3.11, FastAPI, pytest and ruff
- Supabase for database and auth
- Redis for in-memory database

Further improvements are planned to make this a cloud-native application.

# Local development

To start the backend, frontend and supabase, issue:

```
make dev
```

To stop these services, do:

```
make stop
```

# Docs

To build and use documentation with a website, we use MkDocs. To start out, with `uv`, create a `venv-docs` and activate it:

```bash
$uv venv venv-docs

$source venv-docs/bin/activate
```

Then, install MkDocs:

```bash
$ uv pip install mkdocs
```

Lastly, build the documentation:

```bash
$ make docs-build
```

This will output a `site/` directory containing the static site. To serve the website in localhost:

```bash
$ make docs-serve
```
