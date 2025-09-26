from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Manutenzione Mezzi</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 2rem; background: #f0f0f0; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 2rem; border-radius: 8px; }
            h1 { color: #333; }
            .success { color: green; font-weight: bold; font-size: 1.2rem; }
            .button { background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; display: inline-block; margin: 10px 0; }
            .test-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 2rem 0; }
            .test-card { background: #f8f9fa; border: 1px solid #dee2e6; padding: 1rem; border-radius: 6px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔧 Test Connessione - Manutenzione Mezzi</h1>
            <p class="success">✅ Connessione Flask RIUSCITA!</p>

            <div class="test-grid">
                <div class="test-card">
                    <h3>✅ Server Web</h3>
                    <p>Flask funziona correttamente</p>
                </div>
                <div class="test-card">
                    <h3>✅ HTML</h3>
                    <p>I template vengono caricati</p>
                </div>
                <div class="test-card">
                    <h3>✅ CSS</h3>
                    <p>Gli stili funzionano</p>
                </div>
                <div class="test-card">
                    <h3>✅ Porta 5000</h3>
                    <p>Nessun conflitto di porte</p>
                </div>
            </div>

            <h2>Prossimi passi:</h2>
            <ol>
                <li>✅ Questo test funziona</li>
                <li>🔄 Prova l'app con database: <a href="/test-db" class="button">Test Database</a></li>
                <li>🔄 Prova l'app completa: <a href="/test-full" class="button">Test App Completa</a></li>
            </ol>

            <p><strong>Se vedi questa pagina, il problema è nei template complessi!</strong></p>
        </div>
    </body>
    </html>
    '''

@app.route('/test-db')
def test_db():
    try:
        from database import DatabaseManager
        from models import VeicoloService

        db = DatabaseManager()
        service = VeicoloService(db)
        veicoli = service.get_tutti_veicoli()

        return f'''
        <!DOCTYPE html>
        <html>
        <head><title>Test Database</title></head>
        <body style="font-family: Arial; padding: 2rem; background: #e8f5e8;">
            <h1>✅ DATABASE FUNZIONA!</h1>
            <p>Veicoli nel database: {len(veicoli)}</p>
            <p><a href="/">&larr; Torna ai test</a></p>
            <p><a href="/test-full">Prova app completa</a></p>
        </body>
        </html>
        '''
    except Exception as e:
        return f'''
        <!DOCTYPE html>
        <html>
        <head><title>Errore Database</title></head>
        <body style="font-family: Arial; padding: 2rem; background: #ffe6e6;">
            <h1>❌ Errore Database</h1>
            <p>Errore: {str(e)}</p>
            <p><a href="/">&larr; Torna ai test</a></p>
        </body>
        </html>
        '''

@app.route('/test-full')
def test_full():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Redirect App Completa</title></head>
    <body style="font-family: Arial; padding: 2rem;">
        <h1>🔄 Test App Completa</h1>
        <p>Ora ferma questo test e avvia l'app principale:</p>
        <ol>
            <li>Premi CTRL+C per fermare questo test</li>
            <li>Esegui: <code>python app.py</code></li>
            <li>Vai su: http://127.0.0.1:5000</li>
        </ol>
        <p><a href="/">&larr; Torna ai test</a></p>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("=== TEST CONNESSIONE MINIMO ===")
    print("Se QUESTO funziona, il problema sono i template complessi")
    print("Vai su: http://127.0.0.1:5000")
    print("")
    app.run(debug=False, host='127.0.0.1', port=5000)