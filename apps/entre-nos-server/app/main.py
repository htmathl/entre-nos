from fastapi import FastAPI, Request, Depends, HTTPException, status
import asyncpg
from app.core.database import lifespan
from app.core.security import get_current_user, get_db, CurrentUser

app = FastAPI(
    title="entre-nós API",
    version="0.1.0",
    description="API do app privado do casal (módulo financeiro)",
    lifespan=lifespan,
)

@app.get("/health")
def healthcheck():
    return {"status": "ok", "app": "entre-nos-server"}

@app.get("/health/db")
async def healthcheck_db(request: Request):
    """Testa se a API consegue executar queries no Postgres"""

    pool = request.app.state.pool
    async with pool.acquire() as conn:
        versao = await conn.fetchval("SELECT version();")

        async with conn.transaction():
            await conn.execute("SET LOCAL ROLE authenticated;")
            total_pessoas = await conn.fetchval("SELECT count(*) FROM nucleo.pessoa;")

    return {
        "status": "connected",
        "postgres_version": versao,
        "total_pessoas_cadastradas": total_pessoas,
    }

@app.get("/me")
async def get_me(
    current_user: CurrentUser = Depends(get_current_user),
    conn: asyncpg.Connection = Depends(get_db),
):
    """
    Rota protegida:
    1. Exige token JWT válido (GoTrue) com aud: 'authenticated'.
    2. Usa o get_db com RLS ativo.
    3. Busca os dados da pessoa logada na tabela nucleo.pessoa.
    """
    row = await conn.fetchrow(
        "SELECT id, nome_pessoa, apelido FROM nucleo.pessoa WHERE id = $1;",
        current_user.id,
    )
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pessoa não encontrada no cadastro da casa.",
        )

    return {
        "user_id": str(row["id"]),
        "nome": row["nome_pessoa"],
        "apelido": row["apelido"],
        "email": current_user.email,
        "role": current_user.role,
    }