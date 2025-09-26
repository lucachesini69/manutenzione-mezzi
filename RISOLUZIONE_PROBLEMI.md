# 🔧 Risoluzione Problemi - Gestione Manutenzione Mezzi

## 🚀 Modalità di Avvio

### Metodo 1: Script Automatico (Windows)
Doppio click su `avvia_windows.bat`

### Metodo 2: Script Automatico (Linux/macOS)
```bash
./avvia.sh
```

### Metodo 3: Avvio Manuale
```bash
cd manutenzione_mezzi
pip install -r requirements.txt
python app.py
```

### Metodo 4: Test Diagnostico
```bash
python test_simple.py
```

## ❌ Problemi Comuni e Soluzioni

### 1. "ModuleNotFoundError: No module named 'flask'"
**Causa:** Flask non è installato
**Soluzione:**
```bash
pip install -r requirements.txt
```

### 2. "Address already in use" / Porta occupata
**Causa:** Un'altra applicazione usa la porta 5000
**Soluzione:**
- Chiudi altre applicazioni che usano la porta 5000
- Oppure modifica la porta in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### 3. "Python was not found"
**Causa:** Python non è installato o non è nel PATH
**Soluzione:**
- Installa Python da https://python.org
- Su Windows, assicurati di selezionare "Add to PATH"

### 4. "Permission denied" / Errori di permessi
**Causa:** Permessi insufficienti
**Soluzione Linux/macOS:**
```bash
chmod +x avvia.sh
chmod 755 .
```

### 5. Database corrotto
**Causa:** File database danneggiato
**Soluzione:**
```bash
# Elimina il database (perderai i dati)
rm manutenzione.db        # Linux/macOS
del manutenzione.db       # Windows

# Riavvia l'applicazione per creare un nuovo database
python app.py
```

### 6. Template not found / File non trovati
**Causa:** Struttura cartelle errata
**Verifica:**
```
manutenzione_mezzi/
├── app.py
├── templates/
│   └── base.html
└── static/
    └── style.css
```

### 7. L'applicazione si avvia ma non risponde
**Cause possibili:**
- Firewall che blocca la connessione
- Browser che non si connette a localhost

**Soluzioni:**
1. Prova un browser diverso
2. Usa `127.0.0.1:5000` invece di `localhost:5000`
3. Disabilita temporaneamente il firewall
4. Controlla che non ci siano proxy attivi

### 8. Errori di encoding (caratteri strani)
**Causa:** Problemi di encoding su Windows
**Soluzione:**
- Usa `avvia_windows.bat` invece di `avvia.bat`
- Oppure imposta l'encoding UTF-8:
```cmd
chcp 65001
python app.py
```

## 🔍 Test Diagnostici

### Test Componenti Base
```bash
python -c "
import flask, sqlite3
print('Flask:', flask.__version__)
print('SQLite disponibile')
"
```

### Test Database
```bash
python -c "
from database import DatabaseManager
db = DatabaseManager()
print('Database OK')
"
```

### Test Applicazione
```bash
python test_simple.py
```

## 📋 Checklist Pre-Avvio

- [ ] Python 3.7+ installato
- [ ] pip funzionante
- [ ] Cartella completa con tutti i file
- [ ] Permessi di lettura/scrittura
- [ ] Porta 5000 libera
- [ ] Firewall configurato

## 🌐 URL di Accesso

- **Principale:** http://localhost:5000
- **Alternativo:** http://127.0.0.1:5000
- **Test:** http://localhost:5002 (con test_simple.py)

## 🆘 Se Nulla Funziona

1. **Reinstalla tutto:**
```bash
pip uninstall flask jinja2 werkzeug
pip install -r requirements.txt
```

2. **Usa una porta diversa:**
Modifica `app.py` alla fine:
```python
app.run(debug=True, host='127.0.0.1', port=8080)
```

3. **Versione minimale:**
Crea un file `test_minimal.py`:
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Funziona!"

app.run(port=5000)
```

4. **Controlla i log:**
Avvia con debug abilitato:
```bash
python -c "
from app import app
app.run(debug=True, host='127.0.0.1', port=5000)
"
```

## 🔧 Personalizzazioni

### Cambiare Porta
Modifica in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=NUOVA_PORTA)
```

### Database Esterno
Modifica in `app.py`:
```python
db_manager = DatabaseManager('percorso/database.db')
```

### Disabilitare Debug
Modifica in `app.py`:
```python
app.run(debug=False, host='127.0.0.1', port=5000)
```

---

**Se il problema persiste, verifica che tutti i file siano presenti e che Python sia installato correttamente.**