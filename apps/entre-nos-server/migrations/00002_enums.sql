-- +goose Up
create type financeiro.moeda           as enum ('BRL', 'USD', 'EUR');
create type financeiro.recorrencia     as enum ('semanal', 'mensal', 'anual', 'unica');
create type financeiro.fonte_renda     as enum ('salario', 'pix_devolucao', 'receita_extraordinaria');
create type financeiro.banco           as enum ('itau', 'inter', 'caixa', 'mercado_pago');
create type financeiro.bandeira        as enum ('visa', 'mastercard', 'elo');
create type financeiro.origem_despesa  as enum ('manual', 'fatura');
create type financeiro.status_importacao as enum ('pendente', 'confirmado', 'erro');
create type financeiro.status_linha    as enum ('pendente', 'confirmada', 'ignorada');
create type financeiro.status_aporte   as enum ('planejado', 'guardado', 'nao_guardado');

-- +goose Down
drop type financeiro.status_aporte;
drop type financeiro.status_linha;
drop type financeiro.status_importacao;
drop type financeiro.origem_despesa;
drop type financeiro.bandeira;
drop type financeiro.banco;
drop type financeiro.fonte_renda;
drop type financeiro.recorrencia;
drop type financeiro.moeda;
