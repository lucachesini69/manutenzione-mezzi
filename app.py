from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from datetime import datetime, date
import json
import os
from database import DatabaseManager
from models import VeicoloService, ManutenzioneService, TIPI_MANUTENZIONE, TIPI_VEICOLI
from local_sync_backup import LocalSyncBackup
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Inizializza il database
db_manager = DatabaseManager()
veicolo_service = VeicoloService(db_manager)
manutenzione_service = ManutenzioneService(db_manager)

# Inizializza backup locale con sync
backup_service = LocalSyncBackup()

# Funzione di backup automatico
def backup_automatico():
    """Esegue il backup automatico del database"""
    try:
        print("🔄 Avvio backup automatico...")
        success = backup_service.backup_database()
        if success:
            print("✅ Backup automatico completato")
            backup_service.cleanup_old_backups(keep_count=10)
        else:
            print("❌ Backup automatico fallito")
    except Exception as e:
        print(f"❌ Errore durante backup automatico: {e}")

# Configura scheduler per backup automatico
scheduler = BackgroundScheduler()
# Backup ogni giorno alle 2:00 AM
scheduler.add_job(func=backup_automatico, trigger="cron", hour=2, minute=0, id='backup_job')

# Avvia scheduler solo se non in debug mode
if not os.environ.get('FLASK_ENV') == 'development':
    try:
        scheduler.start()
        print("Scheduler backup automatico avviato (ogni giorno alle 2:00)")
    except Exception as e:
        print(f"Errore avvio scheduler: {e}")

    # Ferma scheduler quando l'app si chiude
    atexit.register(lambda: scheduler.shutdown())

# Funzione per convertire decimali italiani
def converti_decimale(valore_str):
    """Converte stringhe con virgola o punto in float"""
    if not valore_str:
        return None

    # Rimuove spazi
    valore_str = str(valore_str).strip()

    if not valore_str:
        return None

    try:
        # Sostituisce virgola con punto
        valore_str = valore_str.replace(',', '.')
        return float(valore_str)
    except ValueError:
        return None

@app.route('/')
def dashboard():
    veicoli = veicolo_service.get_tutti_veicoli()
    prossime_manutenzioni = manutenzione_service.get_prossime_manutenzioni()
    ultime_manutenzioni = manutenzione_service.get_tutte_manutenzioni()[:5]

    # Statistiche generali
    stats = {
        'num_veicoli': len(veicoli),
        'num_manutenzioni_totali': len(manutenzione_service.get_tutte_manutenzioni()),
        'prossime_scadenze': len(prossime_manutenzioni)
    }

    return render_template('dashboard_simple.html',
                         veicoli=veicoli,
                         prossime_manutenzioni=prossime_manutenzioni,
                         ultime_manutenzioni=ultime_manutenzioni,
                         stats=stats)

@app.route('/veicoli')
def lista_veicoli():
    veicoli = veicolo_service.get_tutti_veicoli()
    return render_template('veicoli.html', veicoli=veicoli, tipi_veicoli=TIPI_VEICOLI)

@app.route('/veicoli/nuovo', methods=['GET', 'POST'])
def nuovo_veicolo():
    if request.method == 'POST':
        nome = request.form.get('nome')
        tipo = request.form.get('tipo')
        anno = request.form.get('anno')
        km_attuali = request.form.get('km_attuali', 0)
        note = request.form.get('note')

        if not nome or not tipo:
            flash('Nome e tipo sono obbligatori', 'error')
            return redirect(url_for('nuovo_veicolo'))

        try:
            anno = int(anno) if anno else None
            km_attuali = int(km_attuali) if km_attuali else 0

            veicolo_service.crea_veicolo(nome, tipo, anno, km_attuali, note)
            flash(f'Veicolo {nome} aggiunto con successo', 'success')
            return redirect(url_for('lista_veicoli'))

        except ValueError:
            flash('Anno e chilometraggio devono essere numeri validi', 'error')
            return redirect(url_for('nuovo_veicolo'))

    return render_template('nuovo_veicolo.html', tipi_veicoli=TIPI_VEICOLI)

