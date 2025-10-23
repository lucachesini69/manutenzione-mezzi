@echo off
REM ===========================================
REM 🚀 SCRIPT AUTOMATICO DEPLOYMENT - WINDOWS
REM Manutenzione Mezzi - Deploy Automatizzato
REM ===========================================

setlocal enabledelayedexpansion

REM Colori (limitati su Windows CMD)
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

REM Banner
echo.
echo ╔════════════════════════════════════════════╗
echo ║   🚀 DEPLOY AUTOMATICO MANUTENZIONE MEZZI  ║
echo ╚════════════════════════════════════════════╝
echo.

REM Controlla se siamo nella directory corretta
if not exist "app.py" (
    echo %RED%❌ Errore: esegui questo script dalla directory del progetto%NC%
    pause
    exit /b 1
)

echo %GREEN%✅ Directory del progetto trovata!%NC%

REM ===========================================
REM STEP 1: Verifica dipendenze
REM ===========================================

echo.
echo %BLUE%ℹ️  STEP 1/6: Verifica dipendenze...%NC%

REM Controlla Git
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo %RED%❌ Git non installato. Scaricalo da https://git-scm.com/%NC%
    pause
    exit /b 1
)
echo %GREEN%✅ Git installato%NC%

REM Controlla Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo %RED%❌ Python non installato. Scaricalo da https://python.org/%NC%
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo %GREEN%✅ !PYTHON_VERSION! installato%NC%

REM ===========================================
REM STEP 2: Genera SECRET_KEY
REM ===========================================

echo.
echo %BLUE%ℹ️  STEP 2/6: Generazione SECRET_KEY sicura...%NC%

for /f "tokens=*" %%i in ('python -c "import secrets; print(secrets.token_hex(32))"') do set SECRET_KEY=%%i
echo %GREEN%✅ SECRET_KEY generata%NC%

REM Salva in file .env locale
if not exist ".env" (
    (
        echo # Environment variables per sviluppo locale
        echo # NON committare questo file!
        echo.
        echo FLASK_ENV=development
        echo SECRET_KEY=!SECRET_KEY!
        echo DATABASE_PATH=manutenzione.db
        echo LOG_LEVEL=INFO
    ) > .env
    echo %GREEN%✅ File .env creato per sviluppo locale%NC%
) else (
    echo %YELLOW%⚠️  File .env già esistente, non modificato%NC%
)

REM ===========================================
REM STEP 3: Verifica repository Git
REM ===========================================

echo.
echo %BLUE%ℹ️  STEP 3/6: Verifica repository Git...%NC%

if not exist ".git" (
    echo %YELLOW%⚠️  Non è un repository Git. Inizializzo...%NC%
    git init
    git add .
    git commit -m "Initial commit - Manutenzione Mezzi"
    echo %GREEN%✅ Repository Git inizializzato%NC%
)

REM Controlla remote
git remote get-url origin >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo %YELLOW%⚠️  Nessun remote GitHub configurato%NC%
    echo.
    echo Per connettere a GitHub:
    echo 1. Crea un repository su https://github.com/new
    echo 2. Esegui: git remote add origin https://github.com/TUO_USERNAME/manutenzione-mezzi.git
    echo 3. Esegui: git push -u origin main
) else (
    for /f "tokens=*" %%i in ('git remote get-url origin') do set REMOTE_URL=%%i
    echo %GREEN%✅ Remote GitHub: !REMOTE_URL!%NC%
)

REM ===========================================
REM STEP 4: Scelta piattaforma deployment
REM ===========================================

echo.
echo %BLUE%ℹ️  STEP 4/6: Scegli piattaforma di deployment%NC%
echo.
echo Piattaforme disponibili:
echo   1^) Railway ^(consigliato - più semplice^)
echo   2^) Render ^(alternativa gratuita^)
echo   3^) Test locale con Ngrok
echo   4^) Solo configurazione ^(esci^)
echo.
set /p PLATFORM_CHOICE="Scegli opzione (1-4): "

REM ===========================================
REM STEP 5: Deployment specifico per piattaforma
REM ===========================================

echo.
echo %BLUE%ℹ️  STEP 5/6: Configurazione deployment...%NC%
echo.

