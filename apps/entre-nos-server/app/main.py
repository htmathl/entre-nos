from fastapi import FastAPI, Request
from app.core.database import lifespan

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
