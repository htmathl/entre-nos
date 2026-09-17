-- +goose Up

-- nucleo.pessoa — membros da casa (id vem do login Supabase/GoTrue)
create table nucleo.pessoa (
    id          uuid primary key references auth.users(id),
    nome_pessoa text not null,
    apelido     text not null
);

-- tabelas de apoio
create table financeiro.categoria (
    id             serial primary key,
    nome_categoria text not null
);

create table financeiro.cartao (
    id         serial primary key,
    nome_cartao text not null,
    banco      financeiro.banco not null,
    bandeira   financeiro.bandeira
);

-- importação de fatura (um upload = uma linha aqui)
create table financeiro.importacao (
    id               serial primary key,
    fk_id_cartao     int not null references financeiro.cartao(id),
    arquivo_original text not null,
    periodo          text,                          -- '2024-08'
    status           financeiro.status_importacao not null default 'pendente',
    fk_id_pessoa     uuid not null references nucleo.pessoa(id),
    created_at       timestamptz not null default now()
);

-- linhas cruas da fatura (staging — aguardando revisão)
create table financeiro.importacao_linha (
    id                serial primary key,
    fk_id_importacao  int not null references financeiro.importacao(id),
    linha_bruta       text,
    nome_despesa      text not null,
    data_despesa      date not null,
    valor             decimal(10,2) not null,
    total_parcelas    int not null default 1,
    n_parcela         int not null default 1,
    fk_id_categoria   int references financeiro.categoria(id),
    status            financeiro.status_linha not null default 'pendente'
);

-- compra parcelada (agrupa as parcelas de uma compra)
create table financeiro.compra_parcelada (
    id              serial primary key,
    nome            text not null,
    valor_total     decimal(10,2),
    total_parcelas  int not null,
    fk_id_categoria int references financeiro.categoria(id),
    fk_id_pessoa    uuid not null references nucleo.pessoa(id),
    created_at      timestamptz not null default now()
);

-- despesa (saída de dinheiro)
create table financeiro.despesa (
    id                      serial primary key,
    nome_despesa            text not null,
    data_despesa            date not null,
    valor_original          decimal(10,2) not null,
    moeda                   financeiro.moeda not null,
    valor_brl               decimal(10,2) not null,       -- convertido e congelado
    taxa_cambio             decimal(12,6),                -- null se BRL
    n_parcela               int not null default 1,
    origem                  financeiro.origem_despesa not null default 'manual',
    fk_id_importacao        int references financeiro.importacao(id),
    fk_id_compra_parcelada  int references financeiro.compra_parcelada(id),
    fk_id_categoria         int references financeiro.categoria(id),
    fk_id_cartao            int references financeiro.cartao(id),
    fk_id_pessoa            uuid not null references nucleo.pessoa(id),
    created_at              timestamptz not null default now(),
    updated_at              timestamptz not null default now()
);

-- entrada (receita)
create table financeiro.entrada (
    id           serial primary key,
    nome_entrada text not null,
    data_entrada date not null,
    valor        decimal(10,2) not null,
    recorrencia  financeiro.recorrencia not null default 'unica',
    fonte_renda  financeiro.fonte_renda not null,
    fk_id_pessoa uuid not null references nucleo.pessoa(id),
    created_at   timestamptz not null default now(),
    updated_at   timestamptz not null default now()
);

-- reserva (onde fica guardado o dinheiro)
create table financeiro.reserva (
    id           serial primary key,
    nome         text not null,
    banco        financeiro.banco not null,
    meta         decimal(10,2),
    fk_id_pessoa uuid not null references nucleo.pessoa(id),
    created_at   timestamptz not null default now()
);

-- aporte (movimentação dentro de uma reserva)
create table financeiro.aporte (
    id               serial primary key,
    fk_id_reserva    int not null references financeiro.reserva(id),
    valor            decimal(10,2) not null,
    data_prevista    date not null,
    recorrencia      financeiro.recorrencia not null default 'unica',
    status           financeiro.status_aporte not null default 'planejado',
    data_realizacao  date,
    fk_id_pessoa     uuid not null references nucleo.pessoa(id),
    created_at       timestamptz not null default now(),
    updated_at       timestamptz not null default now()
);

-- +goose Down
drop table financeiro.aporte;
drop table financeiro.reserva;
drop table financeiro.entrada;
drop table financeiro.despesa;
drop table financeiro.compra_parcelada;
drop table financeiro.importacao_linha;
drop table financeiro.importacao;
drop table financeiro.cartao;
drop table financeiro.categoria;
drop table nucleo.pessoa;
