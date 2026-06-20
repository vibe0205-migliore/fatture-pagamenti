import imaplib
import email
import os

DOWNLOAD_DIR = "./da_caricare" 
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

ACCOUNT_CONFIGS = [
    {"email": "lulodig@gmail.com", "password": "oqzwryybiqnshzml", "imap_server": "imap.gmail.com"},
    {"email": "vibe0205@gmail.com", "password": "ytriylikvrxejwjz", "imap_server": "imap.gmail.com"},
    {"email": "lodigiani@avb-engineering.com", "password": "ounueffsegpcrrzo", "imap_server": "imap.gmail.com"}
]

def scarica_da_account(config):
    try:
        mail = imaplib.IMAP4_SSL(config["imap_server"])
        mail.login(config["email"], config["password"])
        mail.select("inbox")

        # Cerca solo le email NON LETTE
        status, messages = mail.search(None, 'UNSEEN')
        if status != "OK" or not messages[0]:
            print(f"[{config['email']}] Nessuna nuova email non letta.")
            mail.logout()
            return

        # Converte correttamente l'elenco dei messaggi sia per stringhe che per byte
        id_list = messages[0].split()

        for num in id_list:
            status, data = mail.fetch(num, '(RFC822)')
            if status != "OK":
                continue
                
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            for part in msg.walk():
                if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                    continue

                filename = part.get_filename()
                if filename:
                    # Pulisce il nome del file da caratteri non validi
                    filename = "".join(c for c in filename if c.isalnum() or c in ('.', '_', '-'))
                    filepath = os.path.join(DOWNLOAD_DIR, filename)
                    
                    with open(filepath, "wb") as f:
                        f.write(part.get_payload(decode=True))
                    print(f"[{config['email']}] Scaricato con successo: {filename}")
                    
        mail.logout()
    except Exception as e:
        print(f"Errore su {config['email']}: {e}")

for account in ACCOUNT_CONFIGS:
    print(f"Controllo in corso su: {account['email']}...")
    scarica_da_account(account)
