# 🔧 Gestione Manutenzione Mezzi

Un'applicazione web completa per gestire la manutenzione di veicoli (auto, moto, biciclette, ecc.) che funziona completamente in locale nel browser.

## ✨ Caratteristiche Principali

- **🚗 Gestione Veicoli**: Registra e gestisci i tuoi mezzi con informazioni dettagliate
- **🔧 Storico Manutenzioni**: Tieni traccia di tutti gli interventi effettuati
- **⏰ Promemoria Automatici**: Notifiche per le prossime manutenzioni in scadenza
- **📊 Statistiche e Analisi**: Visualizza spese e frequenza degli interventi
- **💾 Backup e Export**: Esporta i dati in CSV e crea backup del database
- **🌙 Tema Scuro/Chiaro**: Interfaccia adattiva con supporto per entrambi i temi
- **📱 Design Responsive**: Ottimizzata per desktop, tablet e smartphone
- **🔒 Privacy Completa**: Tutti i dati rimangono sul tuo computer

## 🚀 Installazione e Avvio

### Prerequisiti
- Python 3.7 o superiore
- pip (package installer per Python)

### Installazione

1. **Scarica o clona il progetto**:
   ```bash
   # Se hai scaricato il file ZIP, estrailo in una cartella
   # Oppure clona il repository se disponibile
   ```

2. **Naviga nella cartella del progetto**:
   ```bash
   cd manutenzione_mezzi
   ```

3. **Installa le dipendenze**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Avvia l'applicazione**:
   ```bash
   python app.py
   ```

5. **Apri il browser** e visita:
   ```
   http://localhost:5001
   ```

### 🎯 Avvio Rapido

Per Windows:
```cmd
cd manutenzione_mezzi
pip install -r requirements.txt
python app.py
```

Per macOS/Linux:
```bash
cd manutenzione_mezzi
pip3 install -r requirements.txt
python3 app.py
```

## 📋 Funzionalità Dettagliate

### Gestione Veicoli
- **Registrazione**: Aggiungi veicoli con nome, tipo, anno, chilometraggio
- **Modifica**: Aggiorna informazioni e chilometraggio in tempo reale
- **Note Personali**: Aggiungi annotazioni e dettagli specifici
- **Eliminazione**: Rimuovi veicoli non più utilizzati

### Registro Manutenzioni
- **Interventi Completi**: Registra data, chilometraggio, tipo di manutenzione
- **Descrizioni Dettagliate**: Aggiungi dettagli su parti sostituite e lavori effettuati
- **Costi**: Tieni traccia delle spese per ogni intervento
- **Promemoria Futuri**: Imposta scadenze per chilometraggio o data

### Dashboard Intelligente
- **Panoramica Generale**: Visualizza statistiche sui tuoi veicoli
- **Prossime Scadenze**: Vedi rapidamente cosa necessita manutenzione
- **Ultime Attività**: Storico recente degli interventi
- **Azioni Rapide**: Accesso veloce alle funzioni più utilizzate

### Funzioni Avanzate
- **Ricerca e Filtri**: Trova rapidamente manutenzioni specifiche
- **Esportazione CSV**: Esporta tutti i dati per analisi esterne
- **Backup Database**: Salva una copia di sicurezza dei tuoi dati
- **Stampa**: Crea report stampabili delle manutenzioni

## 📁 Struttura del Progetto

```
manutenzione_mezzi/
├── app.py                 # Applicazione Flask principale
├── database.py           # Gestione database SQLite
├── models.py            # Modelli dati per veicoli e manutenzioni
├── requirements.txt     # Dipendenze Python
├── manutenzione.db      # Database SQLite (creato automaticamente)
├── templates/           # Template HTML
│   ├── base.html
│   ├── dashboard.html
│   ├── veicoli.html
│   ├── dettaglio_veicolo.html
│   ├── nuovo_veicolo.html
│   ├── manutenzioni.html
│   └── nuova_manutenzione.html
├── static/              # File statici (CSS, JS)
│   ├── style.css
│   └── script.js
└── README.md           # Questo file
```

## 🎨 Personalizzazione

### Tipi di Veicoli
I tipi di veicoli predefiniti includono:
- Auto, Moto, Scooter, Bicicletta
- Camper, Furgone, Autocarro, Quad

