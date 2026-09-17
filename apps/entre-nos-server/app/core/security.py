from uuid import UUID
from typing import AsyncGenerator
import jwt
from pydantic import BaseModel
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import asyncpg

from app.core.config import settings

# 1. Cria o esquema Bearer (adiciona o botão verde "Authorize" no Swagger /docs)
bearer_scheme = HTTPBearer(auto_error=True)

class CurrentUser(BaseModel):
    """Dados básicos do usuário logado extraídos do token do GoTrue."""
    id: UUID
    email: str | None = None
    role: str = "authenticated"

async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> CurrentUser:
    """Valida o JWT do Supabase GoTrue e retorna os dados do usuário."""
    token = credentials.credentials
    try:
        payload = jwt.decode (
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            audience="authenticated", # Exige estritamente que o token seja de um usuário autenticado
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado. Faça login novamente."
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido.",
        )
    
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token sem identificador de usuário (sub).",
        )

    return CurrentUser(
        id=UUID(sub),
        email=payload.get("email"),
        role=payload.get("role", "authenticated"),
    )

async def get_db(
    request: Request,
    user: CurrentUser = Depends(get_current_user),
) -> AsyncGenerator[asyncpg.Connection, None]:
    """
    Dependency injetável que:
    1. Pega uma conexão da pool
    2. Inicia uma transação segura
    3. Ativa o RLS com o UUID do usuário logado
    4. Entrega a conexão pro endpoint
    """
    pool: asyncpg.Pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.transaction():
            # Assume a role authenticated
            await conn.execute("SET LOCAL ROLE authenticated;")
            # Define o auth.uid() no Postgres para as regras de RLS
            await conn.execute(
                "SELECT set_config('request.jwt.claim.sub', $1, true);",
                str(user.id),
            )
            await conn.execute(
                "SELECT set_config('request.jwt.claim.role', $1, true);",
                user.role,
            )

            yield conn