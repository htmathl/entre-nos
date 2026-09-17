"""
gerar_chaves.py — entre-nós
Gera todas as chaves/segredos necessários para o .env do Supabase self-hosted.

Uso:
    python gerar_chaves.py            → imprime no terminal
    python gerar_chaves.py --env      → sobrescreve o .env com os valores gerados

Atenção: segredos gerados são únicos por execução. Guarde o .env em local seguro.
"""

import hmac
import hashlib
import base64
import json
import time
import secrets
import string
import argparse
from pathlib import Path

# ── helpers ──────────────────────────────────────────────────────────────────

def urlsafe(n_bytes: int) -> str:
    """Gera n_bytes aleatórios e retorna como base64url (sem +, /, =)."""
    return secrets.token_urlsafe(n_bytes)

def alphanumeric(n_chars: int) -> str:
    """Gera string alfanumérica de exatamente n_chars caracteres."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(n_chars))

def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

def make_jwt(payload: dict, secret: str) -> str:
    """Gera um JWT HS256 assinado com secret."""
    header = b64url(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())
    body   = b64url(json.dumps(payload,                         separators=(",", ":")).encode())
    msg    = f"{header}.{body}".encode()
    sig    = b64url(hmac.new(secret.encode(), msg, hashlib.sha256).digest())
    return f"{header}.{body}.{sig}"

# ── geração ──────────────────────────────────────────────────────────────────

def gerar_chaves() -> dict:
    now = int(time.time())
    exp = now + 10 * 365 * 24 * 3600  # 10 anos

    jwt_secret = urlsafe(48)           # >= 32 chars, URL-safe

    anon_key = make_jwt(
        {"role": "anon",         "iss": "supabase", "iat": now, "exp": exp},
        jwt_secret,
    )
    service_key = make_jwt(
        {"role": "service_role", "iss": "supabase", "iat": now, "exp": exp},
        jwt_secret,
    )

    return {
        "POSTGRES_PASSWORD":    urlsafe(32),       # URL-safe (sem +/=)
        "JWT_SECRET":           jwt_secret,
        "JWT_EXPIRY":           "3600",
        "PG_META_CRYPTO_KEY":   urlsafe(32),       # URL-safe
        "SECRET_KEY_BASE":      urlsafe(64),       # URL-safe, longo pro Realtime/Phoenix
        "REALTIME_DB_ENC_KEY":  alphanumeric(16),  # exatamente 16 chars ASCII (AES-128)
        "ANON_KEY":             anon_key,
        "SERVICE_ROLE_KEY":     service_key,
    }

# ── .env template ─────────────────────────────────────────────────────────────

ENV_TEMPLATE = """\
# ============================================================
# entre-nós — Supabase (compose enxuto) — variáveis de ambiente
# Gerado automaticamente por gerar_chaves.py em {timestamp}
# ⚠️  NUNCA suba este arquivo para o git.
# ============================================================

# --- Postgres ---
POSTGRES_HOST=db
POSTGRES_DB=postgres
POSTGRES_PORT=5432
POSTGRES_PASSWORD={POSTGRES_PASSWORD}

# --- JWT ---
JWT_SECRET={JWT_SECRET}
JWT_EXPIRY={JWT_EXPIRY}

# --- meta / studio ---
PG_META_CRYPTO_KEY={PG_META_CRYPTO_KEY}
STUDIO_DEFAULT_ORGANIZATION=entre-nos
STUDIO_DEFAULT_PROJECT=entre-nos

# --- URLs ---
SUPABASE_PUBLIC_URL=http://localhost:54321
SITE_URL=http://localhost:3000
API_EXTERNAL_URL=http://localhost:54321
ADDITIONAL_REDIRECT_URLS=http://localhost:3000

# --- Chaves de API ---
ANON_KEY={ANON_KEY}
SERVICE_ROLE_KEY={SERVICE_ROLE_KEY}

# --- gotrue ---
DISABLE_SIGNUP=false
ENABLE_EMAIL_AUTOCONFIRM=true

# --- realtime ---
SECRET_KEY_BASE={SECRET_KEY_BASE}
REALTIME_DB_ENC_KEY={REALTIME_DB_ENC_KEY}
"""

# ── main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Gera chaves para o .env do Supabase entre-nós")
    parser.add_argument("--env", action="store_true", help="Escreve (ou sobrescreve) o .env")
    args = parser.parse_args()

    chaves = gerar_chaves()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    env_content = ENV_TEMPLATE.format(timestamp=timestamp, **chaves)

    # sempre imprime no terminal
    print("\n" + "=" * 60)
    print("  CHAVES GERADAS — entre-nós Supabase")
    print("=" * 60)
    for k, v in chaves.items():
        if k in ("ANON_KEY", "SERVICE_ROLE_KEY"):
            print(f"\n{k}:\n  {v}")
        else:
            print(f"{k}: {v}")
    print("\n" + "=" * 60)

    if args.env:
        env_path = Path(__file__).parent / ".env"
        env_path.write_text(env_content, encoding="utf-8")
        print(f"\n✅ .env escrito em: {env_path}")
        print("   Lembre-se: não suba esse arquivo pro git!\n")
    else:
        print("\nDica: rode com --env para escrever direto no .env")
        print()


if __name__ == "__main__":
    main()
