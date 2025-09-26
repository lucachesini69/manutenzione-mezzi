# 📧 Backup Email - Setup 2 Minuti

## ✅ **Backup automatico via email configurato!**

### **🚀 Cosa fa:**
- ✅ Backup automatico ogni giorno alle 2:00 AM
- ✅ Il database ti arriva via email
- ✅ Backup manuale dal menu dell'app
- ✅ Completamente gratuito

---

## **🔧 Per attivare serve solo:**

### **STEP 1: Password App Gmail**
1. **Gmail** → **Gestione Account Google**
2. **Sicurezza** → **Verifica in due passaggi** (deve essere ATTIVA)
3. **Password per le app** → **Genera nuova**
4. **Nome:** `Manutenzione Mezzi`
5. **Copia la password** di 16 caratteri (tipo: `abcd efgh ijkl mnop`)

### **STEP 2: Su Render (Environment Variables)**
Aggiungi queste 3 variabili:

```
BACKUP_EMAIL = tua-email@gmail.com
BACKUP_EMAIL_PASSWORD = abcd efgh ijkl mnop
BACKUP_TO_EMAIL = tua-email@gmail.com (o altra email dove ricevere backup)
```

### **STEP 3: Deploy**
- Render rileverà automaticamente le modifiche
- Backup attivo in 1 minuto!

---

## **📱 Come usare:**

### **Backup automatico:**
- Ogni giorno alle 2:00 AM ricevi email con backup
- Oggetto: "Backup Manutenzione Mezzi - DD/MM/YYYY HH:MM"
- Allegato: database completo

### **Backup manuale:**
- Nell'app: vai su `/backup-email`
- Ricevi subito l'email con backup

### **Email di backup contiene:**
- ✅ Database completo (.db)
- ✅ Data e ora backup
- ✅ Dimensione file
- ✅ Pronto per il ripristino

---

## **💾 ALTERNATIVA: Backup Locale + Sync**

Se non vuoi configurare email:

### **Backup in cartella OneDrive/Google Drive:**
1. Crea cartella: `C:\Users\[TUO-USER]\OneDrive\ManutenzioneBackup`
2. Modifica app per salvare lì
3. OneDrive sincronizza automaticamente
4. Zero configurazione online!

---

## **🎯 QUALE SCEGLI?**

### **📧 EMAIL (Consigliato)**
- ✅ 2 minuti setup
- ✅ Backup nella posta
- ✅ Nessun servizio esterno

### **💾 LOCALE + SYNC**
- ✅ Zero config online
- ✅ Usa OneDrive esistente
- ✅ Cartella dedicata

**Dimmi quale preferisci!** 🚀