# Getting Started

As a developer, you'll need the following:

- Node 22+
- Node.js version manager (such as `nvm`)
- `npm`
- `uv` for backend project management 
- Docker and Docker Compose 
- Supabase (through the CLI)
- GNU Make (optional, but recommended for deploying the project as dev/prod)

## Local setup 

Use your editor of preference (VSCode, Nvim, etc). WebMUN uses Ruff for code style formatting for Python code and Prettier for frontend style.

Keep in mind you'll need to fill the `.env` variables on `backend/.env` and `frontend/.env.local`. Use the existing `.env.example` files as a reference. In particular, you'll need Supabase secret variables to deploy a dev server, so you can start the Supabase service first to grab those:

```bash
supabase start || npx supabase start
```

This will output things like Supabase project URL, Database URL, etc. Grab those and populate the `.env` files.

Additionally, our backend uses asymmetric JWT signing keys for local token validation. This is automatically fetched by the backend.


## Deploying the development server 

To start all services needed (Frontend DEV server, backend server, Supabase), use a `make` command on the project root:

```bash
make dev
```

This orchestrates, through simple commands, everything needed. To stop the services, use:

```bash 
make stop
```

If needed, you might start only one specific service, such as frontend. For that, you can do:

```bash
# inside frontend/
npm run dev
```

and 

```bash 
# inside backend/ (not recommended since backend needs the database running)
uv run .
```

You can verify the app works (or not) by going to the frontend local URL (`http://localhost:5173/`), or backend docs (`http://localhost:8000/docs#/`), or Supabase Studio URL (`http://localhost:54323/`)
