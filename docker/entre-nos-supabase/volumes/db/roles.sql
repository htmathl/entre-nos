-- ============================================================
-- roles.sql — roda como 'postgres' via migrate.sh (init-scripts/*.sql)
-- Ajusta senhas e ownership para os roles internos do Supabase.
-- Nota: supabase_functions_admin não existe nesta versão da imagem.
-- ============================================================

\set pgpass `echo "$POSTGRES_PASSWORD"`

-- Ajusta senhas dos roles que de fato existem nesta imagem
ALTER USER authenticator         WITH PASSWORD :'pgpass';
ALTER USER pgbouncer             WITH PASSWORD :'pgpass';
ALTER USER supabase_auth_admin   WITH PASSWORD :'pgpass';
ALTER USER supabase_storage_admin WITH PASSWORD :'pgpass';
ALTER USER supabase_admin        WITH PASSWORD :'pgpass';

-- Transfere ownership das funções auth.* para supabase_auth_admin
-- (a imagem as cria como postgres, mas o gotrue precisa ser o dono pra recriá-las)
ALTER FUNCTION auth.uid()   OWNER TO supabase_auth_admin;
ALTER FUNCTION auth.role()  OWNER TO supabase_auth_admin;
ALTER FUNCTION auth.email() OWNER TO supabase_auth_admin;
