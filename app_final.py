from flask import Flask, request, redirect, url_for, jsonify, send_file, render_template_string
from datetime import datetime, date
import json
import os
from database import DatabaseManager
from models import VeicoloService, ManutenzioneService, TIPI_MANUTENZIONE, TIPI_VEICOLI

app = Flask(__name__)
app.secret_key = 'manutenzione-mezzi-2024'

# Inizializza il database
db_manager = DatabaseManager()
veicolo_service = VeicoloService(db_manager)
manutenzione_service = ManutenzioneService(db_manager)

# Template CSS comune
CSS_STYLES = '''
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: #f8fafc;
    line-height: 1.6;
    color: #2d3748;
}
.container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
.nav {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
}
.nav-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.nav-brand {
    font-size: 1.5rem;
    font-weight: bold;
    color: white;
    text-decoration: none;
}
.nav-links { display: flex; gap: 2rem; }
.nav-link {
    color: rgba(255,255,255,0.9);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;
}
.nav-link:hover { color: white; }
.header {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
}
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}
.stat-card {
    background: linear-gradient(135deg, #4c51bf 0%, #667eea 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 8px;
    text-align: center;
}
.stat-number {
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}
.stat-label {
    font-size: 0.9rem;
    opacity: 0.9;
}
.section {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin: 1.5rem 0;
}
.section h2 {
    color: #2d3748;
    margin-bottom: 1rem;
    font-size: 1.5rem;
}
.btn {
    background: #4c51bf;
    color: white;
    padding: 0.75rem 1.5rem;
    text-decoration: none;
    border-radius: 6px;
    display: inline-block;
    margin: 0.5rem 0.5rem 0.5rem 0;
    font-weight: 500;
    transition: background 0.2s;
    border: none;
    cursor: pointer;
}
.btn:hover { background: #434190; }
.btn-success { background: #48bb78; }
.btn-success:hover { background: #38a169; }
.btn-danger { background: #f56565; }
.btn-danger:hover { background: #e53e3e; }
.btn-sm {
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
}
.vehicle-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1rem;
}
.vehicle-card {
    background: #f7fafc;
    border: 1px solid #e2e8f0;
    padding: 1rem;
    border-radius: 6px;
}
.vehicle-name {
    font-weight: 600;
    font-size: 1.1rem;
    color: #2d3748;
    margin-bottom: 0.5rem;
}
.vehicle-type {
    background: #4c51bf;
    color: white;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
    display: inline-block;
    margin-bottom: 0.5rem;
}
.empty-state {
    text-align: center;
    padding: 3rem;
    color: #718096;
}
.empty-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}
.maintenance-item {
    background: #f7fafc;
    border-left: 4px solid #4c51bf;
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 0 6px 6px 0;
}
.maintenance-urgent {
    border-left-color: #f56565;
}
.form-container {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.form-group {
    margin-bottom: 1rem;
}
.form-label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #2d3748;
}
.form-input, .form-select, .form-textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    font-size: 1rem;
}
.form-input:focus, .form-select:focus, .form-textarea:focus {
    outline: none;
    border-color: #4c51bf;
    box-shadow: 0 0 0 3px rgba(76, 81, 191, 0.1);
}
.form-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
}
.success-message {
    background: #f0fff4;
    color: #276749;
    padding: 1rem;
    border-radius: 6px;
    margin: 1rem 0;
    border-left: 4px solid #48bb78;
}
.error-message {
    background: #fed7d7;
    color: #c53030;
    padding: 1rem;
    border-radius: 6px;
    margin: 1rem 0;
    border-left: 4px solid #f56565;
}
.quick-actions {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-top: 2rem;
}
.quick-action {
    background: white;
    border: 2px solid #e2e8f0;
    padding: 1.5rem;
    border-radius: 8px;
    text-align: center;
    text-decoration: none;
    color: #2d3748;
    transition: all 0.2s;
}
.quick-action:hover {
    border-color: #4c51bf;
    transform: translateY(-2px);
}
.quick-action-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
}
.list-container {
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.list-item {
    padding: 1rem;
    border-bottom: 1px solid #e2e8f0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.list-item:last-child {
    border-bottom: none;
}
@media (max-width: 768px) {
    .container { padding: 1rem; }
    .nav-content { flex-direction: column; gap: 1rem; }
    .nav-links { flex-wrap: wrap; justify-content: center; }
    .stats-grid { grid-template-columns: 1fr; }
    .vehicle-grid { grid-template-columns: 1fr; }
    .form-grid { grid-template-columns: 1fr; }
    .quick-actions { grid-template-columns: 1fr; }
}
</style>
'''

