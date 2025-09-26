#!/usr/bin/env python3

print("=== TEST APPLICAZIONE MANUTENZIONE MEZZI ===")
print()

try:
    print("1. Test import Flask...")
    from flask import Flask
    print("   OK Flask importato correttamente")

    print("2. Test import database...")
    from database import DatabaseManager
    print("   OK DatabaseManager importato")

    print("3. Test import models...")
    from models import VeicoloService, ManutenzioneService
    print("   OK Services importati")

    print("4. Test inizializzazione database...")
    db = DatabaseManager()
    print("   OK Database inizializzato")

    print("5. Test creazione app Flask...")
    app = Flask(__name__)
    app.secret_key = 'test-key'
    print("   OK App Flask creata")

    print("6. Test route semplice...")
    @app.route('/')
    def test():
        return "App funziona!"
    print("   OK Route registrata")

    print()
    print("=== TUTTI I TEST SUPERATI ===")
    print("L'applicazione dovrebbe funzionare correttamente.")
    print()

    # Avvia il server
    print("Avvio server di test...")
    print("Apri il browser su: http://localhost:5002")
    print("Premi CTRL+C per fermare")
    print()

    app.run(host='127.0.0.1', port=5002, debug=False)

except Exception as e:
    print(f"   ERRORE: {e}")
    import traceback
    traceback.print_exc()
    print()
    print("=== RISOLUZIONE PROBLEMI ===")
    print("1. Verifica che Python sia installato correttamente")
    print("2. Esegui: pip install -r requirements.txt")
    print("3. Verifica che la cartella contenga tutti i file necessari")
    print("4. Controlla i permessi dei file")