import dropbox
import os
from datetime import datetime

class DropboxBackup:
    def __init__(self):
        # Token di accesso (da configurare)
        self.access_token = os.environ.get('DROPBOX_ACCESS_TOKEN')
        self.dbx = None

        if self.access_token:
            self.dbx = dropbox.Dropbox(self.access_token)

    def backup_database(self, db_path='manutenzione.db'):
        """Esegue backup su Dropbox"""
        if not self.dbx:
            print("Token Dropbox non configurato")
            return False

        if not os.path.exists(db_path):
            print(f"Database {db_path} non trovato")
            return False

        try:
            # Nome file con timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            remote_path = f'/manutenzione_backup_{timestamp}.db'

            # Upload file
            with open(db_path, 'rb') as f:
                self.dbx.files_upload(f.read(), remote_path)

            print(f"✅ Backup Dropbox completato: {remote_path}")
            return True

        except Exception as e:
            print(f"❌ Errore backup Dropbox: {e}")
            return False

    def cleanup_old_backups(self, keep_count=10):
        """Elimina backup vecchi"""
        if not self.dbx:
            return

        try:
            # Lista files
            result = self.dbx.files_list_folder('')
            backups = [f for f in result.entries if f.name.startswith('manutenzione_backup')]

            # Ordina per data (più vecchi prima)
            backups.sort(key=lambda x: x.name)

            # Elimina i più vecchi
            for backup in backups[:-keep_count]:
                self.dbx.files_delete_v2(f'/{backup.name}')
                print(f"🗑️ Eliminato: {backup.name}")

        except Exception as e:
            print(f"Errore pulizia Dropbox: {e}")

if __name__ == "__main__":
    backup = DropboxBackup()
    backup.backup_database()