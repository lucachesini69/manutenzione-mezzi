import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

class EmailBackup:
    def __init__(self):
        # Configurazione Gmail (usa variabili d'ambiente)
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email = os.environ.get('BACKUP_EMAIL')
        self.password = os.environ.get('BACKUP_EMAIL_PASSWORD')
        self.to_email = os.environ.get('BACKUP_TO_EMAIL', self.email)

    def backup_database(self, db_path='manutenzione.db'):
        """Invia backup via email"""
        if not all([self.email, self.password]):
            print("Credenziali email non configurate")
            return False

        if not os.path.exists(db_path):
            print(f"Database {db_path} non trovato")
            return False

        try:
            # Crea messaggio
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = self.to_email
            msg['Subject'] = f"Backup Manutenzione Mezzi - {datetime.now().strftime('%d/%m/%Y %H:%M')}"

            # Corpo del messaggio
            body = f"""
Backup automatico database manutenzione mezzi.

Data backup: {datetime.now().strftime('%d/%m/%Y alle %H:%M')}
Dimensione file: {os.path.getsize(db_path)} bytes

Questo backup è generato automaticamente dall'applicazione.
            """
            msg.attach(MIMEText(body, 'plain'))

            # Allega database
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"manutenzione_backup_{timestamp}.db"

            with open(db_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())

            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}',
            )
            msg.attach(part)

            # Invia email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()

            print(f"✅ Backup email inviato a: {self.to_email}")
            return True

        except Exception as e:
            print(f"❌ Errore backup email: {e}")
            return False

if __name__ == "__main__":
    from email.mime.text import MIMEText
    backup = EmailBackup()
    backup.backup_database()