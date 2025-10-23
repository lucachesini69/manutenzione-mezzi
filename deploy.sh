#!/bin/bash

# ===========================================
# 🚀 SCRIPT AUTOMATICO DEPLOYMENT
# Manutenzione Mezzi - Deploy Automatizzato
# ===========================================

set -e  # Esci in caso di errore

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔════════════════════════════════════════════╗"
echo "║   🚀 DEPLOY AUTOMATICO MANUTENZIONE MEZZI  ║"
echo "╔════════════════════════════════════════════╝"
echo -e "${NC}"

# Funzione per stampare messaggi
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Controlla se siamo nella directory corretta
if [ ! -f "app.py" ] || [ ! -f "requirements.txt" ]; then
    print_error "Errore: esegui questo script dalla directory del progetto manutenzione-mezzi"
    exit 1
fi

print_success "Directory del progetto trovata!"

# ===========================================
# STEP 1: Verifica dipendenze
# ===========================================

echo ""
print_info "STEP 1/6: Verifica dipendenze..."

# Controlla Git
if ! command -v git &> /dev/null; then
    print_error "Git non installato. Installalo da https://git-scm.com/"
    exit 1
fi
print_success "Git installato"

# Controlla Python
if ! command -v python3 &> /dev/null; then
    print_error "Python3 non installato. Installalo da https://python.org/"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
print_success "$PYTHON_VERSION installato"

# ===========================================
# STEP 2: Genera SECRET_KEY
# ===========================================

echo ""
print_info "STEP 2/6: Generazione SECRET_KEY sicura..."

SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
print_success "SECRET_KEY generata: ${SECRET_KEY:0:16}...${SECRET_KEY: -8}"

# Salva in file .env locale
if [ ! -f ".env" ]; then
    cat > .env <<EOF
# Environment variables per sviluppo locale
# NON committare questo file!

FLASK_ENV=development
SECRET_KEY=$SECRET_KEY
DATABASE_PATH=manutenzione.db
LOG_LEVEL=INFO
EOF
    print_success "File .env creato per sviluppo locale"
else
    print_warning "File .env già esistente, non modificato"
fi

# ===========================================
# STEP 3: Verifica repository Git
# ===========================================

echo ""
print_info "STEP 3/6: Verifica repository Git..."

# Controlla se è un repo Git
if [ ! -d ".git" ]; then
    print_warning "Non è un repository Git. Inizializzo..."
    git init
    git add .
    git commit -m "Initial commit - Manutenzione Mezzi"
    print_success "Repository Git inizializzato"
fi

# Controlla se ci sono modifiche non committate
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    print_warning "Ci sono modifiche non committate"
    echo ""
    git status --short
    echo ""
    read -p "Vuoi committare le modifiche? (s/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[SsYy]$ ]]; then
        git add .
        read -p "Messaggio commit (premi INVIO per default): " COMMIT_MSG
        if [ -z "$COMMIT_MSG" ]; then
            COMMIT_MSG="Update per deployment automatico"
        fi
        git commit -m "$COMMIT_MSG"
        print_success "Modifiche committate"
    fi
fi

# Controlla remote
if ! git remote get-url origin &> /dev/null; then
    print_warning "Nessun remote GitHub configurato"
    echo ""
    print_info "Per connettere a GitHub:"
    echo "1. Crea un repository su https://github.com/new"
    echo "2. Esegui: git remote add origin https://github.com/TUO_USERNAME/manutenzione-mezzi.git"
    echo "3. Esegui: git push -u origin main"
else
    REMOTE_URL=$(git remote get-url origin)
    print_success "Remote GitHub: $REMOTE_URL"
fi

# ===========================================
# STEP 4: Scelta piattaforma deployment
# ===========================================

echo ""
print_info "STEP 4/6: Scegli piattaforma di deployment"
echo ""
echo "Piattaforme disponibili:"
echo "  1) Railway (consigliato - più semplice)"
echo "  2) Render (alternativa gratuita)"
echo "  3) Heroku (a pagamento dal 2022)"
echo "  4) Test locale con Ngrok"
echo "  5) Solo configurazione (esci)"
echo ""
read -p "Scegli opzione (1-5): " -n 1 -r PLATFORM_CHOICE
echo ""

# ===========================================
# STEP 5: Deployment specifico per piattaforma
# ===========================================

echo ""
print_info "STEP 5/6: Configurazione deployment..."