Puoi modificare l'elenco nel file `models.py` nella variabile `TIPI_VEICOLI`.

### Tipi di Manutenzione
I tipi di manutenzione predefiniti includono:
- Cambio olio motore, Cambio filtri
- Cambio gomme, Controllo freni
- Tagliando, Revisione generale

Modifica l'elenco nel file `models.py` nella variabile `TIPI_MANUTENZIONE`.

### Temi e Colori
L'applicazione supporta tema chiaro e scuro. I colori sono configurabili nel file `static/style.css` tramite le variabili CSS in `:root`.

## 🔧 Configurazione Avanzata

### Porta Personalizzata
Per utilizzare una porta diversa da 5001:
```python
# Modifica l'ultima riga di app.py
app.run(debug=True, host='0.0.0.0', port=8080)
```

### Database Personalizzato
Per utilizzare un percorso diverso per il database:
```python
# Modifica in app.py
db_manager = DatabaseManager('percorso/personalizzato/database.db')
```

## 📊 Backup e Ripristino

### Backup Automatico
L'applicazione offre funzionalità di backup integrate:
- **Backup Database**: Scarica una copia del file SQLite
- **Export CSV**: Esporta dati in formato CSV per Excel/LibreOffice

### Ripristino Manuale
Per ripristinare un backup:
1. Ferma l'applicazione
2. Sostituisci il file `manutenzione.db` con il tuo backup
3. Riavvia l'applicazione

## ❓ Risoluzione Problemi

### L'applicazione non si avvia
```bash
# Verifica la versione di Python
python --version

# Reinstalla le dipendenze
pip install --upgrade -r requirements.txt

# Verifica che la porta 5001 non sia in uso
netstat -an | findstr 5001  # Windows
lsof -i :5001              # macOS/Linux
```

### Database corrotto
```bash
# Elimina il database esistente (perderai i dati)
rm manutenzione.db  # macOS/Linux
del manutenzione.db # Windows

# Riavvia l'applicazione per creare un nuovo database
python app.py
```

### Errori di permessi
```bash
# Su macOS/Linux, potrebbero servire permessi di scrittura
chmod 755 .
chmod 644 *.py
```

## 🔒 Privacy e Sicurezza

- **Locale al 100%**: Nessun dato viene inviato a server esterni
- **Nessuna registrazione**: Non servono account o login
- **Database locale**: Tutti i dati rimangono sul tuo computer
- **Backup controllato**: Tu decidi quando e dove fare backup

## 🆘 Supporto

### FAQ

**Q: Posso usare l'applicazione su più computer?**
A: Sì, copia l'intera cartella su ogni computer e avvia l'applicazione.

**Q: Come condivido i dati tra dispositivi?**
A: Usa la funzione di backup/export per trasferire i dati.

**Q: L'applicazione funziona offline?**
A: Sì, completamente. Non serve connessione internet.

**Q: Posso modificare il codice?**
A: Certamente! Il codice è libero e modificabile secondo le tue esigenze.

### Problemi Comuni

1. **Errore "Address already in use"**: Un'altra applicazione usa la porta 5001
2. **Errore "Module not found"**: Installa le dipendenze con `pip install -r requirements.txt`
3. **Database locked**: Chiudi altre istanze dell'applicazione

## 🚀 Funzionalità Future

Possibili miglioramenti per versioni future:
- [ ] Upload di foto per veicoli e manutenzioni
- [ ] Grafici avanzati e analytics
- [ ] Promemoria email/notifiche desktop
- [ ] Integrazione con API di garage/officine
- [ ] App mobile companion
- [ ] Sincronizzazione cloud opzionale

## 📄 Licenza

Questo progetto è libero per uso personale e modifiche. Sentiti libero di adattarlo alle tue esigenze specifiche.

## 🤝 Contributi

Se hai suggerimenti o migliorie:
1. Modifica il codice secondo le tue necessità
2. Documenta le modifiche effettuate
3. Condividi le tue personalizzazioni con altri utenti

---

**Buona gestione delle tue manutenzioni! 🚗🔧**

*Versione 1.0 - Applicazione locale per la gestione manutenzione mezzi*