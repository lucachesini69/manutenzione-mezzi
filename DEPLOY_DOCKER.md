# 🐳 Deploy con Docker (su un server che ospita già altre app)

Questa guida fa girare "Gestione Manutenzione Mezzi" in **container Docker**
(app Flask + database Postgres), isolato dalle altre applicazioni presenti sul
server. L'app viene pubblicata **solo su `localhost`** e il tuo **reverse proxy
esistente** (Nginx o Traefik) la espone sul web: così **non tocca le porte 80/443**
già usate dall'altra app.

File coinvolti: `Dockerfile`, `docker-compose.yml`, `.env.example`.

---

## Prerequisiti

Docker e il plugin Compose (di solito già presenti se hai altre app in container):
```bash
docker --version
docker compose version
```
Se mancano: `curl -fsSL https://get.docker.com | sh`

---

## 1️⃣ Scarica l'app e prepara le variabili

```bash
git clone https://github.com/lucachesini69/manutenzione-mezzi.git
cd manutenzione-mezzi

cp .env.example .env
nano .env        # imposta DB_PASSWORD, SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD
```
Per generare una `SECRET_KEY` casuale:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```
> Se la porta **8080** è già occupata da un'altra app, cambia `HOST_PORT` nel `.env`.

---

## 2️⃣ Avvia lo stack

```bash
docker compose up -d --build
```
Docker costruisce l'immagine, avvia Postgres e l'app. Al primo avvio vengono create
le tabelle e l'utente admin indicato nel `.env`.

Verifica che sia tutto attivo:
```bash
docker compose ps
curl http://127.0.0.1:8080/health      # deve rispondere {"status": "healthy", ...}
docker compose logs -f web             # per vedere i log dell'app
```
A questo punto l'app gira su **127.0.0.1:8080**, raggiungibile solo dal server.

---

## 3️⃣ Collega il tuo reverse proxy

### Opzione A — Nginx (installato sul server, non in container)

Aggiungi un file `/etc/nginx/sites-available/manutenzione`:
```nginx
server {
    listen 80;
    server_name manutenzione.tuo-dominio.it;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
Attivalo e ricarica:
```bash
ln -s /etc/nginx/sites-available/manutenzione /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```
HTTPS gratuito (se hai un dominio che punta al server):
```bash
certbot --nginx -d manutenzione.tuo-dominio.it
```

### Opzione B — Traefik / nginx-proxy (già in container)

Se il tuo reverse proxy gira in Docker su una rete condivisa (es. `proxy`), togli il
blocco `ports:` dal servizio `web` e aggiungi le label/rete del tuo proxy. Esempio
per Traefik nel `docker-compose.yml`:
```yaml
  web:
    # ...togli "ports:" e aggiungi:
    networks: [proxy]
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.manutenzione.rule=Host(`manutenzione.tuo-dominio.it`)"
      - "traefik.http.services.manutenzione.loadbalancer.server.port=8000"

networks:
  proxy:
    external: true
```
> Adatta i nomi (`proxy`, entrypoint, certresolver) a come è configurato il tuo Traefik.

---

## 🔄 Aggiornare l'app

```bash
cd manutenzione-mezzi
git pull
docker compose up -d --build
```

## 💾 Backup del database

```bash
# Backup su file
docker compose exec db pg_dump -U manutenzione manutenzione > backup_$(date +%F).sql

# Ripristino
cat backup_2026-07-11.sql | docker compose exec -T db psql -U manutenzione manutenzione
```
In alternativa usa il pulsante **📥 Backup DB** nell'app (scarica un JSON completo).
I dati del Postgres restano nel volume `pgdata` anche dopo `docker compose down`.

## 🧹 Comandi utili

| Azione | Comando |
|---|---|
| Stato container | `docker compose ps` |
| Log app | `docker compose logs -f web` |
| Riavvia | `docker compose restart web` |
| Ferma (dati salvi) | `docker compose down` |
| Ferma ed elimina i dati | `docker compose down -v` ⚠️ |

---

## ❓ Problemi comuni

| Sintomo | Soluzione |
|---|---|
| La porta 8080 è occupata | Cambia `HOST_PORT` nel `.env` e riavvia |
| `502` dal reverse proxy | Controlla `docker compose ps` e `docker compose logs web` |
| Errore SSL sul DB | Verifica che nel compose ci sia `PGSSLMODE: disable` (Postgres interno) |
