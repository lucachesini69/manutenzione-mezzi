@echo off
echo.
echo ========================================
echo   GESTIONE MANUTENZIONE MEZZI
echo ========================================
echo.
echo Installazione dipendenze...
pip install -r requirements.txt
echo.
echo Avvio dell'applicazione...
echo L'applicazione sara' disponibile su:
echo http://localhost:5000
echo.
echo Premi CTRL+C per fermare l'applicazione
echo.
python app.py
pause