# Template di navigazione comune
def get_nav():
    return '''
    <nav class="nav">
        <div class="nav-content">
            <a href="/" class="nav-brand">🔧 Manutenzione Mezzi</a>
            <div class="nav-links">
                <a href="/" class="nav-link">Dashboard</a>
                <a href="/veicoli" class="nav-link">Veicoli</a>
                <a href="/manutenzioni" class="nav-link">Manutenzioni</a>
                <a href="/backup" class="nav-link">Backup</a>
            </div>
        </div>
    </nav>
    '''

@app.route('/')
def dashboard():
    try:
        veicoli = veicolo_service.get_tutti_veicoli()
        prossime_manutenzioni = manutenzione_service.get_prossime_manutenzioni()
        ultime_manutenzioni = manutenzione_service.get_tutte_manutenzioni()[:5]

        stats = {
            'num_veicoli': len(veicoli),
            'num_manutenzioni_totali': len(manutenzione_service.get_tutte_manutenzioni()),
            'prossime_scadenze': len(prossime_manutenzioni)
        }

        veicoli_html = ""
        if veicoli:
            for veicolo in veicoli:
                veicoli_html += f'''
                <div class="vehicle-card">
                    <div class="vehicle-name">{veicolo.nome}</div>
                    <div class="vehicle-type">{veicolo.tipo}</div>
                    <div>Km: {veicolo.km_attuali:,}</div>
                    {f'<div style="color: #718096; font-size: 0.9rem; margin-top: 0.5rem;">{veicolo.note}</div>' if veicolo.note else ''}
                    <div style="margin-top: 1rem;">
                        <a href="/veicoli/{veicolo.id}" class="btn btn-sm">Dettagli</a>
                        <a href="/manutenzioni/nuova?veicolo_id={veicolo.id}" class="btn btn-sm btn-success">Manutenzione</a>
                    </div>
                </div>
                '''
        else:
            veicoli_html = '''
            <div class="empty-state">
                <div class="empty-icon">🚗</div>
                <h3>Nessun veicolo registrato</h3>
                <p>Inizia aggiungendo il tuo primo veicolo</p>
                <a href="/veicoli/nuovo" class="btn">Aggiungi primo veicolo</a>
            </div>
            '''

        prossime_html = ""
        if prossime_manutenzioni:
            for manutenzione in prossime_manutenzioni:
                prossime_html += f'''
                <div class="maintenance-item maintenance-urgent">
                    <div style="font-weight: 600;">{manutenzione.tipo_manutenzione}</div>
                    <div style="color: #4c51bf;">{manutenzione.nome_veicolo}</div>
                    <div style="color: #718096; font-size: 0.9rem;">
                        {f'Scadenza: {manutenzione.prossima_manutenzione_data.strftime("%d/%m/%Y")}' if manutenzione.prossima_manutenzione_data else ''}
                        {f'Km: {manutenzione.prossima_manutenzione_km:,}' if manutenzione.prossima_manutenzione_km else ''}
                    </div>
                </div>
                '''

        ultime_html = ""
        if ultime_manutenzioni:
            for manutenzione in ultime_manutenzioni:
                ultime_html += f'''
                <div class="maintenance-item">
                    <div style="font-weight: 600;">{manutenzione.tipo_manutenzione}</div>
                    <div style="color: #4c51bf;">{manutenzione.nome_veicolo}</div>
                    <div style="color: #718096; font-size: 0.9rem;">
                        {manutenzione.data_intervento.strftime('%d/%m/%Y')} - {manutenzione.km_intervento:,} km
                        {f' - €{manutenzione.costo:.2f}' if manutenzione.costo else ''}
                    </div>
                </div>
                '''

        return render_template_string(f'''
        <!DOCTYPE html>
        <html lang="it">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Dashboard - Gestione Manutenzione Mezzi</title>
            {CSS_STYLES}
        </head>
        <body>
            {get_nav()}
            <div class="container">
                <div class="header">
                    <h1>Dashboard</h1>
                    <p>Panoramica generale dei tuoi veicoli e manutenzioni</p>
                </div>

                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">{stats['num_veicoli']}</div>
                        <div class="stat-label">Veicoli registrati</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{stats['num_manutenzioni_totali']}</div>
                        <div class="stat-label">Manutenzioni totali</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{stats['prossime_scadenze']}</div>
                        <div class="stat-label">Prossime scadenze</div>
                    </div>
                </div>

                <div class="section">
                    <h2>I tuoi veicoli</h2>
                    <div class="vehicle-grid">
                        {veicoli_html}
                    </div>
                </div>

                {f'''
                <div class="section">
                    <h2>Prossime manutenzioni ({len(prossime_manutenzioni)})</h2>
                    {prossime_html}
                </div>
                ''' if prossime_manutenzioni else ''}

                {f'''
                <div class="section">
                    <h2>Ultime manutenzioni</h2>
                    {ultime_html}
                    <div style="text-align: center; margin-top: 1rem;">
                        <a href="/manutenzioni" class="btn">Vedi tutte le manutenzioni</a>
                    </div>
                </div>
                ''' if ultime_manutenzioni else ''}

                <div class="quick-actions">
                    <a href="/veicoli/nuovo" class="quick-action">
                        <div class="quick-action-icon">🚗</div>
                        <h3>Aggiungi veicolo</h3>
                        <p>Registra un nuovo mezzo</p>
                    </a>
                    <a href="/manutenzioni/nuova" class="quick-action">
                        <div class="quick-action-icon">🔧</div>
                        <h3>Nuova manutenzione</h3>
                        <p>Registra un intervento</p>
                    </a>
                    <a href="/backup" class="quick-action">
                        <div class="quick-action-icon">📥</div>
                        <h3>Backup dati</h3>
                        <p>Scarica backup del database</p>
                    </a>
                </div>
            </div>
        </body>
        </html>
        ''')

    except Exception as e:
        return f'''
        <!DOCTYPE html>
        <html>
        <head><title>Errore Dashboard</title></head>
        <body style="font-family: Arial; padding: 2rem; background: #fed7d7;">
            <h1>❌ Errore nella Dashboard</h1>
            <p><strong>Errore:</strong> {str(e)}</p>
            <p><a href="/veicoli/nuovo">Aggiungi primo veicolo</a></p>
        </body>
        </html>
        '''

