import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path='manutenzione.db'):
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_database(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Tabella veicoli
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS veicoli (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    anno INTEGER,
                    km_attuali INTEGER DEFAULT 0,
                    foto BLOB,
                    note TEXT,
                    data_creazione DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Tabella manutenzioni
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS manutenzioni (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    veicolo_id INTEGER,
                    data_intervento DATE NOT NULL,
                    km_intervento INTEGER NOT NULL,
                    tipo_manutenzione TEXT NOT NULL,
                    descrizione TEXT,
                    costo REAL,
                    prossima_manutenzione_km INTEGER,
                    prossima_manutenzione_data DATE,
                    data_creazione DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (veicolo_id) REFERENCES veicoli (id) ON DELETE CASCADE
                )
            ''')

            conn.commit()

    def inserisci_veicolo(self, nome, tipo, anno=None, km_attuali=0, note=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO veicoli (nome, tipo, anno, km_attuali, note)
                VALUES (?, ?, ?, ?, ?)
            ''', (nome, tipo, anno, km_attuali, note))
            conn.commit()
            return cursor.lastrowid

    def get_veicoli(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM veicoli ORDER BY nome')
            return cursor.fetchall()

    def get_veicolo_by_id(self, veicolo_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM veicoli WHERE id = ?', (veicolo_id,))
            return cursor.fetchone()

    def aggiorna_km_veicolo(self, veicolo_id, nuovi_km):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE veicoli SET km_attuali = ? WHERE id = ?', (nuovi_km, veicolo_id))
            conn.commit()

    def elimina_veicolo(self, veicolo_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM veicoli WHERE id = ?', (veicolo_id,))
            conn.commit()

    def inserisci_manutenzione(self, veicolo_id, data_intervento, km_intervento,
                             tipo_manutenzione, descrizione=None, costo=None,
                             prossima_manutenzione_km=None, prossima_manutenzione_data=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO manutenzioni
                (veicolo_id, data_intervento, km_intervento, tipo_manutenzione,
                 descrizione, costo, prossima_manutenzione_km, prossima_manutenzione_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (veicolo_id, data_intervento, km_intervento, tipo_manutenzione,
                  descrizione, costo, prossima_manutenzione_km, prossima_manutenzione_data))
            conn.commit()

            # Aggiorna i km del veicolo se maggiori di quelli attuali
            veicolo = self.get_veicolo_by_id(veicolo_id)
            if veicolo and km_intervento > veicolo[4]:  # km_attuali è l'indice 4
                self.aggiorna_km_veicolo(veicolo_id, km_intervento)

            return cursor.lastrowid

    def get_manutenzioni_by_veicolo(self, veicolo_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM manutenzioni
                WHERE veicolo_id = ?
                ORDER BY data_intervento DESC
            ''', (veicolo_id,))
            return cursor.fetchall()

    def get_tutte_manutenzioni(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT m.*, v.nome as nome_veicolo
                FROM manutenzioni m
                JOIN veicoli v ON m.veicolo_id = v.id
                ORDER BY m.data_intervento DESC
            ''')
            return cursor.fetchall()

    def get_prossime_manutenzioni(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            today = datetime.now().date()
            cursor.execute('''
                SELECT m.*, v.nome as nome_veicolo, v.km_attuali
                FROM manutenzioni m
                JOIN veicoli v ON m.veicolo_id = v.id
                WHERE (m.prossima_manutenzione_data IS NOT NULL AND m.prossima_manutenzione_data <= ?)
                   OR (m.prossima_manutenzione_km IS NOT NULL AND v.km_attuali >= m.prossima_manutenzione_km)
                ORDER BY m.prossima_manutenzione_data, m.prossima_manutenzione_km
            ''', (today,))
            return cursor.fetchall()

    def elimina_manutenzione(self, manutenzione_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM manutenzioni WHERE id = ?', (manutenzione_id,))
            conn.commit()

    def get_statistiche_spese_veicolo(self, veicolo_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT
                    COUNT(*) as num_interventi,
                    SUM(costo) as totale_spese,
                    AVG(costo) as media_spese,
                    MIN(data_intervento) as primo_intervento,
                    MAX(data_intervento) as ultimo_intervento
                FROM manutenzioni
                WHERE veicolo_id = ? AND costo IS NOT NULL
            ''', (veicolo_id,))
            return cursor.fetchone()

    def get_manutenzione_by_id(self, manutenzione_id):
        """Ottiene una manutenzione per ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM manutenzioni WHERE id = ?
            ''', (manutenzione_id,))
            return cursor.fetchone()

    def aggiorna_manutenzione(self, manutenzione_id, veicolo_id, data_intervento,
                            km_intervento, tipo_manutenzione, descrizione=None,
                            costo=None, prossima_manutenzione_km=None,
                            prossima_manutenzione_data=None):
        """Aggiorna una manutenzione esistente"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE manutenzioni SET
                    veicolo_id = ?,
                    data_intervento = ?,
                    km_intervento = ?,
                    tipo_manutenzione = ?,
                    descrizione = ?,
                    costo = ?,
                    prossima_manutenzione_km = ?,
                    prossima_manutenzione_data = ?
                WHERE id = ?
            ''', (veicolo_id, data_intervento, km_intervento, tipo_manutenzione,
                  descrizione, costo, prossima_manutenzione_km,
                  prossima_manutenzione_data, manutenzione_id))
            return cursor.rowcount > 0

    def backup_database(self, backup_path):
        import shutil
        shutil.copy2(self.db_path, backup_path)
        return True

    def restore_database(self, backup_path):
        import shutil
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, self.db_path)
            return True
        return False

    def export_to_csv(self, table_name, csv_path):
        import csv
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if table_name == 'veicoli':
                cursor.execute('SELECT * FROM veicoli')
                headers = ['id', 'nome', 'tipo', 'anno', 'km_attuali', 'foto', 'note', 'data_creazione']
            elif table_name == 'manutenzioni':
                cursor.execute('''
                    SELECT m.*, v.nome as nome_veicolo
                    FROM manutenzioni m
                    JOIN veicoli v ON m.veicolo_id = v.id
                ''')
                headers = ['id', 'veicolo_id', 'data_intervento', 'km_intervento', 'tipo_manutenzione',
                          'descrizione', 'costo', 'prossima_manutenzione_km', 'prossima_manutenzione_data',
                          'data_creazione', 'nome_veicolo']

            data = cursor.fetchall()

            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                writer.writerows(data)

            return True