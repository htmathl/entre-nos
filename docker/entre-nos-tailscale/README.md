# 🌐 Tailscale (entre-nós)

Container dedicado que integra a stack de desenvolvimento do homelab à VPN privada do casal (**Tailscale**).
Atua simultaneamente como gateway de acesso seguro e como **Proxy Reverso (Tailscale Serve)**, eliminando a necessidade do Nginx.

---

## 🔒 Isolamento & Segurança

* **Modo Userspace (`TS_USERSPACE=true`)**: O Tailscale roda sem exigir permissões de kernel do Windows ou dispositivos `/dev/net/tun`.
* **Rede Nichada**: O container está conectado apenas à rede Docker `entre-nos`. A máquina física (Windows pessoal) não é exposta para a VPN — apenas as portas dos containers mapeados.

---

## 🧭 Roteamento Declarativo (`serve.json`)

O arquivo [`serve.json`](./serve.json) mapeia as requisições que chegam na Tailnet para os containers internos:

| Rota Tailscale | Destino Interno | Serviço |
|---|---|---|
| `http://entre-nos/` | `http://entre-nos-app:3001` | **Frontend (Next.js)** |
| `http://entre-nos/api/` | `http://entre-nos-server:8000` | **Backend (FastAPI)** |

Ambos respondem sob o mesmo domínio (`http://entre-nos`), eliminando qualquer problema de CORS entre front e back.

---

## 🚀 Como Configurar do Zero

### 1. Gerar a Auth Key
1. Acesse o painel do Tailscale: [https://login.tailscale.com/admin/settings/keys](https://login.tailscale.com/admin/settings/keys)
2. Gere uma chave marcando:
   * **Reusable**: Sim
   * **Ephemeral**: Não
   * **Pre-authorized**: Sim
3. Crie o arquivo `.env` nesta pasta com a chave:
   ```env
   TS_AUTHKEY=tskey-auth-kXXXXX-XXXXXXXXXXXXXXXXXXXXXXXX
   ```

### 2. Subir o Container
Na pasta `docker/`:
```powershell
docker compose up -d tailscale
```

### 3. Desativar Expiração da Máquina (Crucial)
A `TS_AUTHKEY` só é usada no primeiro segundo de boot para registrar o nó. As credenciais definitivas são salvas no volume Docker persistente `tailscale-state`.

Para a máquina nunca ser desconectada automaticamente após 90/180 dias:
1. Vá em [https://login.tailscale.com/admin/machines](https://login.tailscale.com/admin/machines)
2. Clique no menu `...` ao lado de `entre-nos`
3. Selecione **"Disable key expiry"**
