"""
Modulo per la configurazione centralizzata del logging
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from config import LOGGING_ENABLED, LOG_LEVEL, LOG_FILE


def setup_logger(name='manutenzione_mezzi'):
    """
    Configura e restituisce un logger con handler per file e console

    Args:
        name: Nome del logger (default: 'manutenzione_mezzi')

    Returns:
        Logger configurato
    """
    # Crea logger
    logger = logging.getLogger(name)

    # Evita duplicazione di handler
    if logger.handlers:
        return logger

    # Imposta livello da config o variabile ambiente
    log_level = os.environ.get('LOG_LEVEL', LOG_LEVEL)
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Formato log
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler console (sempre attivo per vedere i log)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # Handler file (solo se logging abilitato)
    if LOGGING_ENABLED:
        log_file = os.environ.get('LOG_FILE', LOG_FILE)

        # Crea directory per i log se non esiste
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # RotatingFileHandler per evitare file troppo grandi
        # Max 10MB per file, mantiene 5 backup
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

    return logger


# Logger di default per l'applicazione
logger = setup_logger()


def get_logger(name):
    """
    Ottiene un logger specifico per un modulo

    Args:
        name: Nome del logger (di solito __name__ del modulo)

    Returns:
        Logger configurato
    """
    return setup_logger(name)
