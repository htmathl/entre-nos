from contextlib import asynccontextmanager
import asyncpg
from fastapi import FastAPI
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: abre a pool de conexões com o Postgres
    app.state.pool = await asyncpg.create_pool(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        database=settings.POSTGRES_DB,
        min_size=2,
        max_size=10,
    )
    print("✅ Conectado ao PostgreSQL com sucesso!")

    yield

    # Shutdown: fecha a pool ao encerrar o servidor
    await app.state.pool.close()
    print("🛑 Conexões com o PostgreSQL encerradas.")