case $PLATFORM_CHOICE in
    1)
        # RAILWAY
        print_info "Deployment su Railway..."
        echo ""

        # Controlla se Railway CLI è installato
        if command -v railway &> /dev/null; then
            print_success "Railway CLI già installato"

            # Login
            print_info "Esegui login su Railway..."
            railway login

            # Inizializza progetto
            if [ ! -f "railway.json" ]; then
                railway init
                print_success "Progetto Railway inizializzato"
            fi

            # Aggiungi variabili ambiente
            print_info "Configurazione variabili ambiente..."
            railway variables set SECRET_KEY="$SECRET_KEY"
            railway variables set FLASK_ENV="production"

            # Deploy
            print_info "Deployment in corso..."
            railway up

            # Ottieni URL
            print_success "Deployment completato!"
            echo ""
            railway open

        else
            print_warning "Railway CLI non installato"
            echo ""
            print_info "Segui questi passi:"
            echo "1. Installa Railway CLI:"
            echo "   npm install -g @railway/cli"
            echo "   (oppure: brew install railway)"
            echo ""
            echo "2. Ri-esegui questo script"
            echo ""
            print_info "OPPURE usa la dashboard web:"
            echo "1. Vai su https://railway.app"
            echo "2. Login con GitHub"
            echo "3. New Project → Deploy from GitHub repo"
            echo "4. Seleziona: manutenzione-mezzi"
            echo "5. Aggiungi variabile ambiente:"
            echo "   SECRET_KEY = $SECRET_KEY"
            echo ""
        fi
        ;;

    2)
        # RENDER
        print_info "Deployment su Render..."
        echo ""
        print_info "Segui questi passi:"
        echo "1. Vai su https://render.com"
        echo "2. Registrati/Login con GitHub"
        echo "3. Click 'New' → 'Web Service'"
        echo "4. Connetti il repository: manutenzione-mezzi"
        echo "5. Configurazione:"
        echo "   - Name: manutenzione-mezzi"
        echo "   - Build Command: pip install -r requirements.txt"
        echo "   - Start Command: gunicorn app:app"
        echo ""
        echo "6. Variabili ambiente (Environment):"
        echo "   SECRET_KEY = $SECRET_KEY"
        echo "   FLASK_ENV = production"
        echo ""
        echo "7. Click 'Create Web Service'"
        echo ""
        print_success "Il deploy richiederà 2-3 minuti"
        ;;

    3)
        # HEROKU
        print_warning "Heroku non è più gratuito dal 2022"
        echo ""
        print_info "Alternativa consigliata: Railway o Render (gratuiti)"
        ;;

    4)
        # NGROK (test locale)
        print_info "Test locale con Ngrok..."
        echo ""

        # Installa dipendenze
        print_info "Installazione dipendenze Python..."
        python3 -m pip install -r requirements.txt --quiet

        # Controlla Ngrok
        if ! command -v ngrok &> /dev/null; then
            print_warning "Ngrok non installato"
            echo ""
            echo "1. Scarica da https://ngrok.com/download"
            echo "2. Registrati su https://dashboard.ngrok.com/signup"
            echo "3. Configura il token: ngrok config add-authtoken <TOKEN>"
            echo ""
            exit 1
        fi

        print_success "Ngrok installato"

        # Avvia app in background
        print_info "Avvio applicazione locale..."
        python3 app.py &
        APP_PID=$!

        sleep 3

        # Avvia Ngrok
        print_info "Avvio tunnel Ngrok..."
        echo ""
        print_success "App in esecuzione! Premi CTRL+C per fermare"
        echo ""

        ngrok http 5001

        # Cleanup
        kill $APP_PID 2>/dev/null
        ;;

    5)
        print_info "Solo configurazione - nessun deployment"
        ;;

    *)
        print_error "Opzione non valida"
        exit 1
        ;;
esac

# ===========================================
# STEP 6: Riepilogo e istruzioni finali
# ===========================================

echo ""
print_info "STEP 6/6: Riepilogo"
echo ""

cat << EOF
╔════════════════════════════════════════════════════════╗
║            📋 CONFIGURAZIONE COMPLETATA                 ║
╚════════════════════════════════════════════════════════╝

📁 File creati/aggiornati:
   ✅ .env (variabili ambiente locali)
   ✅ .env.example (template per produzione)
   ✅ Procfile (configurazione Railway/Heroku)
   ✅ gunicorn.conf.py (server production)
   ✅ requirements.txt (dipendenze)

🔐 Secret Key generata:
   SECRET_KEY = $SECRET_KEY

   ⚠️  IMPORTANTE: Copia questa chiave nelle variabili
   ambiente della piattaforma scelta!

📚 Documentazione:
   - README.md (introduzione)
   - DEPLOY_ONLINE.md (guida deployment)
   - .env.example (variabili ambiente)

🌐 Repository GitHub:
   $(git remote get-url origin 2>/dev/null || echo "Non configurato")

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 PROSSIMI PASSI:

1. Configura deployment sulla piattaforma scelta
2. Aggiungi SECRET_KEY nelle variabili ambiente
3. Verifica che l'app funzioni correttamente
4. (Opzionale) Configura backup automatici

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆘 SERVE AIUTO?

Railway:   https://docs.railway.app/
Render:    https://render.com/docs
GitHub:    https://github.com/lucachesini69/manutenzione-mezzi

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EOF

print_success "Setup completato con successo! 🎉"
echo ""
