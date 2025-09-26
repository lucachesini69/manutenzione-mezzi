# 🚀 Come mettere l'app ONLINE

## 📱 **OPZIONE 1: Railway (GRATUITO - CONSIGLIATO)**

### 1️⃣ Preparazione
1. Vai su https://railway.app
2. Registrati con GitHub
3. Installa Git se non lo hai: https://git-scm.com/

### 2️⃣ Setup Git nella cartella del progetto
```bash
git init
git add .
git commit -m "Initial commit"
```

### 3️⃣ Deploy su Railway
1. Railway Dashboard → "New Project"
2. "Deploy from GitHub repo"
3. Seleziona questo repository
4. Railway rileva automaticamente Flask
5. L'app sarà online in 2-3 minuti!

### 4️⃣ URL Finale
Railway ti darà un URL tipo: `https://tua-app.up.railway.app`

---

## 📱 **OPZIONE 2: Render (GRATUITO)**

1. Vai su https://render.com
2. Registrati con GitHub
3. "New Web Service"
4. Connetti il repository
5. Impostazioni:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Port**: Lascia vuoto (auto)

---

## 📱 **OPZIONE 3: Ngrok (TEMPORANEO - PER TEST)**

### Setup veloce per test:
1. Scarica ngrok: https://ngrok.com/
2. Installa e registrati
3. Nella cartella del progetto:
```bash
python app.py
# In un altro terminale:
ngrok http 5001
```
4. Usa l'URL fornito da ngrok (valido fino a quando chiudi)

---

## 🔧 **File già preparati per il deployment:**
- ✅ `Procfile` - Per Heroku/Railway
- ✅ `requirements.txt` - Dipendenze Python
- ✅ `runtime.txt` - Versione Python
- ✅ App modificata per produzione

## 🌍 **Dopo il deployment l'app sarà accessibile:**
- Da qualsiasi PC/smartphone
- Con URL pubblico permanente
- Database SQLite incluso
- Nessun costo (piani gratuiti)

---

**💡 SUGGERIMENTO:** Railway è più semplice e affidabile per principianti!