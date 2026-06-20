@echo off
echo ==================================================
echo 1. SCARICAMENTO ALLEGATI DA EMAIL
echo ==================================================
python scarica_allegati.py

echo.
echo ==================================================
echo 2. SMISTAMENTO AUTOMATICO DOCUMENTI
echo ==================================================
python organizza_documenti.py

echo.
echo ==================================================
echo 3. CARICAMENTO AUTOMATICO SU GITHUB
echo ==================================================
git add .
git commit -m "Aggiornamento automatico commessa"
git push origin main

echo.
echo Operazione completata con successo!
pause
