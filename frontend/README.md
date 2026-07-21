# Frontend repository

This project uses **React + TypeScript + Vite**, in addition to Shadcn for components, React Router for routing capabilities, and Zustand for state management.

# Setup 

Prerequisites: Node 20+

1. Install packages required for the project and copy the .env

```bash
npm install
cp .env.example .env.local
```

2. Run the project using `npm`
```bash
npm run dev
```

# Supabase Auth

We use Supabase's SDK in order to connect to the Auth API and login users. You can check more on the official docs.
I you want to know how to develop with Supabase Auth, this [guide](https://supabase.com/docs/guides/getting-started/tutorials/with-react?queryGroups=database-method&database-method=dashboard) might be good.
