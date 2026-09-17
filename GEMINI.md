# entre-nós — notas para agentes de IA

## Regras de comportamento

- **Nunca fazer `git push`** — o usuário controla todos os pushes manualmente.
- **Nunca rodar `docker compose down -v`** sem confirmação explícita do usuário.
  O `-v` apaga os volumes Docker e **destrói os dados do banco permanentemente**.
  Usar `docker compose down` (sem `-v`) para parar os containers preservando os dados.

## Contexto do projeto

App privado de casal (homelab). Ver `docs/draft/arquitetura_inicial.md` para
decisões de arquitetura e `docs/draft/db/db_v0.md` para o schema do banco.
