-- +goose Up

-- ── RLS ──────────────────────────────────────────────────────────────────────
-- nucleo.pessoa: só leitura pra authenticated; escrita só via service_role (seed)
alter table nucleo.pessoa enable row level security;
create policy "membros leem a casa" on nucleo.pessoa
    for select using (true);

-- financeiro.*: membro da casa lê e escreve tudo
alter table financeiro.categoria        enable row level security;
alter table financeiro.cartao           enable row level security;
alter table financeiro.importacao       enable row level security;
alter table financeiro.importacao_linha enable row level security;
alter table financeiro.compra_parcelada enable row level security;
alter table financeiro.despesa          enable row level security;
alter table financeiro.entrada          enable row level security;
alter table financeiro.reserva          enable row level security;
alter table financeiro.aporte           enable row level security;

create policy "membro da casa" on financeiro.categoria
    for all using (auth.uid() in (select id from nucleo.pessoa));
create policy "membro da casa" on financeiro.cartao
    for all using (auth.uid() in (select id from nucleo.pessoa));
create policy "membro da casa" on financeiro.importacao
    for all using (auth.uid() in (select id from nucleo.pessoa));
create policy "membro da casa" on financeiro.importacao_linha
    for all using (auth.uid() in (select id from nucleo.pessoa));
create policy "membro da casa" on financeiro.compra_parcelada
    for all using (auth.uid() in (select id from nucleo.pessoa));
create policy "membro da casa" on financeiro.despesa
    for all using (auth.uid() in (select id from nucleo.pessoa));
create policy "membro da casa" on financeiro.entrada
    for all using (auth.uid() in (select id from nucleo.pessoa));
create policy "membro da casa" on financeiro.reserva
    for all using (auth.uid() in (select id from nucleo.pessoa));
create policy "membro da casa" on financeiro.aporte
    for all using (auth.uid() in (select id from nucleo.pessoa));

-- ── Grants ───────────────────────────────────────────────────────────────────
-- O FastAPI conecta como 'authenticator' e faz SET LOCAL ROLE authenticated.
-- O authenticated precisa de acesso aos schemas e tabelas.

grant usage on schema nucleo     to authenticator;
grant usage on schema financeiro to authenticator;

grant usage on schema nucleo     to authenticated;
grant usage on schema financeiro to authenticated;

-- nucleo.pessoa: só leitura
grant select on nucleo.pessoa to authenticated;

-- financeiro.*: leitura e escrita completa
grant select, insert, update, delete on
    financeiro.categoria,
    financeiro.cartao,
    financeiro.importacao,
    financeiro.importacao_linha,
    financeiro.compra_parcelada,
    financeiro.despesa,
    financeiro.entrada,
    financeiro.reserva,
    financeiro.aporte
to authenticated;

-- sequences (necessário para serial/insert)
grant usage, select on all sequences in schema financeiro to authenticated;

-- +goose Down
-- revoga grants
revoke all on all tables    in schema financeiro from authenticated;
revoke all on all sequences in schema financeiro from authenticated;
revoke all on nucleo.pessoa from authenticated;
revoke usage on schema financeiro from authenticated;
revoke usage on schema nucleo     from authenticated;
revoke usage on schema financeiro from authenticator;
revoke usage on schema nucleo     from authenticator;

-- remove policies
drop policy "membro da casa" on financeiro.aporte;
drop policy "membro da casa" on financeiro.reserva;
drop policy "membro da casa" on financeiro.entrada;
drop policy "membro da casa" on financeiro.despesa;
drop policy "membro da casa" on financeiro.compra_parcelada;
drop policy "membro da casa" on financeiro.importacao_linha;
drop policy "membro da casa" on financeiro.importacao;
drop policy "membro da casa" on financeiro.cartao;
drop policy "membro da casa" on financeiro.categoria;
drop policy "membros leem a casa" on nucleo.pessoa;

-- desativa RLS
alter table financeiro.aporte           disable row level security;
alter table financeiro.reserva          disable row level security;
alter table financeiro.entrada          disable row level security;
alter table financeiro.despesa          disable row level security;
alter table financeiro.compra_parcelada disable row level security;
alter table financeiro.importacao_linha disable row level security;
alter table financeiro.importacao       disable row level security;
alter table financeiro.cartao           disable row level security;
alter table financeiro.categoria        disable row level security;
alter table nucleo.pessoa               disable row level security;
