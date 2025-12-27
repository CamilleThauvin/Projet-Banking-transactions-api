# Guide de Collaboration - Projet Banking Transactions API

## Vue d'ensemble

Ce projet est divisé en **4 parties** pour 4 personnes. Chaque personne travaille sur une section spécifique du projet.

---

## Répartition du travail

### **Personne 1 : Transactions** (8 endpoints)
- Fichiers à modifier : `banking_api/routes/transactions.py` et `banking_api/services/transactions_service.py`
- Responsabilité : Tous les endpoints liés aux transactions

### **Personne 2 : Statistiques** (4 endpoints)
- Fichiers à modifier : `banking_api/routes/stats.py` et `banking_api/services/stats_service.py`
- Responsabilité : Tous les endpoints de statistiques

### **Personne 3 : Fraude et Clients** (6 endpoints)
- Fichiers à modifier : 
  - `banking_api/routes/fraud.py` et `banking_api/services/fraud_detection_service.py` (3 endpoints)
  - `banking_api/routes/customers.py` et `banking_api/services/customer_service.py` (3 endpoints)
- Responsabilité : Détection de fraude et gestion des clients

### **Personne 4 : Système et Tests** (2 endpoints + tests)
- Fichiers à modifier : 
  - `banking_api/routes/system.py` et `banking_api/services/system_service.py` (2 endpoints)
  - `tests/test_routes.py` et `tests/test_unittest.py` (tous les tests)
- Responsabilité : Endpoints système et écriture des tests

---

## Étapes pour démarrer

### **Étape 1 : Cloner le projet (Tout le monde)**

1. Ouvrir Git Bash ou un terminal
2. Aller dans le dossier où vous voulez travailler (ex: `cd Desktop`)
3. Cloner le projet :
   ```bash
   git clone [URL_DU_PROJET]
   cd Projet-Banking-transactions-api
   ```

### **Étape 2 : Installer les dépendances (Tout le monde)**

1. Créer un environnement virtuel :
   ```bash
   python -m venv venv
   ```

2. Activer l'environnement virtuel :
   - **Windows (Git Bash)** : `source venv/Scripts/activate`
   - **Windows (CMD)** : `venv\Scripts\activate`
   - **Mac/Linux** : `source venv/bin/activate`

3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

### **Étape 3 : Tester que tout fonctionne (Tout le monde)**

1. Lancer l'API :
   ```bash
   uvicorn banking_api.main:app --reload
   ```

2. Ouvrir dans le navigateur : http://localhost:8000/docs

3. Vérifier que vous voyez la documentation Swagger

---

## Instructions par personne

### **PERSONNE 1 : Transactions**

#### Votre mission
Implémenter les 8 endpoints de transactions dans les fichiers :
- `banking_api/services/transactions_service.py` (logique métier)
- `banking_api/routes/transactions.py` (routes API)

#### Endpoints à créer :
1. `GET /api/transactions` - Liste avec pagination et filtres
2. `GET /api/transactions/{id}` - Détail d'une transaction
3. `POST /api/transactions/search` - Recherche
4. `GET /api/transactions/types` - Types disponibles
5. `GET /api/transactions/recent` - Transactions récentes
6. `DELETE /api/transactions/{id}` - Suppression
7. `GET /api/transactions/by-customer/{customer_id}` - Par client émetteur
8. `GET /api/transactions/to-customer/{customer_id}` - Par client destinataire

#### Étapes de travail :

1. **Créer une branche Git** :
   ```bash
   git checkout -b feature/transactions
   ```

2. **Ouvrir les fichiers** :
   - `banking_api/services/transactions_service.py`
   - `banking_api/routes/transactions.py`