@app.route('/veicoli/<int:veicolo_id>')
def dettaglio_veicolo(veicolo_id):
    veicolo = veicolo_service.get_veicolo_by_id(veicolo_id)
    if not veicolo:
        flash('Veicolo non trovato', 'error')
        return redirect(url_for('lista_veicoli'))

    manutenzioni = manutenzione_service.get_manutenzioni_veicolo(veicolo_id)
    stats = manutenzione_service.get_statistiche_spese(veicolo_id)

    return render_template('dettaglio_veicolo.html',
                         veicolo=veicolo,
                         manutenzioni=manutenzioni,
                         stats=stats)

@app.route('/veicoli/<int:veicolo_id>/elimina', methods=['POST'])
def elimina_veicolo(veicolo_id):
    veicolo = veicolo_service.get_veicolo_by_id(veicolo_id)
    if veicolo:
        veicolo_service.elimina_veicolo(veicolo_id)
        flash(f'Veicolo {veicolo.nome} eliminato con successo', 'success')
    else:
        flash('Veicolo non trovato', 'error')
    return redirect(url_for('lista_veicoli'))

@app.route('/manutenzioni')
def lista_manutenzioni():
    manutenzioni = manutenzione_service.get_tutte_manutenzioni()
    return render_template('manutenzioni.html', manutenzioni=manutenzioni)

@app.route('/manutenzioni/nuova', methods=['GET', 'POST'])
def nuova_manutenzione():
    if request.method == 'POST':
        veicolo_id = request.form.get('veicolo_id')
        data_intervento = request.form.get('data_intervento')
        km_intervento = request.form.get('km_intervento')
        tipo_manutenzione = request.form.get('tipo_manutenzione')
        descrizione = request.form.get('descrizione')
        costo = request.form.get('costo')
        prossima_manutenzione_km = request.form.get('prossima_manutenzione_km')
        prossima_manutenzione_data = request.form.get('prossima_manutenzione_data')

        if not all([veicolo_id, data_intervento, km_intervento, tipo_manutenzione]):
            flash('Tutti i campi obbligatori devono essere compilati', 'error')
            return redirect(url_for('nuova_manutenzione'))

        try:
            veicolo_id = int(veicolo_id)
            km_intervento = int(km_intervento)
            costo = converti_decimale(costo)
            prossima_manutenzione_km = int(prossima_manutenzione_km) if prossima_manutenzione_km else None

            if not prossima_manutenzione_data:
                prossima_manutenzione_data = None

            manutenzione_service.crea_manutenzione(
                veicolo_id, data_intervento, km_intervento, tipo_manutenzione,
                descrizione, costo, prossima_manutenzione_km, prossima_manutenzione_data
            )

            flash('Manutenzione aggiunta con successo', 'success')
            return redirect(url_for('dettaglio_veicolo', veicolo_id=veicolo_id))

        except ValueError as e:
            flash('Errore nei dati inseriti: valori numerici non validi', 'error')
            return redirect(url_for('nuova_manutenzione'))

    veicoli = veicolo_service.get_tutti_veicoli()
    veicolo_id = request.args.get('veicolo_id')
    return render_template('nuova_manutenzione.html',
                         veicoli=veicoli,
                         tipi_manutenzione=TIPI_MANUTENZIONE,
                         veicolo_id_preselezionato=veicolo_id)

@app.route('/manutenzioni/<int:manutenzione_id>/elimina', methods=['POST'])
def elimina_manutenzione(manutenzione_id):
    manutenzione_service.elimina_manutenzione(manutenzione_id)
    flash('Manutenzione eliminata con successo', 'success')
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/export/veicoli')
def export_veicoli():
    try:
        csv_path = 'export_veicoli.csv'
        db_manager.export_to_csv('veicoli', csv_path)
        return send_file(csv_path, as_attachment=True, download_name='veicoli.csv')
    except Exception as e:
        flash(f'Errore durante l\'esportazione: {str(e)}', 'error')
        return redirect(url_for('lista_veicoli'))

