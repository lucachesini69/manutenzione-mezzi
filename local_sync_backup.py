import os
import shutil
from datetime import datetime
import platform

class LocalSyncBackup:
    def __init__(self):
        self.backup_folder = self.get_onedrive_backup_folder()

    def get_onedrive_backup_folder(self):
        """Trova automaticamente la cartella OneDrive e crea la cartella backup"""

        # Percorsi comuni di OneDrive su Windows
        username = os.getenv('USERNAME', 'User')
        possible_paths = [
            f"C:\\Users\\{username}\\OneDrive\\ManutenzioneBackup",
            f"C:\\Users\\{username}\\OneDrive - Personal\\ManutenzioneBackup",
            f"C:\\Users\\{username}\\OneDrive\\Documents\\ManutenzioneBackup",
            f"C:\\Users\\{username}\\Desktop\\ManutenzioneBackup",  # Fallback
            f"C:\\Users\\{username}\\Documents\\ManutenzioneBackup"  # Fallback 2
        ]

        # Prova a trovare OneDrive
        for path in possible_paths:
            base_dir = os.path.dirname(path)
            if os.path.exists(base_dir) or "OneDrive" in path:
                try:
                    os.makedirs(path, exist_ok=True)
                    print(f"Cartella backup creata: {path}")
                    return path
                except:
                    continue

        # Se OneDrive non trovato, usa Documents
        fallback_path = f"C:\\Users\\{username}\\Documents\\ManutenzioneBackup"
        os.makedirs(fallback_path, exist_ok=True)
        print(f"Cartella backup (fallback): {fallback_path}")
        return fallback_path

    def backup_database(self, db_path='manutenzione.db'):
        """Crea backup del database nella cartella sincronizzata"""

        if not os.path.exists(db_path):
            print(f"Database {db_path} non trovato")
            return False

        try:
            # Nome file con timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f'manutenzione_backup_{timestamp}.db'
            backup_path = os.path.join(self.backup_folder, backup_filename)

            # Copia il database
            shutil.copy2(db_path, backup_path)

            print(f"Backup salvato in: {backup_path}")
            print(f"OneDrive sincronizzera automaticamente il file")

            return True

        except Exception as e:
            print(f"Errore durante il backup: {e}")
            return False

    def cleanup_old_backups(self, keep_count=10):
        """Mantiene solo gli ultimi N backup"""

        if not os.path.exists(self.backup_folder):
            return

        try:
            # Lista tutti i backup
            backup_files = []
            for file in os.listdir(self.backup_folder):
                if file.startswith('manutenzione_backup_') and file.endswith('.db'):
                    file_path = os.path.join(self.backup_folder, file)
                    backup_files.append((file_path, os.path.getmtime(file_path)))

            # Ordina per data (più vecchi prima)
            backup_files.sort(key=lambda x: x[1])

            # Elimina i backup più vecchi
            for file_path, _ in backup_files[:-keep_count]:
                os.remove(file_path)
                filename = os.path.basename(file_path)
                print(f"Eliminato backup vecchio: {filename}")

        except Exception as e:
            print(f"Errore durante la pulizia: {e}")

    def get_backup_info(self):
        """Restituisce informazioni sui backup esistenti"""

        if not os.path.exists(self.backup_folder):
            return {
                'folder_path': self.backup_folder,
                'backup_count': 0,
                'latest_backup': None,
                'total_size': 0
            }

        try:
            backup_files = []
            total_size = 0

            for file in os.listdir(self.backup_folder):
                if file.startswith('manutenzione_backup_') and file.endswith('.db'):
                    file_path = os.path.join(self.backup_folder, file)
                    file_size = os.path.getsize(file_path)
                    file_date = datetime.fromtimestamp(os.path.getmtime(file_path))

                    backup_files.append({
                        'filename': file,
                        'path': file_path,
                        'size': file_size,
                        'date': file_date
                    })
                    total_size += file_size

            # Ordina per data (più recenti prima)
            backup_files.sort(key=lambda x: x['date'], reverse=True)

            return {
                'folder_path': self.backup_folder,
                'backup_count': len(backup_files),
                'latest_backup': backup_files[0] if backup_files else None,
                'total_size': total_size,
                'all_backups': backup_files
            }

        except Exception as e:
            print(f"Errore nel recupero info backup: {e}")
            return {
                'folder_path': self.backup_folder,
                'backup_count': 0,
                'latest_backup': None,
                'total_size': 0,
                'error': str(e)
            }

def test_backup():
    """Testa la funzionalità di backup"""
    backup = LocalSyncBackup()
    print(f"Cartella backup: {backup.backup_folder}")

    # Informazioni sui backup esistenti
    info = backup.get_backup_info()
    print(f"Backup esistenti: {info['backup_count']}")
    if info['latest_backup']:
        print(f"Ultimo backup: {info['latest_backup']['date']}")

    # Esegui test backup
    success = backup.backup_database()
    if success:
        print("Test backup completato!")
    else:
        print("Test backup fallito!")

    return success

if __name__ == "__main__":
    test_backup()