-- +goose Up
alter database postgres set timezone = 'America/Sao_Paulo';

create schema nucleo;
create schema financeiro;

-- +goose Down
drop schema financeiro cascade;
drop schema nucleo cascade;
