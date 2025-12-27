@echo off
REM Script pour lancer l'API Banking Transactions

REM Activer l'environnement virtuel
call venv\Scripts\activate.bat

REM Installer les dépendances si nécessaire
pip install -r requirements.txt --quiet

REM Lancer l'API
echo Démarrage de l'API Banking Transactions...
uvicorn banking_api.main:app --reload

