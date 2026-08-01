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

To start the backend, frontend and supabase, issue:

```
make dev
```

To stop these services, do:

```
make stop
```
