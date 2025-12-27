#!/bin/bash
# Script pour lancer l'API Banking Transactions (Git Bash / Linux / Mac)

# Activer l'environnement virtuel
source venv/Scripts/activate 2>/dev/null || source venv/bin/activate

# Installer les dépendances si nécessaire
pip install -r requirements.txt --quiet

# Lancer l'API
echo "Démarrage de l'API Banking Transactions..."
uvicorn banking_api.main:app --reload

