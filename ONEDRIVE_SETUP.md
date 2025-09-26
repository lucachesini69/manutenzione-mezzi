# 💙 Setup Backup OneDrive (GRATUITO - Senza Carta)

## **✅ OneDrive: 5GB gratuiti senza carta di credito!**

### **🔧 STEP 1: Registra app Microsoft**

1. **Vai su:** https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps
2. **"New registration"**
3. **Nome:** `Manutenzione Mezzi Backup`
4. **Account types:** `Personal Microsoft accounts only`
5. **Redirect URI:** `http://localhost:8080` (tipo Web)
6. **Register**

### **🔧 STEP 2: Genera credenziali**

1. **Nella tua app registrata:**
2. **"Certificates & secrets"** → **"New client secret"**
3. **Descrizione:** `Backup secret`
4. **Expires:** `24 months`
5. **Add** → **COPIA IL VALUE** (sparirà!)

### **🔧 STEP 3: Configura permessi**

1. **"API permissions"**
2. **"Add a permission"** → **Microsoft Graph**
3. **"Application permissions"**
4. **Seleziona:** `Files.ReadWrite.All`
5. **"Add permissions"**
6. **"Grant admin consent"** (clicca ✓)

### **🔧 STEP 4: Prima autorizzazione (locale)**

1. **Crea file `onedrive_auth.py`:**
```python
from msal import PublicClientApplication
import json

# Sostituisci con il tuo CLIENT_ID
CLIENT_ID = "il-tuo-client-id"

app = PublicClientApplication(
    CLIENT_ID,
    authority="https://login.microsoftonline.com/common"
)

# Avvia autorizzazione
scopes = ["https://graph.microsoft.com/Files.ReadWrite"]
result = app.acquire_token_interactive(scopes=scopes)

if "access_token" in result:
    print("✅ Autorizzazione riuscita!")
    print("Token da copiare in ONEDRIVE_TOKEN:")
    print(json.dumps(result, indent=2))
else:
    print("❌ Errore:", result)
```

2. **Esegui:** `python onedrive_auth.py`
3. **Si apre il browser** → autorizza l'accesso
4. **Copia il JSON** del token

### **🔧 STEP 5: Configura su Render**

**Environment Variables:**
- `ONEDRIVE_CLIENT_ID`: Il tuo Client ID
- `ONEDRIVE_CLIENT_SECRET`: Il secret generato
- `ONEDRIVE_TOKEN`: Il JSON del token (tutto su una riga)

---

## **🔄 ALTERNATIVA: Google Apps Script**

Se preferisci Google Drive senza carta:

### **📝 Google Apps Script (100% gratuito):**

1. **Vai su:** https://script.google.com
2. **Nuovo progetto:** `Manutenzione Backup`
3. **Incolla questo codice:**

```javascript
function doPost(e) {
  try {
    // Ricevi backup via webhook
    const data = e.postData.getDataAsString();
    const backup = Utilities.base64Decode(JSON.parse(data).file);

    // Crea file su Drive
    const timestamp = new Date().toISOString().slice(0,10);
    const filename = `manutenzione_backup_${timestamp}.db`;

    DriveApp.createFile(
      DriveApp.createBlob(backup)
        .setName(filename)
        .setContentType('application/x-sqlite3')
    );

    return ContentService.createTextOutput('Backup saved to Google Drive');
  } catch (error) {
    return ContentService.createTextOutput('Error: ' + error.toString());
  }
}
```

4. **Deploy** → **Web app** → **Execute as me**
5. **Copia URL webhook** da usare nell'app

---

## **🤔 QUALE SCEGLIERE?**

### **💙 OneDrive (Raccomandato)**
- ✅ API robusta
- ✅ 5GB gratuiti
- ✅ Gestione file completa
- ⚠️ Setup 10 minuti

### **📗 Google Apps Script**
- ✅ Completamente gratuito
- ✅ Unlimited storage su Drive
- ✅ Setup 5 minuti
- ⚠️ Solo via webhook

**Quale preferisci? OneDrive o Google Apps Script?** 🚀