# Flask API pour la Génération de Factures

Cette API Flask expose les fonctionnalités de génération de factures via des endpoints REST.

## 🚀 Démarrage rapide

### 1. Installer les dépendances
```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Installer Flask
pip install flask
```

### 2. Démarrer l'application
```bash
# Option 1: Script automatique
./start_flask.sh

# Option 2: Manuel
export FLASK_ENV=development
export FLASK_DEBUG=1
python3 app.py
```

L'application sera accessible sur `http://localhost:5000`

## 📋 Endpoints disponibles

### Health Check
- **GET** `/health`
- Vérifie l'état de l'API et du générateur de factures

### Génération de factures

#### Générer une facture unique
- **POST** `/api/factures/generate`
- Génère un PDF pour une facture spécifique

**Payload JSON:**
```json
{
    "facture_id": "123",
    "client": {
        "first_name": "John",
        "last_name": "Doe",
        "location": "Montreal"
    },
    "items": [
        {
            "prix_unitaire": 25.0,
            "quantite": 2,
            "frais": 5.0
        }
    ],
    "date_emission": "2025-08-23T12:00:00",
    "date_validite": "2025-08-31T12:00:00",
    "status": "A_PAYER"
}
```

**Réponse:** Fichier PDF téléchargeable

#### Génération en lot
- **POST** `/api/factures/generate-batch`
- Traite toutes les factures disponibles selon le statut

**Payload JSON (optionnel):**
```json
{
    "filter_status": "A_PAYER"
}
```

### Consultation des données

#### Statut des factures
- **GET** `/api/factures/status`
- Retourne la liste de toutes les factures avec leur statut

#### Détails d'une facture
- **GET** `/api/factures/<facture_id>`
- Retourne les détails complets d'une facture spécifique

#### Statistiques
- **GET** `/api/statistics`
- Retourne des statistiques globales sur les factures

## 🧪 Tests

### Tester l'API
```bash
# Démarrer l'application Flask dans un terminal
./start_flask.sh

# Dans un autre terminal, lancer les tests
python3 test_flask_api.py
```

### Exemple avec curl
```bash
# Health check
curl http://localhost:5000/health

# Générer une facture
curl -X POST http://localhost:5000/api/factures/generate \
  -H "Content-Type: application/json" \
  -d '{
    "facture_id": "TEST-001",
    "client": {
      "first_name": "Test Client",
      "last_name": "Example",
      "location": "Montreal, QC"
    },
    "items": [
      {
        "prix_unitaire": 25.0,
        "quantite": 2,
        "frais": 5.0
      }
    ],
    "date_emission": "2025-08-23T12:00:00",
    "date_validite": "2025-09-22T12:00:00",
    "status": "A_PAYER"
  }' \
  --output facture_test.pdf
```

## 🔧 Configuration

L'API utilise le fichier `config.json` existant pour se connecter aux services Dropcolis et Directus.

### Variables d'environnement
- `PORT`: Port d'écoute (défaut: 5000)
- `FLASK_ENV`: Environnement Flask (development/production)
- `FLASK_DEBUG`: Mode debug (1/0)

## 📊 Réponses d'API

### Format standard
```json
{
    "status": "success",
    "data": {...},
    "timestamp": "2025-08-23T17:54:18.738"
}
```

### Codes d'erreur
- `200`: Succès
- `400`: Données invalides
- `404`: Endpoint non trouvé
- `500`: Erreur interne du serveur

## 🚨 Gestion des erreurs

L'API inclut une gestion complète des erreurs :
- Validation des données d'entrée
- Gestion des erreurs de génération PDF
- Gestion des erreurs de connexion API
- Logs détaillés pour le débogage

## 🔍 Monitoring

### Logs
L'API génère des logs détaillés pour :
- Initialisation du générateur
- Génération de factures
- Erreurs et exceptions
- Statistiques de performance

### Métriques
- Nombre de factures traitées
- Temps de génération
- Taux de succès/échec
- Utilisation des ressources

## 🚀 Déploiement

### Production
```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (optionnel)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python3", "app.py"]
```

## 📝 Notes importantes

1. **Sécurité**: L'API n'inclut pas d'authentification par défaut
2. **Performance**: Les PDF sont générés de manière synchrone
3. **Stockage**: Les fichiers temporaires sont automatiquement nettoyés
4. **Concurrence**: L'API peut gérer plusieurs requêtes simultanées

## 🤝 Support

Pour toute question ou problème :
1. Vérifiez les logs de l'application
2. Testez avec l'endpoint `/health`
3. Consultez la documentation des tests
4. Vérifiez la configuration dans `config.json`