if "%PLATFORM_CHOICE%"=="1" (
    REM RAILWAY
    echo %BLUE%Deployment su Railway...%NC%
    echo.

    where railway >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        echo %GREEN%✅ Railway CLI già installato%NC%

        echo %BLUE%ℹ️  Esegui login su Railway...%NC%
        call railway login

        if not exist "railway.json" (
            call railway init
            echo %GREEN%✅ Progetto Railway inizializzato%NC%
        )

        echo %BLUE%ℹ️  Configurazione variabili ambiente...%NC%
        call railway variables set SECRET_KEY="!SECRET_KEY!"
        call railway variables set FLASK_ENV="production"

        echo %BLUE%ℹ️  Deployment in corso...%NC%
        call railway up

        echo %GREEN%✅ Deployment completato!%NC%
        call railway open

    ) else (
        echo %YELLOW%⚠️  Railway CLI non installato%NC%
        echo.
        echo Segui questi passi:
        echo 1. Installa Node.js da https://nodejs.org/
        echo 2. Apri un nuovo prompt dei comandi e esegui:
        echo    npm install -g @railway/cli
        echo 3. Ri-esegui questo script
        echo.
        echo OPPURE usa la dashboard web:
        echo 1. Vai su https://railway.app
        echo 2. Login con GitHub
        echo 3. New Project → Deploy from GitHub repo
        echo 4. Seleziona: manutenzione-mezzi
        echo 5. Aggiungi variabile ambiente:
        echo    SECRET_KEY = !SECRET_KEY!
        echo.
    )

) else if "%PLATFORM_CHOICE%"=="2" (
    REM RENDER
    echo %BLUE%Deployment su Render...%NC%
    echo.
    echo Segui questi passi:
    echo 1. Vai su https://render.com
    echo 2. Registrati/Login con GitHub
    echo 3. Click 'New' → 'Web Service'
    echo 4. Connetti il repository: manutenzione-mezzi
    echo 5. Configurazione:
    echo    - Name: manutenzione-mezzi
    echo    - Build Command: pip install -r requirements.txt
    echo    - Start Command: gunicorn app:app
    echo.
    echo 6. Variabili ambiente ^(Environment^):
    echo    SECRET_KEY = !SECRET_KEY!
    echo    FLASK_ENV = production
    echo.
    echo 7. Click 'Create Web Service'
    echo.

) else if "%PLATFORM_CHOICE%"=="3" (
    REM NGROK
    echo %BLUE%Test locale con Ngrok...%NC%
    echo.

    echo %BLUE%ℹ️  Installazione dipendenze Python...%NC%
    python -m pip install -r requirements.txt --quiet

    where ngrok >nul 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo %YELLOW%⚠️  Ngrok non installato%NC%
        echo.
        echo 1. Scarica da https://ngrok.com/download
        echo 2. Estrai ngrok.exe in questa cartella o in PATH
        echo 3. Registrati su https://dashboard.ngrok.com/signup
        echo 4. Configura il token: ngrok config add-authtoken ^<TOKEN^>
        echo.
        pause
        exit /b 1
    )

    echo %GREEN%✅ Ngrok installato%NC%
    echo.
    echo %BLUE%ℹ️  Avvio applicazione locale...%NC%

    REM Avvia app in finestra separata
    start /b python app.py

    timeout /t 3 /nobreak >nul

    echo %BLUE%ℹ️  Avvio tunnel Ngrok...%NC%
    echo.
    echo %GREEN%✅ App in esecuzione! Premi CTRL+C per fermare%NC%
    echo.

    ngrok http 5001

) else if "%PLATFORM_CHOICE%"=="4" (
    echo %BLUE%ℹ️  Solo configurazione - nessun deployment%NC%

) else (
    echo %RED%❌ Opzione non valida%NC%
    pause
    exit /b 1
)

REM ===========================================
REM STEP 6: Riepilogo
REM ===========================================

echo.
echo %BLUE%ℹ️  STEP 6/6: Riepilogo%NC%
echo.

echo ╔════════════════════════════════════════════════════════╗
echo ║            📋 CONFIGURAZIONE COMPLETATA                 ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo 📁 File creati/aggiornati:
echo    ✅ .env ^(variabili ambiente locali^)
echo    ✅ .env.example ^(template per produzione^)
echo    ✅ Procfile ^(configurazione Railway/Heroku^)
echo    ✅ gunicorn.conf.py ^(server production^)
echo    ✅ requirements.txt ^(dipendenze^)
echo.
echo 🔐 Secret Key generata:
echo    SECRET_KEY = !SECRET_KEY!
echo.
echo    ⚠️  IMPORTANTE: Copia questa chiave nelle variabili
echo    ambiente della piattaforma scelta!
echo.
echo 📚 Documentazione:
echo    - README.md ^(introduzione^)
echo    - DEPLOY_ONLINE.md ^(guida deployment^)
echo    - .env.example ^(variabili ambiente^)
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 📖 PROSSIMI PASSI:
echo.
echo 1. Configura deployment sulla piattaforma scelta
echo 2. Aggiungi SECRET_KEY nelle variabili ambiente
echo 3. Verifica che l'app funzioni correttamente
echo 4. ^(Opzionale^) Configura backup automatici
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo %GREEN%✅ Setup completato con successo! 🎉%NC%
echo.

pause
