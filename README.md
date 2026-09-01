[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=uspcodelab_webmun&metric=coverage)](https://sonarcloud.io/summary/new_code?id=uspcodelab_webmun)
[![CI](https://github.com/uspcodelab/webmun/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/uspcodelab/webmun/actions/workflows/ci.yml)
![FastAPI](https://img.shields.io/badge/FastAPI-005571.svg?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)

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

For automated recipes, this project uses `Just`. Ensure you have it installed.

To start the backend, frontend and supabase, issue:

```
just dev
```

To stop these services, do:

```
just stop
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
$ just docs-build
```

This will output a `site/` directory containing the static site. To serve the website in localhost:

```bash
$ just docs-serve
```