3. **Comprendre la structure** :
   - Les **services** contiennent la logique métier (traitement des données)
   - Les **routes** exposent les endpoints API (ce que l'utilisateur appelle)

4. **Implémenter les fonctions** :
   - Commencer par les fonctions dans `transactions_service.py`
   - Utiliser `get_transactions_df()` pour obtenir les données
   - Utiliser `get_deleted_ids()` pour exclure les supprimés
   - Convertir les données pandas en modèles Pydantic

5. **Créer les routes** :
   - Dans `transactions.py`, créer les endpoints avec `@router.get()`, `@router.post()`, etc.
   - Appeler les fonctions du service
   - Gérer les erreurs (404 si non trouvé)

6. **Tester** :
   - Lancer l'API : `uvicorn banking_api.main:app --reload`
   - Tester chaque endpoint dans http://localhost:8000/docs

7. **Sauvegarder** :
   ```bash
   git add banking_api/services/transactions_service.py banking_api/routes/transactions.py
   git commit -m "Ajout des endpoints transactions"
   git push origin feature/transactions
   ```

---

###  **PERSONNE 2 : Statistiques**

#### Votre mission
Implémenter les 4 endpoints de statistiques dans :
- `banking_api/services/stats_service.py` (logique métier)
- `banking_api/routes/stats.py` (routes API)

#### Endpoints à créer :
1. `GET /api/stats/overview` - Vue d'ensemble
2. `GET /api/stats/amount-distribution` - Distribution par montants
3. `GET /api/stats/by-type` - Par type de transaction
4. `GET /api/stats/daily` - Statistiques quotidiennes

#### Étapes de travail :

1. **Créer une branche Git** :
   ```bash
   git checkout -b feature/stats
   ```

2. **Ouvrir les fichiers** :
   - `banking_api/services/stats_service.py`
   - `banking_api/routes/stats.py`

3. **Implémenter les fonctions** :
   - `get_overview()` : Calculer total, moyenne, min, max, nombre de clients
   - `get_amount_distribution()` : Grouper par tranches (0-100, 100-500, etc.)
   - `get_stats_by_type()` : Grouper par type et calculer les stats
   - `get_daily_stats()` : Grouper par date et calculer les stats

4. **Utiliser pandas** :
   - `df.groupby()` pour grouper
   - `df.agg()` pour calculer plusieurs stats
   - `df["column"].sum()`, `.mean()`, `.min()`, `.max()` pour les calculs

5. **Créer les routes** :
   - Routes simples avec `@router.get()`
   - Appeler les fonctions du service
   - Retourner les résultats

6. **Tester** :
   - Lancer l'API et tester dans http://localhost:8000/docs

7. **Sauvegarder** :
   ```bash
   git add banking_api/services/stats_service.py banking_api/routes/stats.py
   git commit -m "Ajout des endpoints statistiques"
   git push origin feature/stats
   ```

---

### **PERSONNE 3 : Fraude et Clients**

#### Votre mission
Implémenter 6 endpoints :
- **Fraude** : `banking_api/services/fraud_detection_service.py` et `banking_api/routes/fraud.py`
- **Clients** : `banking_api/services/customer_service.py` et `banking_api/routes/customers.py`

#### Endpoints à créer :

**Fraude (3 endpoints)** :
1. `GET /api/fraud/summary` - Résumé des fraudes
2. `GET /api/fraud/by-type` - Fraudes par type
3. `POST /api/fraud/predict` - Prédiction de fraude

**Clients (3 endpoints)** :
1. `GET /api/customers` - Liste des clients
2. `GET /api/customers/{customer_id}` - Détail d'un client
3. `GET /api/customers/top` - Top clients

#### Étapes de travail :

1. **Créer une branche Git** :
   ```bash
   git checkout -b feature/fraud-customers
   ```

2. **Commencer par les Clients** :
   - Ouvrir `customer_service.py` et `customers.py`
   - `get_customers()` : Grouper par `client_id` et calculer les stats
   - `get_customer_by_id()` : Filtrer par ID
   - `get_top_customers()` : Trier et prendre les N premiers

3. **Ensuite la Fraude** :
   - Ouvrir `fraud_detection_service.py` et `fraud.py`
   - Créer des heuristiques simples :
     * Montant très élevé (> 95ème percentile)
     * Fréquence élevée de transactions
     * Transactions suspectes par type
   - `get_fraud_summary()` : Compter les transactions suspectes
   - `predict_fraud()` : Évaluer une transaction

4. **Tester chaque partie** :
   - Tester les endpoints clients
   - Tester les endpoints fraude

5. **Sauvegarder** :
   ```bash
   git add banking_api/services/customer_service.py banking_api/routes/customers.py
   git add banking_api/services/fraud_detection_service.py banking_api/routes/fraud.py
   git commit -m "Ajout des endpoints fraude et clients"
   git push origin feature/fraud-customers
   ```

---

### **PERSONNE 4 : Système et Tests**

#### Votre mission
- Implémenter les 2 endpoints système
- Écrire tous les tests pour tous les endpoints

#### Endpoints système à créer :
1. `GET /api/system/health` - Santé du système
2. `GET /api/system/metadata` - Métadonnées

#### Étapes de travail :

1. **Créer une branche Git** :
   ```bash
   git checkout -b feature/system-tests
   ```

2. **Implémenter les endpoints système** :
   - Ouvrir `system_service.py` et `system.py`
   - `get_health()` : Vérifier si les données sont chargées, retourner le statut
   - `get_metadata()` : Retourner version, environnement, nombre de transactions, etc.

3. **Écrire les tests** :
   - Ouvrir `tests/test_routes.py`
   - Pour chaque endpoint, écrire au moins 1 test :
     ```python
     def test_get_transactions():
         response = client.get("/api/transactions")
         assert response.status_code == 200
         data = response.json()
         assert "items" in data
     ```
   - Tester les cas de succès (200)
   - Tester les cas d'erreur (404, 422)

4. **Tests unittest** :
   - Ouvrir `tests/test_unittest.py`
   - Écrire des scénarios complets :
     * Workflow complet (get, search, delete)
     * Vérification de cohérence des données
     * Tests de pagination

5. **Exécuter les tests** :
   ```bash
   pytest
   ```
   Vérifier que tous les tests passent

6. **Sauvegarder** :
   ```bash
   git add banking_api/services/system_service.py banking_api/routes/system.py
   git add tests/
   git commit -m "Ajout endpoints système et tests"
   git push origin feature/system-tests
   ```

---

## Comment fusionner le travail (Quand tout est terminé)

### Option 1 : Une personne fusionne tout (le chef du groupe)

1. **Créer une branche de fusion** :
   ```bash
   git checkout main
   git pull origin main
   git checkout -b merge-all-features
   ```

2. **Fusionner chaque branche** :
   ```bash
   git merge feature/transactions
   git merge feature/stats
   git merge feature/fraud-customers
   git merge feature/system-tests
   ```

3. **Résoudre les conflits** (si il y en a) :
   - Ouvrir les fichiers en conflit
   - Choisir quelle version garder
   - Sauvegarder

4. **Tester que tout fonctionne** :
   ```bash
   uvicorn banking_api.main:app --reload
   pytest
   ```

5. **Pousser sur main** :
   ```bash
   git push origin merge-all-features
   ```

### Option 2 : Fusionner une par une 

Le chef d’équipe valide les merge requests afin de protéger la branche principale et d’éviter toute régression du projet.
Une seule personne est responsable de la validation et de la fusion des merge requests.

---

## Ressources utiles

### Documentation FastAPI
- https://fastapi.tiangolo.com/
- Documentation automatique : http://localhost:8000/docs

### Commandes Git essentielles

```bash
# Voir l'état des fichiers
git status

# Ajouter des fichiers
git add nom_du_fichier.py

# Sauvegarder (commit)
git commit -m "Description de ce que vous avez fait"

# Envoyer sur le serveur
git push origin nom_de_la_branche

# Récupérer les dernières modifications
git pull origin main

# Changer de branche
git checkout nom_de_la_branche

# Créer une nouvelle branche
git checkout -b nom_de_la_branche
```

### Structure des fichiers

```
banking_api/
├── services/     → Logique métier (traitement des données)
├── routes/       → Endpoints API (ce que l'utilisateur appelle)
├── models/       → Modèles de données (déjà créés)
└── core/         → Configuration (déjà créé)
```

---

## Conseils importants

1. **Toujours tester avant de sauvegarder** : Lancer l'API et vérifier que ça fonctionne
2. **Faire des commits réguliers** : Sauvegarder souvent votre travail
3. **Communiquer** : Si vous bloquez, demandez de l'aide aux autres
4. **Respecter la structure** : Ne pas modifier les fichiers des autres sans demander
5. **Tester les endpoints** : Utiliser http://localhost:8000/docs pour tester

---

## En cas de problème

### L'API ne démarre pas
- Vérifier que l'environnement virtuel est activé
- Vérifier que les dépendances sont installées : `pip install -r requirements.txt`

### Erreur d'import
- Vérifier que vous êtes dans le bon dossier
- Vérifier que tous les fichiers `__init__.py` existent

### Conflits Git
- Ne pas paniquer
- Ouvrir le fichier en conflit
- Choisir quelle version garder (ou combiner les deux)
- Sauvegarder et faire `git add` puis `git commit`

---

## Checklist finale (avant de rendre)

- [ ] Tous les 20 endpoints fonctionnent
- [ ] Tous les tests passent (`pytest`)
- [ ] L'API démarre sans erreur
- [ ] La documentation Swagger est accessible
- [ ] Le code est sauvegardé sur Git
- [ ] Le README est à jour

---

**Bon courage !**

