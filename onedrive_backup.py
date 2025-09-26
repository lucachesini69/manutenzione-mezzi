import os
import requests
import json
from datetime import datetime
from msal import ConfidentialClientApplication, PublicClientApplication

class OneDriveBackup:
    def __init__(self):
        # Configurazione Microsoft Graph API
        self.client_id = os.environ.get('ONEDRIVE_CLIENT_ID')
        self.client_secret = os.environ.get('ONEDRIVE_CLIENT_SECRET')
        self.tenant_id = os.environ.get('ONEDRIVE_TENANT_ID', 'common')
        self.access_token = None

        # Microsoft Graph endpoints
        self.graph_url = 'https://graph.microsoft.com/v1.0'
        self.scopes = ['https://graph.microsoft.com/Files.ReadWrite']

    def authenticate(self):
        """Autentica con Microsoft Graph usando le credenziali dell'app"""
        if not self.client_id:
            print("Credenziali OneDrive non configurate")
            return False

        try:
            # Prova prima con le credenziali dell'app (se disponibili)
            if self.client_secret:
                app = ConfidentialClientApplication(
                    self.client_id,
                    authority=f"https://login.microsoftonline.com/{self.tenant_id}",
                    client_credential=self.client_secret,
                )
                # Client credentials flow per app
                result = app.acquire_token_for_client(scopes=['https://graph.microsoft.com/.default'])
            else:
                # Usa token esistente dalle variabili d'ambiente
                token_data = os.environ.get('ONEDRIVE_TOKEN')
                if not token_data:
                    print("Token OneDrive non trovato")
                    return False

                token_info = json.loads(token_data)
                self.access_token = token_info.get('access_token')
                return True

            if "access_token" in result:
                self.access_token = result["access_token"]
                return True
            else:
                print(f"Errore autenticazione: {result.get('error_description', 'Unknown error')}")
                return False

        except Exception as e:
            print(f"Errore autenticazione OneDrive: {e}")
            return False

    def get_or_create_backup_folder(self):
        """Crea o trova la cartella di backup"""
        if not self.access_token:
            return None

        folder_name = "Manutenzione_Mezzi_Backup"
        headers = {'Authorization': f'Bearer {self.access_token}'}

        try:
            # Cerca se la cartella esiste
            search_url = f"{self.graph_url}/me/drive/root/children"
            response = requests.get(search_url, headers=headers)

            if response.status_code == 200:
                items = response.json().get('value', [])
                for item in items:
                    if item.get('name') == folder_name and 'folder' in item:
                        return item['id']

            # Crea nuova cartella
            create_url = f"{self.graph_url}/me/drive/root/children"
            folder_data = {
                "name": folder_name,
                "folder": {},
                "@microsoft.graph.conflictBehavior": "rename"
            }

            response = requests.post(create_url, headers=headers, json=folder_data)

            if response.status_code == 201:
                return response.json()['id']
            else:
                print(f"Errore creazione cartella: {response.text}")
                return None

        except Exception as e:
            print(f"Errore gestione cartella: {e}")
            return None

    def backup_database(self, db_path='manutenzione.db'):
        """Esegue backup del database su OneDrive"""
        if not self.authenticate():
            return False

        folder_id = self.get_or_create_backup_folder()
        if not folder_id:
            return False

        if not os.path.exists(db_path):
            print(f"Database {db_path} non trovato")
            return False

        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f'manutenzione_backup_{timestamp}.db'

            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/octet-stream'
            }

            # Upload del file
            upload_url = f"{self.graph_url}/me/drive/items/{folder_id}:/{backup_filename}:/content"

            with open(db_path, 'rb') as file:
                response = requests.put(upload_url, headers=headers, data=file)

            if response.status_code in [200, 201]:
                print(f"✅ Backup OneDrive completato: {backup_filename}")
                return True
            else:
                print(f"❌ Errore upload: {response.text}")
                return False

        except Exception as e:
            print(f"❌ Errore backup OneDrive: {e}")
            return False

    def cleanup_old_backups(self, keep_count=10):
        """Mantiene solo gli ultimi N backup"""
        if not self.access_token:
            return

        folder_id = self.get_or_create_backup_folder()
        if not folder_id:
            return

        try:
            headers = {'Authorization': f'Bearer {self.access_token}'}
            list_url = f"{self.graph_url}/me/drive/items/{folder_id}/children"

            response = requests.get(list_url, headers=headers)

            if response.status_code == 200:
                items = response.json().get('value', [])
                backups = [item for item in items if item['name'].startswith('manutenzione_backup')]

                # Ordina per data di creazione (più vecchi prima)
                backups.sort(key=lambda x: x['createdDateTime'])

                # Elimina i backup più vecchi
                for backup in backups[:-keep_count]:
                    delete_url = f"{self.graph_url}/me/drive/items/{backup['id']}"
                    delete_response = requests.delete(delete_url, headers=headers)

                    if delete_response.status_code == 204:
                        print(f"🗑️ Eliminato backup vecchio: {backup['name']}")

        except Exception as e:
            print(f"Errore pulizia backup: {e}")

def test_backup():
    """Testa la funzionalità di backup"""
    backup = OneDriveBackup()
    return backup.backup_database()

if __name__ == "__main__":
    test_backup()