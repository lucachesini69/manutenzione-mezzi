# 🔐 Configurazione Google Drive Backup

## ✅ **Backup automatico aggiunto all'app!**

### **🚀 Cosa fa:**
- ✅ Backup automatico ogni giorno alle 2:00 AM
- ✅ Salva su Google Drive in cartella "Manutenzione_Mezzi_Backup"
- ✅ Mantiene gli ultimi 10 backup (elimina i vecchi)
- ✅ Backup manuale dal menu dell'app

---

## **🔧 Per attivare il backup devi configurare Google API:**

### **STEP 1: Crea progetto Google**
1. Vai su https://console.cloud.google.com/
2. Crea nuovo progetto: **"Manutenzione Mezzi"**
3. Seleziona il progetto creato

### **STEP 2: Abilita Google Drive API**
1. Menu → **APIs & Services** → **Library**
2. Cerca **"Google Drive API"**
3. Clicca **ENABLE**

### **STEP 3: Crea credenziali**
1. **APIs & Services** → **Credentials**
2. **+ CREATE CREDENTIALS** → **OAuth client ID**
3. **Application type**: Web application
4. **Name**: Manutenzione Mezzi Backup
5. **Authorized redirect URIs**:
   - `http://localhost:8080/`
   - URL della tua app Render (se online)
6. **CREATE**
7. **SCARICA** il file JSON delle credenziali

### **STEP 4: Prima autorizzazione (locale)**
1. Rinomina il file scaricato in `credentials.json`
2. Metti il file nella cartella del progetto
3. Esegui: `python google_drive_backup.py`
4. Si aprirà il browser per autorizzare l'accesso
5. Autorizza l'accesso al tuo Google Drive
6. Verrà creato un file `token.json`

### **STEP 5: Configurazione su Render (per app online)**
1. Copia il contenuto di `token.json`
2. Su Render → Environment Variables
3. Aggiungi variabile:
   - **Name**: `GOOGLE_CREDENTIALS`
   - **Value**: [incolla contenuto di token.json]

---

## **📱 Come usare:**

### **Backup automatico:**
- Avviene ogni giorno alle 2:00 AM automaticamente
- Nessuna azione richiesta

### **Backup manuale:**
- Nell'app, vai su: `/backup-drive`
- O aggiungi bottone nella dashboard

### **Dove trovare i backup:**
- Google Drive → Cartella "Manutenzione_Mezzi_Backup"
- File nominati: `manutenzione_backup_YYYYMMDD_HHMMSS.db`

---

## **🔧 Se non configuri Google Drive:**
- ✅ L'app funziona normalmente
- ❌ Nessun backup automatico
- ✅ Puoi ancora fare backup locali con `/backup`

**💡 IMPORTANTE:** Senza configurazione Google Drive, i backup automatici non funzioneranno ma l'app rimane perfettamente utilizzabile!