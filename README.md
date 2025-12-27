# Banking Transactions API

API FastAPI pour exposer des transactions bancaires fictives à partir d'un CSV.

## Installation

### Prérequis

- Python 3.12+
- pip

### Étapes d'installation

1. Cloner le repository (ou naviguer vers le dossier du projet)

2. Créer un environnement virtuel :
```bash
python -m venv venv
```

3. Activer l'environnement virtuel :
   - Sur Windows : `venv\Scripts\activate`
   - Sur Linux/Mac : `source venv/bin/activate`

4. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Configuration

### Variables d'environnement

Le projet utilise des variables d'environnement pour la configuration :

- `CSV_PATH` : Chemin vers le fichier CSV (défaut : `data/cards_data.csv`)
- `APP_ENV` : Environnement d'exécution (`dev` ou `prod`, défaut : `dev`)

Vous pouvez créer un fichier `.env` à la racine du projet :

```env
CSV_PATH=data/cards_data.csv
APP_ENV=dev
```

## Lancement

### Méthode 1 : Script automatique (recommandé)

**Windows (CMD ou PowerShell) :**
```bash
run.bat
```

**Git Bash / Linux / Mac :**
```bash
./run.sh
```

Le script active automatiquement l'environnement virtuel, installe les dépendances si nécessaire, et lance l'API.

### Méthode 2 : Démarrage manuel

1. Activer l'environnement virtuel :
   - Windows (CMD) : `venv\Scripts\activate`
   - Windows (Git Bash) : `source venv/Scripts/activate`
   - Linux/Mac : `source venv/bin/activate`

2. Lancer le serveur :
```bash
uvicorn banking_api.main:app --reload
```

### Méthode 3 : Sans environnement virtuel (non recommandé)

Si vous préférez installer les dépendances globalement (non recommandé) :
```bash
pip install -r requirements.txt
uvicorn banking_api.main:app --reload
```

L'API sera accessible à l'adresse : `http://localhost:8000`

### Documentation interactive

- Swagger UI : `http://localhost:8000/docs`
- ReDoc : `http://localhost:8000/redoc`

## Tests

### Tests Pytest

Exécuter tous les tests pytest :

```bash
pytest
```

Avec couverture de code :

```bash
pytest --cov=banking_api --cov-report=html
```

### Tests Unittest

Exécuter les tests unittest :

```bash
python -m unittest tests.test_unittest
```

Ou avec pytest :

```bash
pytest tests/test_unittest.py
```

## Structure du projet

```
banking_api/
├── main.py                    # Point d'entrée FastAPI
├── core/
│   └── config.py             # Configuration
├── models/
│   └── schemas.py            # Modèles Pydantic
├── routes/
│   ├── transactions.py       # Routes transactions (8 endpoints)
│   ├── stats.py              # Routes statistiques (4 endpoints)
│   ├── fraud.py              # Routes fraude (3 endpoints)
│   ├── customers.py          # Routes clients (3 endpoints)
│   └── system.py             # Routes système (2 endpoints)
└── services/
    ├── data_loader.py        # Chargement CSV
    ├── transactions_service.py
    ├── stats_service.py
    ├── fraud_detection_service.py
    ├── customer_service.py
    └── system_service.py

tests/
├── test_routes.py            # Tests pytest par endpoint
└── test_unittest.py           # Tests unittest scénarios globaux
```

## Endpoints API

### Transactions (8 endpoints)

- `GET /api/transactions` - Liste paginée avec filtres
- `GET /api/transactions/{id}` - Détail d'une transaction
- `POST /api/transactions/search` - Recherche de transactions
- `GET /api/transactions/types` - Types de transactions disponibles
- `GET /api/transactions/recent` - Transactions récentes
- `DELETE /api/transactions/{id}` - Suppression fictive
- `GET /api/transactions/by-customer/{customer_id}` - Transactions d'un client
- `GET /api/transactions/to-customer/{customer_id}` - Transactions vers un client

### Statistiques (4 endpoints)

- `GET /api/stats/overview` - Vue d'ensemble
- `GET /api/stats/amount-distribution` - Distribution par montants
- `GET /api/stats/by-type` - Statistiques par type
- `GET /api/stats/daily` - Statistiques quotidiennes

### Fraude (3 endpoints)

- `GET /api/fraud/summary` - Résumé des fraudes
- `GET /api/fraud/by-type` - Fraudes par type
- `POST /api/fraud/predict` - Prédiction de fraude

### Clients (3 endpoints)

- `GET /api/customers` - Liste des clients
- `GET /api/customers/{customer_id}` - Détail d'un client
- `GET /api/customers/top` - Top clients

### Système (2 endpoints)

- `GET /api/system/health` - Santé du système
- `GET /api/system/metadata` - Métadonnées

**Total : 20 endpoints**

## Notes importantes

- Les données sont chargées en mémoire depuis le CSV au démarrage
- Les suppressions de transactions sont fictives (marquage en mémoire)
- Le fichier CSV n'est pas versionné (voir `.gitignore`)
- Le dossier `data/` n'est pas versionné
