-- ============================================================
-- Bootstrap: roda como 'postgres' (o bootstrap superuser) ANTES
-- do migrate.sh. Cria o supabase_admin que o migrate.sh usa
-- para conectar e rodar as migrations internas.
-- ============================================================

-- Cria o supabase_admin (o migrate.sh precisa se conectar como ele)
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'supabase_admin') THEN
    CREATE ROLE supabase_admin SUPERUSER LOGIN CREATEROLE CREATEDB REPLICATION BYPASSRLS;
  END IF;
END
$$;
