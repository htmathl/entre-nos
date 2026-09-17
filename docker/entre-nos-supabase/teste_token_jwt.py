"""
teste_token_jwt.py — entre-nós
Faz login no GoTrue e obtém um access_token JWT para testar rotas no Swagger (/docs).

Uso:
    python teste_token_jwt.py
"""

import getpass
import json
import urllib.error
import urllib.request

GOTRUE_URL = "http://localhost:54321/token?grant_type=password"


def main():
    print("\n" + "=" * 55)
    print("  entre-nós — Obter Token JWT (Login)")
    print("=" * 55)

    email = input("\nE-mail: ").strip()
    if not email:
        print("❌ E-mail não pode ser vazio.")
        return

    senha = getpass.getpass("Senha: ")
    if not senha:
        print("❌ Senha não pode ser vazia.")
        return

    data = json.dumps({"email": email, "password": senha}).encode("utf-8")
    req = urllib.request.Request(
        GOTRUE_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            token = res.get("access_token")

            print("\n✅ Login realizado com sucesso!")
            print("\n" + "-" * 55)
            print("ACCESS TOKEN (JWT):")
            print("-" * 55)
            print(token)
            print("-" * 55)
            print("\n💡 Dica: Copie o token acima e cole no botão 'Authorize' em http://localhost:8000/docs\n")

    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="replace")
        print(f"\n❌ Erro no login ({e.code}): {err_msg}\n")
    except Exception as e:
        print(f"\n❌ Erro de conexão: {e}\n")


if __name__ == "__main__":
    main()