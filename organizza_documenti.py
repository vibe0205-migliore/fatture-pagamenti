import os
import shutil
from pypdf import PdfReader

SORGENTE = "./da_caricare"
DESTINAZIONI = {
    "01_Offerte": ["offerta", "preventivo", "quotazione", "proposta commerciale"],
    "02_Disegni": ["disegno", "pianta", "prospetto", "sezione", "dwg", "scala"],
    "03_Fatture": ["fattura", "totale da pagare", "iban", "scadenza", "esente iva"]
}
DEFAULT_FOLDER = "04_Altro_Non_Riconosciuto"

def analizza_testo_pdf(file_path):
    """Legge la prima pagina del PDF per cercare parole chiave"""
    try:
        reader = PdfReader(file_path)
        if len(reader.pages) > 0:
            # Estrae il testo e lo converte in minuscolo
            testo = reader.pages[0].extract_text().lower()
            return testo
    except Exception:
        pass
    return ""

def ordina_file():
    if not os.path.exists(SORGENTE):
        return

    file_presenti = [f for f in os.listdir(SORGENTE) if os.path.isfile(os.path.join(SORGENTE, f))]
    
    for filename in file_presenti:
        file_path = os.path.join(SORGENTE, filename)
        filename_lower = filename.lower()
        spostato = False
        
        # 1. PASSO: Controlla prima il nome del file (come faceva prima)
        for cartella_dest, parole_chiave in DESTINAZIONI.items():
            if any(parola in filename_lower for parola in parole_chiave):
                os.makedirs(cartella_dest, exist_ok=True)
                shutil.move(file_path, os.path.join(cartella_dest, filename))
                print(f"Smistato da Nome File: '{filename}' -> '{cartella_dest}'")
                spostato = True
                break
        
        if spostato:
            continue

        # 2. PASSO: Se il nome non dice nulla ed è un PDF, legge il CONTENUTO del testo
        if filename_lower.endswith('.pdf'):
            testo_contenuto = analizza_testo_pdf(file_path)
            
            for cartella_dest, parole_chiave in DESTINAZIONI.items():
                if any(parola in testo_contenuto for parola in parole_chiave):
                    os.makedirs(cartella_dest, exist_ok=True)
                    shutil.move(file_path, os.path.join(cartella_dest, filename))
                    print(f"Smistato da Contenuto PDF: '{filename}' -> '{cartella_dest}'")
                    spostato = True
                    break

        # 3. PASSO: Se non trova nulla, va nella cartella di default
        if not spostato:
            os.makedirs(DEFAULT_FOLDER, exist_ok=True)
            shutil.move(file_path, os.path.join(DEFAULT_FOLDER, filename))
            print(f"Non riconosciuto: '{filename}' -> spostato in '{DEFAULT_FOLDER}'")

if __name__ == "__main__":
    ordina_file()

