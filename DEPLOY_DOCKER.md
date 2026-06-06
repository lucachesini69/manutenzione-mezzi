# 🐳 Deploy con Docker su VPS

Stack completo in container: **app Flask (Gunicorn) + PostgreSQL + Caddy** (reverse
proxy con HTTPS automatico via Let's Encrypt). Tutto si avvia con un comando.

```
Internet → Caddy (80/443, HTTPS auto) → web:8000 (Gunicorn/Flask) → db:5432 (PostgreSQL)
```

## Prerequisiti

- Una VPS Ubuntu/Debian con accesso SSH
- Un dominio (es. `manutenzione.tuodominio.it`) con un record **DNS A**
  che punta all'IP della VPS

## 1. Installa Docker sulla VPS

```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER   # opzionale: usare docker senza sudo (poi ri-logga)
```

## 2. Firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```
La porta del database e quella dell'app **non** sono esposte all'esterno: solo
Caddy pubblica le porte 80/443.

## 3. Scarica il codice

```bash
sudo mkdir -p /opt && cd /opt
sudo git clone https://github.com/lucachesini69/manutenzione-mezzi.git
sudo chown -R $USER:$USER /opt/manutenzione-mezzi
cd /opt/manutenzione-mezzi
```

## 4. Configura le variabili d'ambiente

```bash
cp .env.example .env
nano .env
```
Compila tutti i valori. Per generare una chiave segreta robusta:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```
Esempio di `.env`:
```ini
DOMAIN=manutenzione.tuodominio.it
ACME_EMAIL=ufficio.tecnico@autechno.it
DB_PASSWORD=una-password-db-robusta
SECRET_KEY=la-chiave-generata-sopra
APP_USERNAME=admin
APP_PASSWORD=la-password-di-accesso-allapp
```

## 5. Avvia tutto

```bash
docker compose up -d --build
```
Caddy richiede automaticamente il certificato HTTPS (ci vuole qualche secondo:
assicurati che il DNS punti già alla VPS).

Verifica lo stato:
```bash
docker compose ps
docker compose logs -f        # Ctrl+C per uscire
```

✅ L'app è online su `https://manutenzione.tuodominio.it` con il login attivo.

---

## Comandi utili

| Azione | Comando |
|---|---|
| Avvia in background | `docker compose up -d` |
| Ferma tutto | `docker compose down` |
| Riavvia | `docker compose restart` |
| Log in tempo reale | `docker compose logs -f` |
| Stato container | `docker compose ps` |

## Aggiornare l'app dopo modifiche al codice

```bash
cd /opt/manutenzione-mezzi
git pull
docker compose up -d --build
```

## Backup del database

```bash
docker compose exec db pg_dump -U manutenzione_user manutenzione > backup_$(date +%F).sql
```
Ripristino (su un DB vuoto):
```bash
cat backup_2026-06-06.sql | docker compose exec -T db psql -U manutenzione_user -d manutenzione
```
> I dati del database sono persistenti nel volume Docker `db_data`: sopravvivono a
> `docker compose down` e ai riavvii. Vengono cancellati solo con `docker compose down -v`.

## Note

- **HTTPS automatico**: Caddy gestisce e rinnova i certificati da solo, nessun certbot.
- **Login**: è attivo perché `APP_PASSWORD` è impostata nel `.env`. Cambiala lì e
  riavvia (`docker compose up -d`) per aggiornarla.
- **Niente porte esposte** per app e database: la superficie d'attacco è minima.
