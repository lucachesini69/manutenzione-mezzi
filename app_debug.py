from flask import Flask, render_template_string

app = Flask(__name__)
app.secret_key = 'debug-key'

# Template minimo per test
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - Manutenzione Mezzi</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #333; margin-bottom: 10px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .stat-card { background: #007bff; color: white; padding: 20px; border-radius: 8px; text-align: center; }
        .stat-number { font-size: 2em; font-weight: bold; margin-bottom: 5px; }
        .vehicle-list { background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }
        .button { background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; display: inline-block; margin: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 Gestione Manutenzione Mezzi</h1>
        <p>Dashboard semplificata per test</p>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{{ stats.num_veicoli }}</div>
                <div>Veicoli</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.num_manutenzioni_totali }}</div>
                <div>Manutenzioni</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.prossime_scadenze }}</div>
                <div>Scadenze</div>
            </div>
        </div>

        <div class="vehicle-list">
            <h2>I tuoi veicoli</h2>
            {% if veicoli %}
                {% for veicolo in veicoli %}
                <div style="background: white; padding: 15px; margin: 10px 0; border-radius: 4px;">
                    <h3>{{ veicolo.nome }}</h3>
                    <p>Tipo: {{ veicolo.tipo }} | KM: {{ veicolo.km_attuali }}</p>
                    {% if veicolo.note %}
                    <p><em>{{ veicolo.note }}</em></p>
                    {% endif %}
                </div>
                {% endfor %}
            {% else %}
                <p>Nessun veicolo registrato. <a href="/test-add-vehicle" class="button">Aggiungi primo veicolo</a></p>
            {% endif %}
        </div>

        <div style="text-align: center; margin-top: 30px;">
            <a href="/test-add-vehicle" class="button">➕ Aggiungi Veicolo</a>
            <a href="/veicoli" class="button">📋 Lista Veicoli</a>
            <a href="/manutenzioni" class="button">🔧 Manutenzioni</a>
        </div>

        <div style="margin-top: 30px; padding: 20px; background: #d4edda; border-radius: 4px;">
            <h3>✅ Test riuscito!</h3>
            <p>Se vedi questa pagina, l'applicazione Flask funziona correttamente con i template.</p>
            <p>Problema risolto: l'app principale dovrebbe funzionare.</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    try:
        from database import DatabaseManager
        from models import VeicoloService, ManutenzioneService

        # Inizializza servizi
        db_manager = DatabaseManager()
        veicolo_service = VeicoloService(db_manager)
        manutenzione_service = ManutenzioneService(db_manager)

        # Carica dati
        veicoli = veicolo_service.get_tutti_veicoli()
        prossime_manutenzioni = manutenzione_service.get_prossime_manutenzioni()
        ultime_manutenzioni = manutenzione_service.get_tutte_manutenzioni()[:5]

        # Statistiche
        stats = {
            'num_veicoli': len(veicoli),
            'num_manutenzioni_totali': len(manutenzione_service.get_tutte_manutenzioni()),
            'prossime_scadenze': len(prossime_manutenzioni)
        }

        return render_template_string(DASHBOARD_TEMPLATE,
                                    veicoli=veicoli,
                                    prossime_manutenzioni=prossime_manutenzioni,
                                    ultime_manutenzioni=ultime_manutenzioni,
                                    stats=stats)

    except Exception as e:
        return f"""
        <html>
        <head><title>Errore Dashboard</title></head>
        <body style="font-family: Arial; padding: 2rem; background: #ffe6e6;">
            <h1>❌ Errore nella Dashboard</h1>
            <p><strong>Errore:</strong> {str(e)}</p>
            <pre>{repr(e)}</pre>
            <p><a href="/test-basic">Prova test di base</a></p>
        </body>
        </html>
        """

@app.route('/test-basic')
def test_basic():
    return """
    <html>
    <head><title>Test Base</title></head>
    <body style="font-family: Arial; padding: 2rem;">
        <h1>✅ Flask funziona!</h1>
        <p>Se vedi questa pagina, Flask e le route funzionano correttamente.</p>
        <p><a href="/">Torna alla dashboard</a></p>
    </body>
    </html>
    """

@app.route('/test-add-vehicle')
def test_add_vehicle():
    try:
        from database import DatabaseManager
        from models import VeicoloService

        db_manager = DatabaseManager()
        veicolo_service = VeicoloService(db_manager)

        # Aggiungi veicolo di test se non esiste
        veicoli = veicolo_service.get_tutti_veicoli()
        if len(veicoli) == 0:
            veicolo_service.crea_veicolo("Honda CBR 600RR", "Moto", 2018, 15000, "Moto sportiva, perfette condizioni")
            veicolo_service.crea_veicolo("Toyota Yaris", "Auto", 2020, 35000, "Auto di famiglia, uso quotidiano")

        return """
        <html>
        <head><title>Veicoli Aggiunti</title></head>
        <body style="font-family: Arial; padding: 2rem;">
            <h1>✅ Veicoli di esempio aggiunti!</h1>
            <p>Ho aggiunto due veicoli di esempio al database.</p>
            <p><a href="/">Torna alla dashboard per vederli</a></p>
        </body>
        </html>
        """

    except Exception as e:
        return f"""
        <html>
        <head><title>Errore</title></head>
        <body style="font-family: Arial; padding: 2rem;">
            <h1>❌ Errore</h1>
            <p>Errore: {str(e)}</p>
            <p><a href="/">Torna alla dashboard</a></p>
        </body>
        </html>
        """

if __name__ == '__main__':
    print("=== APP DEBUG MANUTENZIONE ===")
    print("Vai su: http://127.0.0.1:5004")
    print("Premi CTRL+C per fermare")
    app.run(debug=True, host='127.0.0.1', port=5004)