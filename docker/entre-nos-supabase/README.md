# 🐘 Supabase Self-Hosted (entre-nós)

Stack enxuta do Supabase configurada especificamente para o homelab do casal.
Contém apenas os serviços essenciais para reduzir consumo de memória (~650 MB de RAM):

- **db** (`PostgreSQL 17`): Banco de dados principal e persistente.
- **gotrue** (`v2.196.0`): Autenticação de usuários e emissão de JWT.
- **meta** (`v0.99.0`): API interna de metadados para o Studio.
- **studio** (`Next.js dashboard`): Interface gráfica web de administração.
- **realtime** (`v2.134.10`): Sincronização em tempo real via WebSockets.

---

## 🌐 Portas Expostas

| Serviço | Porta Local | Descrição |
|---|---|---|
| **Studio** | `http://localhost:54323` | Dashboard visual (SQL editor, tabelas) |
| **GoTrue** | `http://localhost:54321` | API de Autenticação / Auth endpoints |
| **Postgres** | `localhost:54322` | Conexão direta SQL (DBeaver, TablePlus, etc.) |
| **Realtime** | `http://localhost:4000` | Servidor WebSocket para streaming de eventos |

---

## 🚀 Guia de Configuração (Do Zero)

### 1. Gerar as Chaves de Ambiente
Gera todas as senhas seguras, URLs-safe e JWTs necessários (`ANON_KEY`, `SERVICE_ROLE_KEY`):

```powershell
python gerar_chaves.py --env
```
> ⚠️ **Atenção:** O arquivo `.env` gerado nunca deve ser comitado no Git.

---

### 2. Subir a Stack
Na pasta raiz do docker (`docker/`):

```powershell
docker compose up -d
```

Verifique se todos os containers estão saudáveis:
```powershell
docker compose ps
```

---

### 3. Rodar as Migrations do Banco (`goose`)
Aplica os schemas (`nucleo`, `financeiro`), tabelas, enums e políticas de RLS:

```powershell
# Estando na pasta docker/entre-nos-supabase/:
goose -dir migrations postgres "host=localhost port=54322 dbname=postgres user=postgres password=SUA_POSTGRES_PASSWORD sslmode=disable" up
```
*(Substitua `SUA_POSTGRES_PASSWORD` pela senha definida no seu `.env`)*.

---

### 4. Cadastrar os Usuários da Casa
Execute o script interativo para cadastrar você e seu parceiro(a):

```powershell
python gotrue.py
```
O script cadastra o usuário no GoTrue e imprime o comando SQL para registrar os membros na tabela `nucleo.pessoa`.

Para executar o SQL impresso no banco via Docker:
```powershell
docker exec entre-nos-db-1 psql -U postgres -c "
INSERT INTO nucleo.pessoa (id, nome_pessoa, apelido) VALUES
  ('<UUID_1>', 'Nome 1', 'voce'),
  ('<UUID_2>', 'Nome 2', 'namorado');
"
```

---

### 5. Travar Novos Cadastros (Segurança)
Após cadastrar os únicos dois membros da casa, desative novos cadastros editando o `.env`:

```env
DISABLE_SIGNUP=true
```

E reinicie apenas o serviço de autenticação:
```powershell
docker compose restart gotrue
```
