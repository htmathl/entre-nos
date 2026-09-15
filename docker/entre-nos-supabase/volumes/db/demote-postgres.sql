-- ============================================================
-- demote-postgres (versão adaptada para Docker self-hosted)
-- 
-- NOTA: O ALTER ROLE postgres NOSUPERUSER foi REMOVIDO
-- intencionalmente. No PG17, o bootstrap superuser (postgres)
-- não pode remover seu próprio atributo SUPERUSER — isso é uma
-- proteção do PG17 e não se aplica à AMI original do Supabase.
-- Para homelab privado, postgres como superuser é seguro.
-- 
-- Os GRANTs abaixo são mantidos para garantir compatibilidade
-- com as demais migrations.
-- ============================================================

-- migrate:up

GRANT ALL ON DATABASE postgres TO postgres;
GRANT ALL ON SCHEMA auth TO postgres;
GRANT ALL ON SCHEMA extensions TO postgres;
GRANT ALL ON ALL TABLES IN SCHEMA auth TO postgres;
GRANT ALL ON ALL TABLES IN SCHEMA extensions TO postgres;
GRANT ALL ON ALL SEQUENCES IN SCHEMA auth TO postgres;
GRANT ALL ON ALL SEQUENCES IN SCHEMA extensions TO postgres;
GRANT ALL ON ALL ROUTINES IN SCHEMA auth TO postgres;
GRANT ALL ON ALL ROUTINES IN SCHEMA extensions TO postgres;

do $$
begin
  if exists (select from pg_namespace where nspname = 'storage') then
    GRANT ALL ON SCHEMA storage TO postgres;
    GRANT ALL ON ALL TABLES IN SCHEMA storage TO postgres;
    GRANT ALL ON ALL SEQUENCES IN SCHEMA storage TO postgres;
    GRANT ALL ON ALL ROUTINES IN SCHEMA storage TO postgres;
  end if;
end $$;

-- ALTER ROLE postgres NOSUPERUSER ... OMITIDO (ver nota acima)

-- migrate:down
