"""
gotrue.py — entre-nós
Script interativo para cadastrar usuários no GoTrue local e gerar o SQL de nucleo.pessoa.

Uso:
    python gotrue.py
"""

import getpass
import json
import urllib.error
import urllib.request

GOTRUE_URL = "http://localhost:54321"


def criar_usuario(email: str, senha: str) -> str:
    data = json.dumps({"email": email, "password": senha}).encode("utf-8")
    req = urllib.request.Request(
        f"{GOTRUE_URL}/signup",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as r:
            resp = json.loads(r.read())
        return resp["user"]["id"]
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Erro {e.code} retornado pelo GoTrue: {err_body}")


def main():
    print("\n" + "=" * 55)
    print("  entre-nós — Cadastro de Usuário (GoTrue)")
    print("=" * 55)

    while True:
        email = input("\nE-mail: ").strip()
        if not email:
            print("❌ E-mail não pode ser vazio.")
            continue

        senha = getpass.getpass("Senha (mínimo 6 caracteres): ")
        if len(senha) < 6:
            print("❌ Senha deve ter pelo menos 6 caracteres.")
            continue

        nome = input("Nome completo: ").strip()
        apelido = input("Apelido (ex: voce, namorado): ").strip()

        try:
            uid = criar_usuario(email, senha)
            print("\n✅ Usuário cadastrado com sucesso no GoTrue!")
            print(f"   UUID: {uid}")
            print("\n📋 Comando SQL para registrar na tabela nucleo.pessoa:")
            print("-" * 55)
            print(
                f"INSERT INTO nucleo.pessoa (id, nome_pessoa, apelido)\n"
                f"VALUES ('{uid}', '{nome}', '{apelido}');"
            )
            print("-" * 55)
        except Exception as e:
            print(f"\n❌ Falha no cadastro: {e}")

        outro = input("\nDeseja cadastrar outro usuário? (s/N): ").strip().lower()
        if outro != "s":
            print("\nFinalizado.\n")
            break


if __name__ == "__main__":
    main()