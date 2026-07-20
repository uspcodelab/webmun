# Supabase development

Ensure you have Supabase CLI installed as a dependency.

Workflow docs can be viewed (here)[https://supabase.com/docs/guides/local-development/database-migrations].
You can opt for using the manual way or the GUI way.

Supabase is used for:
- DB provisioning. For backend workflow, we query PostgreSQL directly instead of querying through Supabase's HTTP API. 
    - This gives us full raw SQL flexibility, with the caveat of managing security by ourselves.
    - Thus, we only use this direct connection on the backend, since it is expected to have privileges.
- Auth. Frontend queries Supabase Auth directly and stores credentials, tokens, etc. Backend uses DB secrety key to locally verify if a key is valid, expired, has been tampered with, etc.

## Workflow

Start Supabase by issuing (on the project root directory):

```
supabase start
```

This will pull the necessary images and start their containers. This will output infos you might need, such as:
- Authentication Keys: save `Secret` to `SUPABASE_JWT_SECRET` on `.env`
- REST, DATABASE Url: save to `SUPABASE_URL` and `DATABASE_URL`, respectivelly

Then, you can run existing migrations (or apply new ones) with:

```
supabase db reset
```

When you want to create/change a table, use (prefer to use a name that explicitly tells what you're doing):

```
supabase migration new <name_of_migration>
```

This will create a `.sql` file under `migrations/`. You can put SQL in there. Take a look at the docs for further references.

If you don't want to use the terminal, fell free to use Supabase Studio by going to the **project url**.