@app.route('/veicoli')
def lista_veicoli():
    veicoli = veicolo_service.get_tutti_veicoli()

    veicoli_html = ""
    if veicoli:
        for veicolo in veicoli:
            veicoli_html += f'''
            <div class="list-item">
                <div>
                    <h3 style="margin-bottom: 0.5rem;">{veicolo.nome}</h3>
                    <div style="color: #718096;">
                        {veicolo.tipo} • {veicolo.km_attuali:,} km
                        {f' • {veicolo.anno}' if veicolo.anno else ''}
                    </div>
                    {f'<div style="font-style: italic; margin-top: 0.25rem;">{veicolo.note}</div>' if veicolo.note else ''}
                </div>
                <div>
                    <a href="/veicoli/{veicolo.id}" class="btn btn-sm">Dettagli</a>
                    <a href="/manutenzioni/nuova?veicolo_id={veicolo.id}" class="btn btn-sm btn-success">Manutenzione</a>
                    <button onclick="if(confirm('Eliminare {veicolo.nome}?')) location.href='/veicoli/{veicolo.id}/elimina'" class="btn btn-sm btn-danger">Elimina</button>
                </div>
            </div>
            '''
    else:
        veicoli_html = '''
        <div class="empty-state">
            <div class="empty-icon">🚗</div>
            <h3>Nessun veicolo registrato</h3>
            <p>Inizia aggiungendo il tuo primo veicolo</p>
            <a href="/veicoli/nuovo" class="btn">Aggiungi primo veicolo</a>
        </div>
        '''

    return render_template_string(f'''
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <title>Veicoli - Gestione Manutenzione Mezzi</title>
        {CSS_STYLES}
    </head>
    <body>
        {get_nav()}
        <div class="container">
            <div class="header">
                <h1>I tuoi veicoli</h1>
                <a href="/veicoli/nuovo" class="btn">➕ Aggiungi veicolo</a>
            </div>

            <div class="list-container">
                {veicoli_html}
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/veicoli/nuovo', methods=['GET', 'POST'])
def nuovo_veicolo():
    message = ""

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        tipo = request.form.get('tipo', '').strip()
        anno = request.form.get('anno', '').strip()
        km_attuali = request.form.get('km_attuali', '0').strip()
        note = request.form.get('note', '').strip()

        if not nome or not tipo:
            message = '<div class="error-message">Nome e tipo sono obbligatori</div>'
        else:
            try:
                anno_int = int(anno) if anno else None
                km_int = int(km_attuali) if km_attuali else 0

                veicolo_service.crea_veicolo(nome, tipo, anno_int, km_int, note or None)
                return redirect('/veicoli')

            except ValueError:
                message = '<div class="error-message">Anno e chilometraggio devono essere numeri validi</div>'

    tipi_options = ''.join([f'<option value="{tipo}">{tipo}</option>' for tipo in TIPI_VEICOLI])

    return render_template_string(f'''
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <title>Nuovo Veicolo - Gestione Manutenzione Mezzi</title>
        {CSS_STYLES}
    </head>
    <body>
        {get_nav()}
        <div class="container">
            <div class="header">
                <h1>Aggiungi nuovo veicolo</h1>
            </div>

            {message}

            <div class="form-container">
                <form method="POST">
                    <div class="form-grid">
                        <div class="form-group">
                            <label class="form-label">Nome/Modello *</label>
                            <input type="text" name="nome" class="form-input" required placeholder="es. Honda CBR 600RR">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Tipo *</label>
                            <select name="tipo" class="form-select" required>
                                <option value="">Seleziona tipo</option>
                                {tipi_options}
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Anno</label>
                            <input type="number" name="anno" class="form-input" min="1900" max="2030" placeholder="es. 2020">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Chilometraggio attuale</label>
                            <input type="number" name="km_attuali" class="form-input" min="0" value="0" placeholder="es. 15000">
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Note</label>
                        <textarea name="note" class="form-textarea" rows="3" placeholder="Note aggiuntive..."></textarea>
                    </div>
                    <div style="margin-top: 2rem;">
                        <button type="submit" class="btn">💾 Salva veicolo</button>
                        <a href="/veicoli" class="btn" style="background: #718096;">Annulla</a>
                    </div>
                </form>
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/veicoli/<int:veicolo_id>')
def dettaglio_veicolo(veicolo_id):
    veicolo = veicolo_service.get_veicolo_by_id(veicolo_id)
    if not veicolo:
        return redirect('/veicoli')

    manutenzioni = manutenzione_service.get_manutenzioni_veicolo(veicolo_id)
    stats = manutenzione_service.get_statistiche_spese(veicolo_id)

    manutenzioni_html = ""
    if manutenzioni:
        for manutenzione in manutenzioni:
            manutenzioni_html += f'''
            <div class="maintenance-item">
                <div style="font-weight: 600; margin-bottom: 0.5rem;">{manutenzione.tipo_manutenzione}</div>
                <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 0.5rem;">
                    <span>📅 {manutenzione.data_intervento.strftime('%d/%m/%Y')}</span>
                    <span>🛣️ {manutenzione.km_intervento:,} km</span>
                    {f'<span>💰 €{manutenzione.costo:.2f}</span>' if manutenzione.costo else ''}
                </div>
                {f'<div style="font-style: italic; color: #718096;">{manutenzione.descrizione}</div>' if manutenzione.descrizione else ''}
                {f'''<div style="margin-top: 0.5rem; padding: 0.5rem; background: #fff5f5; border-radius: 4px;">
                    <strong>Prossima:</strong>
                    {f"📅 {manutenzione.prossima_manutenzione_data.strftime('%d/%m/%Y')}" if manutenzione.prossima_manutenzione_data else ""}
                    {f"🛣️ {manutenzione.prossima_manutenzione_km:,} km" if manutenzione.prossima_manutenzione_km else ""}
                </div>''' if (manutenzione.prossima_manutenzione_data or manutenzione.prossima_manutenzione_km) else ''}
            </div>
            '''
    else:
        manutenzioni_html = '''
        <div class="empty-state">
            <div class="empty-icon">🔧</div>
            <h3>Nessuna manutenzione registrata</h3>
            <p>Inizia registrando la prima manutenzione</p>
        </div>
        '''

    stats_html = ""
    if stats and stats[0] > 0:
        stats_html = f'''
        <div class="section">
            <h2>Statistiche</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem;">
                <div style="text-align: center; padding: 1rem; background: #f7fafc; border-radius: 6px;">
                    <div style="font-size: 1.5rem; font-weight: bold;">{stats[0]}</div>
                    <div style="color: #718096;">Interventi</div>
                </div>
                {f'''<div style="text-align: center; padding: 1rem; background: #f7fafc; border-radius: 6px;">
                    <div style="font-size: 1.5rem; font-weight: bold;">€{stats[1]:.2f}</div>
                    <div style="color: #718096;">Spesa totale</div>
                </div>''' if stats[1] else ''}
                {f'''<div style="text-align: center; padding: 1rem; background: #f7fafc; border-radius: 6px;">
                    <div style="font-size: 1.5rem; font-weight: bold;">€{stats[2]:.2f}</div>
                    <div style="color: #718096;">Media per intervento</div>
                </div>''' if stats[2] else ''}
            </div>
        </div>
        '''

    return render_template_string(f'''
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <title>{veicolo.nome} - Gestione Manutenzione Mezzi</title>
        {CSS_STYLES}
    </head>
    <body>
        {get_nav()}
        <div class="container">
            <div class="header">
                <h1>{veicolo.nome}</h1>
                <div>
                    <a href="/manutenzioni/nuova?veicolo_id={veicolo.id}" class="btn btn-success">🔧 Nuova manutenzione</a>
                    <a href="/veicoli" class="btn" style="background: #718096;">← Torna ai veicoli</a>
                </div>
            </div>

            <div class="section">
                <h2>Informazioni veicolo</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                    <div><strong>Tipo:</strong> {veicolo.tipo}</div>
                    {f'<div><strong>Anno:</strong> {veicolo.anno}</div>' if veicolo.anno else ''}
                    <div><strong>Chilometraggio:</strong> {veicolo.km_attuali:,} km</div>
                    <div><strong>Registrato:</strong> {veicolo.data_creazione.strftime('%d/%m/%Y') if veicolo.data_creazione else 'N/A'}</div>
                </div>
                {f'<div style="margin-top: 1rem;"><strong>Note:</strong> {veicolo.note}</div>' if veicolo.note else ''}
            </div>

            {stats_html}

            <div class="section">
                <h2>Storico manutenzioni ({len(manutenzioni)})</h2>
                {manutenzioni_html}
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/veicoli/<int:veicolo_id>/elimina')
def elimina_veicolo(veicolo_id):
    veicolo_service.elimina_veicolo(veicolo_id)
    return redirect('/veicoli')

@app.route('/manutenzioni')
def lista_manutenzioni():
    manutenzioni = manutenzione_service.get_tutte_manutenzioni()

    manutenzioni_html = ""
    if manutenzioni:
        for manutenzione in manutenzioni:
            manutenzioni_html += f'''
            <div class="list-item">
                <div>
                    <h3 style="margin-bottom: 0.5rem;">{manutenzione.tipo_manutenzione}</h3>
                    <div style="color: #4c51bf; font-weight: 500;">{manutenzione.nome_veicolo}</div>
                    <div style="color: #718096; display: flex; gap: 1rem; flex-wrap: wrap;">
                        <span>📅 {manutenzione.data_intervento.strftime('%d/%m/%Y')}</span>
                        <span>🛣️ {manutenzione.km_intervento:,} km</span>
                        {f'<span>💰 €{manutenzione.costo:.2f}</span>' if manutenzione.costo else ''}
                    </div>
                    {f'<div style="font-style: italic; margin-top: 0.25rem;">{manutenzione.descrizione}</div>' if manutenzione.descrizione else ''}
                </div>
                <div>
                    <a href="/veicoli/{manutenzione.veicolo_id}" class="btn btn-sm">Vedi veicolo</a>
                </div>
            </div>
            '''
    else:
        manutenzioni_html = '''
        <div class="empty-state">
            <div class="empty-icon">🔧</div>
            <h3>Nessuna manutenzione registrata</h3>
            <p>Inizia registrando la prima manutenzione</p>
            <a href="/manutenzioni/nuova" class="btn">🔧 Prima manutenzione</a>
        </div>
        '''

    return render_template_string(f'''
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <title>Manutenzioni - Gestione Manutenzione Mezzi</title>
        {CSS_STYLES}
    </head>
    <body>
        {get_nav()}
        <div class="container">
            <div class="header">
                <h1>Tutte le manutenzioni</h1>
                <a href="/manutenzioni/nuova" class="btn">🔧 Nuova manutenzione</a>
            </div>

            <div class="list-container">
                {manutenzioni_html}
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/manutenzioni/nuova', methods=['GET', 'POST'])
def nuova_manutenzione():
    message = ""
    veicolo_id_preselezionato = request.args.get('veicolo_id', '')

    if request.method == 'POST':
        try:
            veicolo_id = int(request.form.get('veicolo_id'))
            data_intervento = request.form.get('data_intervento')
            km_intervento = int(request.form.get('km_intervento'))
            tipo_manutenzione = request.form.get('tipo_manutenzione')
            descrizione = request.form.get('descrizione', '').strip() or None
            costo = request.form.get('costo', '').strip()
            prossima_km = request.form.get('prossima_manutenzione_km', '').strip()
            prossima_data = request.form.get('prossima_manutenzione_data', '').strip()

            costo_float = float(costo) if costo else None
            prossima_km_int = int(prossima_km) if prossima_km else None
            prossima_data_obj = prossima_data if prossima_data else None

            manutenzione_service.crea_manutenzione(
                veicolo_id, data_intervento, km_intervento, tipo_manutenzione,
                descrizione, costo_float, prossima_km_int, prossima_data_obj
            )

            return redirect(f'/veicoli/{veicolo_id}')

        except Exception as e:
            message = f'<div class="error-message">Errore: {str(e)}</div>'

    veicoli = veicolo_service.get_tutti_veicoli()
    if not veicoli:
        return render_template_string(f'''
        <!DOCTYPE html>
        <html>
        <head><title>Nessun Veicolo</title></head>
        <body style="font-family: Arial; padding: 2rem;">
            <h1>Nessun veicolo disponibile</h1>
            <p><a href="/veicoli/nuovo">Aggiungi prima un veicolo</a></p>
        </body>
        </html>
        ''')

    veicoli_options = ''.join([
        f'<option value="{v.id}" {"selected" if str(v.id) == veicolo_id_preselezionato else ""}>{v.nome} ({v.tipo})</option>'
        for v in veicoli
    ])

    tipi_options = ''.join([f'<option value="{tipo}">{tipo}</option>' for tipo in TIPI_MANUTENZIONE])

    return render_template_string(f'''
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <title>Nuova Manutenzione - Gestione Manutenzione Mezzi</title>
        {CSS_STYLES}
    </head>
    <body>
        {get_nav()}
        <div class="container">
            <div class="header">
                <h1>Registra nuova manutenzione</h1>
            </div>

            {message}

            <div class="form-container">
                <form method="POST">
                    <div class="form-grid">
                        <div class="form-group">
                            <label class="form-label">Veicolo *</label>
                            <select name="veicolo_id" class="form-select" required>
                                <option value="">Seleziona veicolo</option>
                                {veicoli_options}
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Data intervento *</label>
                            <input type="date" name="data_intervento" class="form-input" required value="{datetime.now().strftime('%Y-%m-%d')}">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Chilometraggio *</label>
                            <input type="number" name="km_intervento" class="form-input" required min="0" placeholder="es. 15000">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Tipo manutenzione *</label>
                            <select name="tipo_manutenzione" class="form-select" required>
                                <option value="">Seleziona tipo</option>
                                {tipi_options}
                            </select>
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Descrizione</label>
                        <textarea name="descrizione" class="form-textarea" rows="3" placeholder="Descrizione dettagliata dell'intervento..."></textarea>
                    </div>

                    <div class="form-grid">
                        <div class="form-group">
                            <label class="form-label">Costo (€)</label>
                            <input type="number" name="costo" class="form-input" min="0" step="0.01" placeholder="es. 45.50">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Prossima manutenzione (km)</label>
                            <input type="number" name="prossima_manutenzione_km" class="form-input" min="0" placeholder="es. 20000">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Prossima manutenzione (data)</label>
                            <input type="date" name="prossima_manutenzione_data" class="form-input">
                        </div>
                    </div>

                    <div style="margin-top: 2rem;">
                        <button type="submit" class="btn">💾 Salva manutenzione</button>
                        <a href="/manutenzioni" class="btn" style="background: #718096;">Annulla</a>
                    </div>
                </form>
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/backup')
def backup_database():
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f'backup_manutenzione_{timestamp}.db'
        db_manager.backup_database(backup_path)
        return send_file(backup_path, as_attachment=True)
    except Exception as e:
        return f'<h1>Errore backup: {str(e)}</h1><p><a href="/">Torna alla dashboard</a></p>'

if __name__ == '__main__':
    # Crea dati di esempio se il database è vuoto
    veicoli_esistenti = veicolo_service.get_tutti_veicoli()
    if not veicoli_esistenti:
        print("Creazione dati di esempio...")

        # Aggiungi veicoli di esempio
        veicolo1_id = veicolo_service.crea_veicolo(
            "Honda CBR 600RR", "Moto", 2018, 15000,
            "Moto sportiva, perfette condizioni"
        ).id

        veicolo2_id = veicolo_service.crea_veicolo(
            "Toyota Yaris", "Auto", 2020, 35000,
            "Auto di famiglia, uso quotidiano"
        ).id

        # Aggiungi manutenzioni di esempio
        manutenzione_service.crea_manutenzione(
            veicolo1_id, "2024-01-15", 14500, "Cambio olio motore",
            "Olio Castrol 10W40, filtro olio nuovo", 45.00, 16500, "2024-06-15"
        )

        manutenzione_service.crea_manutenzione(
            veicolo2_id, "2024-02-10", 34000, "Tagliando",
            "Tagliando completo presso officina autorizzata", 280.00, 44000, "2025-02-10"
        )

        print("Dati di esempio creati!")

    print("=== APPLICAZIONE MANUTENZIONE MEZZI ===")
    print("Applicazione avviata con successo!")
    print("Vai su: http://127.0.0.1:5555")
    print("Premi CTRL+C per fermare")
    print("")

    app.run(debug=False, host='127.0.0.1', port=5555)