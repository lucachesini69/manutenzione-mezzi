from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'test-key'

@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>Test Manutenzione Mezzi</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 2rem; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 2rem; border-radius: 8px; }
            h1 { color: #333; }
            .success { color: green; font-weight: bold; }
            .button { background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; display: inline-block; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔧 Gestione Manutenzione Mezzi</h1>
            <p class="success">✅ L'applicazione funziona correttamente!</p>

            <h2>Test delle funzionalità:</h2>
            <p><a href="/test-dashboard" class="button">Test Dashboard</a></p>
            <p><a href="/test-db" class="button">Test Database</a></p>

            <h2>Se questo test funziona:</h2>
            <ol>
                <li>L'applicazione Flask è configurata correttamente</li>
                <li>Il server web funziona</li>
                <li>Il problema potrebbe essere nei template complessi</li>
            </ol>

            <p><strong>Prossimo passo:</strong> Ferma questo test e prova l'app completa</p>
        </div>
    </body>
    </html>
    """

@app.route('/test-dashboard')
def test_dashboard():
    try:
        from database import DatabaseManager
        from models import VeicoloService, ManutenzioneService

        db_manager = DatabaseManager()
        veicolo_service = VeicoloService(db_manager)
        manutenzione_service = ManutenzioneService(db_manager)

        veicoli = veicolo_service.get_tutti_veicoli()

        return f"""
        <html>
        <head><title>Test Dashboard</title></head>
        <body style="font-family: Arial; padding: 2rem;">
            <h1>✅ Test Dashboard Riuscito</h1>
            <p>Database connesso correttamente</p>
            <p>Veicoli nel database: {len(veicoli)}</p>
            <p><a href="/">&larr; Torna al test principale</a></p>
        </body>
        </html>
        """
    except Exception as e:
        return f"""
        <html>
        <head><title>Errore Test</title></head>
        <body style="font-family: Arial; padding: 2rem;">
            <h1>❌ Errore nel test</h1>
            <p>Errore: {str(e)}</p>
            <p><a href="/">&larr; Torna al test principale</a></p>
        </body>
        </html>
        """

@app.route('/test-db')
def test_db():
    try:
        import sqlite3
        conn = sqlite3.connect('manutenzione.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()

        return f"""
        <html>
        <head><title>Test Database</title></head>
        <body style="font-family: Arial; padding: 2rem;">
            <h1>✅ Database SQLite Funziona</h1>
            <p>Tabelle trovate: {tables}</p>
            <p><a href="/">&larr; Torna al test principale</a></p>
        </body>
        </html>
        """
    except Exception as e:
        return f"""
        <html>
        <head><title>Errore Database</title></head>
        <body style="font-family: Arial; padding: 2rem;">
            <h1>❌ Errore Database</h1>
            <p>Errore: {str(e)}</p>
            <p><a href="/">&larr; Torna al test principale</a></p>
        </body>
        </html>
        """

if __name__ == '__main__':
    print("=== TEST APPLICAZIONE MANUTENZIONE ===")
    print("Vai su: http://127.0.0.1:5003")
    print("Premi CTRL+C per fermare")
    app.run(debug=True, host='127.0.0.1', port=5003)