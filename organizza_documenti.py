import os
import shutil

# Cartella dove lo script delle email scarica gli allegati
SORGENTE = "./da_caricare"

# ASSOCIAZIONE PREFISSI -> CARTELLE DI DESTINAZIONE
# Puoi aggiungere nuove righe qui in futuro seguendo lo stesso schema
DESTINAZIONI = {
    "OFF_": "01_Offerte",
    "DIS_": "02_Disegni",
    "FAT_": "03_Fatture"
}

# Cartella dove finiscono i file che non hanno i prefissi sopra
DEFAULT_FOLDER = "04_Altro_Non_Riconosciuto"

def ordina_file():
    if not os.path.exists(SORGENTE):
        print("La cartella sorgente non esiste.")
        return

    file_presenti = [f for f in os.listdir(SORGENTE) if os.path.isfile(os.path.join(SORGENTE, f))]
    
    if not file_presenti:
        print("Nessun file presente nella cartella da smistare.")
        return

    for filename in file_presenti:
        file_path = os.path.join(SORGENTE, filename)
        spostato = False
        
        # Converte il nome in maiuscolo per evitare problemi con "off_" o "OFF_"
        filename_upper = filename.upper()
        
        # Cerca se il file inizia con uno dei prefissi configurati
        for prefisso, cartella_dest in DESTINAZIONI.items():
            if filename_upper.startswith(prefisso.upper()):
                os.makedirs(cartella_dest, exist_ok=True)
                shutil.move(file_path, os.path.join(cartella_dest, filename))
                print(f"Smistato: '{filename}' -> spostato in '{cartella_dest}'")
                spostato = True
                break
        
        # Se il file non corrisponde a nessuna regola, va nella cartella di default
        if not spostato:
            os.makedirs(DEFAULT_FOLDER, exist_ok=True)
            shutil.move(file_path, os.path.join(DEFAULT_FOLDER, filename))
            print(f"Non riconosciuto: '{filename}' -> spostato in '{DEFAULT_FOLDER}'")

if __name__ == "__main__":
    ordina_file()
