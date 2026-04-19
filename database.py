import os
from datetime import datetime
from urllib.parse import urlparse


def _is_postgres_url(url):
    return url and url.startswith(('postgres://', 'postgresql://'))


class DatabaseManager:
    def __init__(self, db_path='manutenzione.db'):
        self.database_url = os.environ.get('DATABASE_URL')
        self.use_postgres = _is_postgres_url(self.database_url)
        self.db_path = db_path

        if self.use_postgres:
            import psycopg2
            import psycopg2.extras
            self._psycopg2 = psycopg2
            self._psycopg2_extras = psycopg2.extras
            self.placeholder = '%s'
        else:
            import sqlite3
            self._sqlite3 = sqlite3
            self.placeholder = '?'

        self.init_database()

    def get_connection(self):
        if self.use_postgres:
            url = self.database_url
            if url.startswith('postgres://'):
                url = url.replace('postgres://', 'postgresql://', 1)
            return self._psycopg2.connect(url, sslmode=os.environ.get('PGSSLMODE', 'require'))
        return self._sqlite3.connect(self.db_path)

    def _q(self, sql):
        """Converte i placeholder ? in %s quando si usa Postgres."""
        if self.use_postgres:
            return sql.replace('?', '%s')
        return sql

    def init_database(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            if self.use_postgres:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS veicoli (
                        id SERIAL PRIMARY KEY,
                        nome TEXT NOT NULL,
                        tipo TEXT NOT NULL,
                        anno INTEGER,
                        km_attuali INTEGER DEFAULT 0,
                        foto BYTEA,
                        note TEXT,
                        data_creazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS manutenzioni (
                        id SERIAL PRIMARY KEY,
                        veicolo_id INTEGER REFERENCES veicoli(id) ON DELETE CASCADE,
                        data_intervento DATE NOT NULL,
                        km_intervento INTEGER NOT NULL,
                        tipo_manutenzione TEXT NOT NULL,
                        descrizione TEXT,
                        costo REAL,
                        prossima_manutenzione_km INTEGER,
                        prossima_manutenzione_data DATE,
                        data_creazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
            else:
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

    def _execute_insert(self, cursor, sql, params):
        if self.use_postgres:
            cursor.execute(self._q(sql) + ' RETURNING id', params)
            return cursor.fetchone()[0]
        cursor.execute(sql, params)
        return cursor.lastrowid

    def inserisci_veicolo(self, nome, tipo, anno=None, km_attuali=0, note=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            new_id = self._execute_insert(
                cursor,
                'INSERT INTO veicoli (nome, tipo, anno, km_attuali, note) VALUES (?, ?, ?, ?, ?)',
                (nome, tipo, anno, km_attuali, note),
            )
            conn.commit()
            return new_id

    def get_veicoli(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM veicoli ORDER BY nome')
            return cursor.fetchall()

    def get_veicolo_by_id(self, veicolo_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(self._q('SELECT * FROM veicoli WHERE id = ?'), (veicolo_id,))
            return cursor.fetchone()

    def aggiorna_km_veicolo(self, veicolo_id, nuovi_km):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(self._q('UPDATE veicoli SET km_attuali = ? WHERE id = ?'), (nuovi_km, veicolo_id))
            conn.commit()

    def elimina_veicolo(self, veicolo_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(self._q('DELETE FROM veicoli WHERE id = ?'), (veicolo_id,))
            conn.commit()

    def inserisci_manutenzione(self, veicolo_id, data_intervento, km_intervento,
                             tipo_manutenzione, descrizione=None, costo=None,
                             prossima_manutenzione_km=None, prossima_manutenzione_data=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            new_id = self._execute_insert(
                cursor,
                '''INSERT INTO manutenzioni
                   (veicolo_id, data_intervento, km_intervento, tipo_manutenzione,
                    descrizione, costo, prossima_manutenzione_km, prossima_manutenzione_data)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (veicolo_id, data_intervento, km_intervento, tipo_manutenzione,
                 descrizione, costo, prossima_manutenzione_km, prossima_manutenzione_data),
            )
            conn.commit()

            veicolo = self.get_veicolo_by_id(veicolo_id)
            if veicolo and km_intervento > (veicolo[4] or 0):
                self.aggiorna_km_veicolo(veicolo_id, km_intervento)

            return new_id

    def get_manutenzioni_by_veicolo(self, veicolo_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                self._q('SELECT * FROM manutenzioni WHERE veicolo_id = ? ORDER BY data_intervento DESC'),
                (veicolo_id,),
            )
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
            cursor.execute(self._q('''
                SELECT m.*, v.nome as nome_veicolo, v.km_attuali
                FROM manutenzioni m
                JOIN veicoli v ON m.veicolo_id = v.id
                WHERE (m.prossima_manutenzione_data IS NOT NULL AND m.prossima_manutenzione_data <= ?)
                   OR (m.prossima_manutenzione_km IS NOT NULL AND v.km_attuali >= m.prossima_manutenzione_km)
                ORDER BY m.prossima_manutenzione_data, m.prossima_manutenzione_km
            '''), (today,))
            return cursor.fetchall()

    def elimina_manutenzione(self, manutenzione_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(self._q('DELETE FROM manutenzioni WHERE id = ?'), (manutenzione_id,))
            conn.commit()

    def get_statistiche_spese_veicolo(self, veicolo_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(self._q('''
                SELECT
                    COUNT(*) as num_interventi,
                    SUM(costo) as totale_spese,
                    AVG(costo) as media_spese,
                    MIN(data_intervento) as primo_intervento,
                    MAX(data_intervento) as ultimo_intervento
                FROM manutenzioni
                WHERE veicolo_id = ? AND costo IS NOT NULL
            '''), (veicolo_id,))
            return cursor.fetchone()

    def get_manutenzione_by_id(self, manutenzione_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(self._q('SELECT * FROM manutenzioni WHERE id = ?'), (manutenzione_id,))
            return cursor.fetchone()

    def aggiorna_manutenzione(self, manutenzione_id, veicolo_id, data_intervento,
                            km_intervento, tipo_manutenzione, descrizione=None,
                            costo=None, prossima_manutenzione_km=None,
                            prossima_manutenzione_data=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(self._q('''
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
            '''), (veicolo_id, data_intervento, km_intervento, tipo_manutenzione,
                  descrizione, costo, prossima_manutenzione_km,
                  prossima_manutenzione_data, manutenzione_id))
            conn.commit()
            return cursor.rowcount > 0

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
