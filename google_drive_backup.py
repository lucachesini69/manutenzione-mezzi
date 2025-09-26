import os
import shutil
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import json

SCOPES = ['https://www.googleapis.com/auth/drive.file']

class GoogleDriveBackup:
    def __init__(self):
        self.service = None
        self.folder_id = None

    def authenticate(self):
        """Autentica con Google Drive usando variabili d'ambiente"""
        creds = None

        # Prova a caricare le credenziali dalle variabili d'ambiente
        if os.environ.get('GOOGLE_CREDENTIALS'):
            creds_data = json.loads(os.environ.get('GOOGLE_CREDENTIALS'))
            creds = Credentials.from_authorized_user_info(creds_data, SCOPES)

        # Se non ci sono credenziali valide, non possiamo continuare
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Errore nel refresh delle credenziali: {e}")
                    return False
            else:
                print("Credenziali Google Drive non configurate")
                return False

        self.service = build('drive', 'v3', credentials=creds)
        return True

    def get_or_create_backup_folder(self):
        """Crea o trova la cartella di backup"""
        if not self.service:
            return None

        folder_name = "Manutenzione_Mezzi_Backup"

        # Cerca se la cartella esiste già
        results = self.service.files().list(
            q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
            spaces='drive'
        ).execute()

        items = results.get('files', [])

        if items:
            self.folder_id = items[0]['id']
            return self.folder_id

        # Crea nuova cartella
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        folder = self.service.files().create(
            body=folder_metadata,
            fields='id'
        ).execute()

        self.folder_id = folder.get('id')
        return self.folder_id

    def backup_database(self, db_path='manutenzione.db'):
        """Esegue il backup del database su Google Drive"""
        if not self.authenticate():
            return False

        if not self.get_or_create_backup_folder():
            return False

        if not os.path.exists(db_path):
            print(f"Database {db_path} non trovato")
            return False

        # Crea nome file con timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'manutenzione_backup_{timestamp}.db'

        try:
            # Upload del file
            media = MediaFileUpload(db_path, mimetype='application/x-sqlite3')

            file_metadata = {
                'name': backup_filename,
                'parents': [self.folder_id]
            }

            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name'
            ).execute()

            print(f"✅ Backup completato: {backup_filename}")
            return True

        except Exception as e:
            print(f"❌ Errore durante il backup: {e}")
            return False

    def cleanup_old_backups(self, keep_count=10):
        """Mantiene solo gli ultimi N backup"""
        if not self.service or not self.folder_id:
            return

        try:
            # Lista tutti i backup nella cartella
            results = self.service.files().list(
                q=f"'{self.folder_id}' in parents and name contains 'manutenzione_backup'",
                orderBy='createdTime desc',
                spaces='drive'
            ).execute()

            items = results.get('files', [])

            # Elimina i backup più vecchi
            for item in items[keep_count:]:
                self.service.files().delete(fileId=item['id']).execute()
                print(f"🗑️ Eliminato backup vecchio: {item['name']}")

        except Exception as e:
            print(f"Errore durante la pulizia: {e}")

def test_backup():
    """Testa la funzionalità di backup"""
    backup = GoogleDriveBackup()
    return backup.backup_database()

if __name__ == "__main__":
    test_backup()