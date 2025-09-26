from msal import PublicClientApplication
import json

# Le tue credenziali
CLIENT_ID = "a119a8e9-6907-4e2c-af70-ac44edfddc5e"

print("Autorizzazione OneDrive per Manutenzione Mezzi")
print("=" * 50)

# Crea l'app MSAL
app = PublicClientApplication(
    CLIENT_ID,
    authority="https://login.microsoftonline.com/consumers"
)

# Scope necessari per OneDrive
scopes = ["https://graph.microsoft.com/Files.ReadWrite"]

print("Si aprira il browser per l'autorizzazione...")
print("Accedi con lo stesso account del tuo OneDrive")
print()

try:
    # Avvia il flusso di autorizzazione interattiva
    result = app.acquire_token_interactive(scopes=scopes)

    if "access_token" in result:
        print("AUTORIZZAZIONE RIUSCITA!")
        print("=" * 50)
        print()

        # Mostra le informazioni per Render
        print("COPIA QUESTE INFORMAZIONI PER RENDER:")
        print()
        print("Environment Variables da aggiungere:")
        print(f"ONEDRIVE_CLIENT_ID = {CLIENT_ID}")
        print("ONEDRIVE_CLIENT_SECRET = [il segreto che hai copiato prima]")
        print()
        print("ONEDRIVE_TOKEN = (copia tutto il JSON qui sotto su UNA SOLA RIGA)")
        print("=" * 50)
        print(json.dumps(result, indent=2))
        print("=" * 50)
        print()
        print("Configurazione completata!")

    else:
        print("ERRORE DURANTE L'AUTORIZZAZIONE:")
        print(f"Errore: {result.get('error')}")
        print(f"Descrizione: {result.get('error_description')}")

except Exception as e:
    print(f"ERRORE: {e}")
    print()
    print("SUGGERIMENTI:")
    print("- Assicurati di avere una connessione internet")
    print("- Usa lo stesso account del tuo OneDrive")
    print("- Se non si apre il browser, copia e incolla l'URL manualmente")

input("\nPremi INVIO per chiudere...")