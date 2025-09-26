@echo off
chcp 65001 > nul
cls

echo.
echo ==========================================
echo    GESTIONE MANUTENZIONE MEZZI
echo ==========================================
echo.

echo Controllo dipendenze Python...
python --version > nul 2>&1
if errorlevel 1 (
    echo ERRORE: Python non trovato!
    echo Installa Python da https://python.org
    pause
    exit /b 1
)

echo Installazione dipendenze...
pip install -r requirements.txt > nul 2>&1
if errorlevel 1 (
    echo ERRORE: Impossibile installare le dipendenze
    echo Esegui manualmente: pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo Avvio dell'applicazione...
echo.
echo L'applicazione sara' disponibile su:
echo http://localhost:5000
echo.
echo Per fermare l'applicazione premi CTRL+C
echo.

python app.py

echo.
echo Applicazione terminata.
pause