# Configurazione applicazione Gestione Manutenzione Mezzi

# Configurazione database
DATABASE_PATH = 'manutenzione.db'

# Configurazione server
HOST = '0.0.0.0'
PORT = 5000
DEBUG = True

# Chiave segreta per sessioni (cambiala per la produzione)
SECRET_KEY = 'change-this-secret-key-in-production'

# Configurazione backup automatico
AUTO_BACKUP_ENABLED = False
AUTO_BACKUP_INTERVAL_DAYS = 7
BACKUP_DIRECTORY = 'backups'

# Limiti applicazione
MAX_VEHICLES = 100
MAX_MAINTENANCES_PER_VEHICLE = 1000

# Configurazione export
EXPORT_DATE_FORMAT = '%Y-%m-%d'
EXPORT_CURRENCY_SYMBOL = '€'

# Temi disponibili
AVAILABLE_THEMES = ['light', 'dark']
DEFAULT_THEME = 'light'

# Lingue supportate (futuro)
SUPPORTED_LANGUAGES = ['it']
DEFAULT_LANGUAGE = 'it'

# Formati data supportati
DATE_FORMATS = {
    'it': '%d/%m/%Y',
    'en': '%m/%d/%Y',
    'iso': '%Y-%m-%d'
}

# Valute supportate
CURRENCIES = {
    'EUR': '€',
    'USD': '$',
    'GBP': '£'
}

# Configurazione notifiche promemoria
REMINDER_ADVANCE_DAYS = 30  # Giorni di anticipo per promemoria
REMINDER_ADVANCE_KM = 1000  # Km di anticipo per promemoria

# Tipi di veicoli personalizzabili
CUSTOM_VEHICLE_TYPES = [
    'Auto',
    'Moto',
    'Scooter',
    'Bicicletta',
    'Camper',
    'Furgone',
    'Autocarro',
    'Quad',
    'Altro'
]

# Tipi di manutenzione personalizzabili
CUSTOM_MAINTENANCE_TYPES = [
    'Cambio olio motore',
    'Cambio filtro olio',
    'Cambio filtro aria',
    'Cambio filtro carburante',
    'Cambio gomme',
    'Equilibratura e convergenza',
    'Controllo freni',
    'Cambio pastiglie freni',
    'Cambio dischi freni',
    'Revisione generale',
    'Tagliando',
    'Cambio batteria',
    'Controllo climatizzatore',
    'Cambio catena distribuzione',
    'Cambio cinghia distribuzione',
    'Controllo sospensioni',
    'Altro'
]

# Configurazione logging
LOGGING_ENABLED = True
LOG_LEVEL = 'INFO'
LOG_FILE = 'app.log'

# Configurazione sicurezza
ENABLE_CSRF_PROTECTION = True  # Abilitato per sicurezza
SECURE_HEADERS = True  # Abilitato per sicurezza

# Configurazione performance
CACHE_ENABLED = False
CACHE_TIMEOUT = 300  # 5 minuti

# Configurazione development
FLASK_ENV = 'development'
TEMPLATES_AUTO_RELOAD = True
STATIC_AUTO_RELOAD = True