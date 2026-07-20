# Supabase development

Ensure you have Supabase CLI installed as a dependency.

Workflow docs can be viewed (here)[https://supabase.com/docs/guides/local-development/database-migrations].
You can opt for using the manual way or the GUI way.

Supabase is used for:
- DB provisioning. For backend workflow, we query PostgreSQL directly instead of querying through Supabase's HTTP API. 
    - This gives us full raw SQL flexibility, with the caveat of managing security by ourselves.
    - Thus, we only use this direct connection on the backend, since it is expected to have privileges.
- Auth. Frontend queries Supabase Auth directly and stores credentials, tokens, etc. Backend uses DB secrety key to locally verify if a key is valid, expired, has been tampered with, etc.
