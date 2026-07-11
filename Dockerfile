# Immagine per "Gestione Manutenzione Mezzi"
FROM python:3.11-slim

# Output dei log in tempo reale, niente file .pyc
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

WORKDIR /app

# Installa prima le dipendenze (sfrutta la cache di Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice dell'applicazione
COPY . .

EXPOSE 8000

# Avvia con Gunicorn (usa gunicorn.conf.py, che legge la porta da $PORT)
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