@app.route('/export/manutenzioni')
def export_manutenzioni():
    try:
        csv_path = 'export_manutenzioni.csv'
        db_manager.export_to_csv('manutenzioni', csv_path)
        return send_file(csv_path, as_attachment=True, download_name='manutenzioni.csv')
    except Exception as e:
        flash(f'Errore durante l\'esportazione: {str(e)}', 'error')
        return redirect(url_for('lista_manutenzioni'))

@app.route('/backup')
def backup_database():
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f'backup_manutenzione_{timestamp}.db'
        db_manager.backup_database(backup_path)
        return send_file(backup_path, as_attachment=True)
    except Exception as e:
        flash(f'Errore durante il backup: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/backup-local')
def backup_to_local():
    """Esegue backup locale con sync automatico"""
    try:
        success = backup_service.backup_database()
        if success:
            info = backup_service.get_backup_info()
            flash(f'✅ Backup salvato in OneDrive! Cartella: {info["folder_path"]}', 'success')
        else:
            flash('❌ Errore durante il backup locale.', 'error')
    except Exception as e:
        flash(f'❌ Errore durante il backup: {str(e)}', 'error')
    return redirect(url_for('dashboard'))

@app.route('/api/veicoli/<int:veicolo_id>/km', methods=['PUT'])
def aggiorna_km_api(veicolo_id):
    try:
        data = request.get_json()
        nuovi_km = int(data['km'])
        veicolo_service.aggiorna_km(veicolo_id, nuovi_km)
        return jsonify({'success': True, 'message': 'Chilometraggio aggiornato'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/stats')
def stats_api():
    veicoli = veicolo_service.get_tutti_veicoli()
    manutenzioni = manutenzione_service.get_tutte_manutenzioni()
    prossime = manutenzione_service.get_prossime_manutenzioni()

    # Calcola statistiche per i grafici
    spese_per_mese = {}
    for manutenzione in manutenzioni:
        if hasattr(manutenzione, 'costo') and manutenzione.costo:
            mese = manutenzione.data_intervento.strftime('%Y-%m')
            spese_per_mese[mese] = spese_per_mese.get(mese, 0) + manutenzione.costo

    return jsonify({
        'veicoli_count': len(veicoli),
        'manutenzioni_count': len(manutenzioni),
        'prossime_scadenze': len(prossime),
        'spese_per_mese': spese_per_mese
    })

# Filtri template personalizzati
@app.template_filter('format_date')
def format_date(value):
    if value:
        if isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m-%d').date()
        return value.strftime('%d/%m/%Y')
    return ''

@app.template_filter('format_currency')
def format_currency(value):
    if value is not None:
        return f'€ {value:.2f}'
    return ''

@app.template_filter('format_km')
def format_km(value):
    if value is not None:
        return f'{value:,} km'.replace(',', '.')
    return ''

# Gestione errori
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Inizializza dati di esempio al primo avvio
if not os.path.exists('manutenzione.db') or os.path.getsize('manutenzione.db') == 0:
    print("Creazione dati di esempio...")

    # Veicoli di esempio
    veicolo1_id = veicolo_service.crea_veicolo(
        "Honda CBR 600RR", "Moto", 2018, 15000,
        "Moto sportiva, perfette condizioni"
    ).id

    veicolo2_id = veicolo_service.crea_veicolo(
        "Toyota Yaris", "Auto", 2020, 35000,
        "Auto di famiglia, uso quotidiano"
    ).id

    # Manutenzioni di esempio
    manutenzione_service.crea_manutenzione(
        veicolo1_id, "2024-01-15", 14500, "Cambio olio motore",
        "Olio Castrol 10W40, filtro olio nuovo", 45.00, 16500, "2024-06-15"
    )

    manutenzione_service.crea_manutenzione(
        veicolo2_id, "2024-02-10", 34000, "Tagliando",
        "Tagliando completo presso officina autorizzata", 280.00, 44000, "2025-02-10"
    )

    print("Dati di esempio creati!")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)