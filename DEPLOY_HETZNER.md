# 🖥️ Deploy su VPS Hetzner

Guida per installare "Gestione Manutenzione Mezzi" su un server Hetzner Cloud
con **Postgres + Gunicorn + Nginx + HTTPS**. Tempo stimato: ~30 minuti.

I file di configurazione pronti sono nella cartella `deploy/`.

---

## 0️⃣ Crea il server

1. Vai su [console.hetzner.cloud](https://console.hetzner.cloud) → **New Project** → **Add Server**
2. Scelte consigliate:
   - **Location**: Nuremberg o Falkenstein (Germania) o Helsinki
   - **Image**: **Ubuntu 24.04**
   - **Type**: **CX22** (2 vCPU, 4 GB RAM) — abbondante per questa app (~4€/mese)
   - **SSH Key**: aggiungi la tua chiave SSH (consigliato) oppure usa la password
3. Crea il server e prendi nota dell'**indirizzo IP**.
4. (Opzionale ma consigliato) Se hai un dominio, crea un record **DNS di tipo A**
   che punta all'IP del server (es. `manutenzione.tuazienda.it → 1.2.3.4`).

Collegati via SSH:
```bash
ssh root@IP_DEL_SERVER
```

---

## 1️⃣ Aggiorna il sistema e installa i pacchetti

```bash
apt update && apt upgrade -y
apt install -y python3-venv python3-pip git postgresql nginx
```

---

## 2️⃣ Crea il database Postgres

```bash
sudo -u postgres psql <<'SQL'
CREATE USER manutenzione WITH PASSWORD 'SCEGLI_UNA_PASSWORD_FORTE';
CREATE DATABASE manutenzione OWNER manutenzione;
SQL
```
> 📌 Annota la password: ti servirà nel file `.env` del passo 4.

---

## 3️⃣ Scarica l'applicazione

Crea un utente di sistema dedicato (senza login) e clona il repository:
```bash
adduser --system --group --home /opt/manutenzione-mezzi manutenzione

git clone https://github.com/lucachesini69/manutenzione-mezzi.git /opt/manutenzione-mezzi
cd /opt/manutenzione-mezzi
```

Crea l'ambiente virtuale e installa le dipendenze:
```bash
python3 -m venv venv
venv/bin/pip install --upgrade pip
venv/bin/pip install -r requirements.txt
```

---

## 4️⃣ Configura le variabili d'ambiente

```bash
cp deploy/manutenzione.env.example /etc/manutenzione.env
nano /etc/manutenzione.env      # compila password, SECRET_KEY e credenziali admin
chmod 600 /etc/manutenzione.env
chown manutenzione:www-data /etc/manutenzione.env
```
Per generare una `SECRET_KEY` casuale:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```
Assegna i permessi della cartella all'utente dell'app:
```bash
chown -R manutenzione:www-data /opt/manutenzione-mezzi
```

---

## 5️⃣ Avvia l'app come servizio (systemd)

```bash
cp deploy/manutenzione.service /etc/systemd/system/manutenzione.service
systemctl daemon-reload
systemctl enable --now manutenzione
systemctl status manutenzione       # deve risultare "active (running)"
```
Al primo avvio l'app crea le tabelle e l'utente admin indicato nel file `.env`.

Se qualcosa non va, controlla i log:
```bash
journalctl -u manutenzione -n 50 --no-pager
```

---

## 6️⃣ Configura Nginx

```bash
cp deploy/nginx-manutenzione.conf /etc/nginx/sites-available/manutenzione
nano /etc/nginx/sites-available/manutenzione   # sostituisci "tuo-dominio.it"
ln -s /etc/nginx/sites-available/manutenzione /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default          # rimuove la pagina di default
nginx -t && systemctl reload nginx
```
A questo punto l'app è raggiungibile via **http://IP_DEL_SERVER** (o il tuo dominio).

---

## 7️⃣ Firewall

```bash
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable
```

---

## 8️⃣ HTTPS gratuito (solo se hai un dominio)

```bash
apt install -y certbot python3-certbot-nginx
certbot --nginx -d tuo-dominio.it -d www.tuo-dominio.it
```
Certbot configura l'HTTPS e il rinnovo automatico. Ora l'app è su **https://tuo-dominio.it** 🎉

---

## 🔄 Aggiornare l'app in futuro

Quando pubblichi nuove modifiche su GitHub:
```bash
cd /opt/manutenzione-mezzi
sudo -u manutenzione git pull
sudo -u manutenzione venv/bin/pip install -r requirements.txt
systemctl restart manutenzione
```

---

## 💾 Backup del database

Backup manuale del Postgres:
```bash
sudo -u postgres pg_dump manutenzione > backup_$(date +%F).sql
```
Per un backup automatico giornaliero, aggiungi una riga a `crontab -e`:
```
0 3 * * * sudo -u postgres pg_dump manutenzione > /root/backup_manutenzione_$(date +\%F).sql
```
In alternativa usa il pulsante **📥 Backup DB** nell'app (scarica un JSON completo).

---

## ❓ Problemi comuni

| Sintomo | Soluzione |
|---|---|
| `502 Bad Gateway` | Il servizio Gunicorn non è attivo: `systemctl status manutenzione` e controlla i log |
| Errore di connessione al DB | Verifica `DATABASE_URL` e `PGSSLMODE=disable` in `/etc/manutenzione.env` |
| Password admin dimenticata | È stata creata solo al primo avvio; per reimpostarla vedi nota sotto |

> 🔑 **Reset password admin**: le credenziali admin vengono create solo quando il DB
> non ha ancora utenti. Per aggiungere un nuovo utente basta usare la pagina **Utenti**
> dall'interno dell'app; se resti chiuso fuori, si può reinserire un utente via SQL.
