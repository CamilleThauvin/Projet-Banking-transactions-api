# Projet-Banking-transactions-api
MBA2 Python Project - Banking Transactions API with FastAPI

# 🏦 Banking Transactions API

API performante capable de traiter un dataset de +6 millions de transactions (1,17 Go).

## 🚀 Installation et Lancement
1. Installer les dépendances : `pip install -r requirements.txt`
2. Lancer le serveur : `python3 -m uvicorn banking_api.main:app --reload`
3. Accéder à la documentation : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 📌 Routes principales
- **Route 1** : `/api/transactions` (Pagination optimisée)
- **Route 9** : `/api/transactions/stats` (Compte des 6 362 620 lignes en < 500ms)