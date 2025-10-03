# 🚀 API Flask pour la Génération de Factures - Résumé Complet

## 📋 Vue d'ensemble

Une API Flask complète a été créée pour exposer les fonctionnalités de génération de factures via des endpoints REST. L'API permet de générer des factures individuelles, en lot, et de consulter les statistiques.

## 🏗️ Architecture

```
generate_facture/
├── app.py                 # Application Flask principale
├── start_api.py          # Script de démarrage Python
├── start_flask.sh        # Script de démarrage Shell
├── api_config.py         # Configuration de l'API
├── test_flask_api.py     # Tests complets de l'API
├── test_flask_simple.py  # Tests de configuration
├── quick_test.py         # Test rapide de tous les composants
├── FLASK_API_README.md   # Documentation détaillée
└── generate_facture.py   # Générateur de factures existant
```

## 🚀 Démarrage rapide

### 1. Vérifier l'installation
```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Tester tous les composants
python3 quick_test.py
```

### 2. Démarrer l'API
```bash
# Option 1: Script Python
python3 start_api.py

# Option 2: Script Shell
./start_flask.sh
```

L'API sera accessible sur `http://localhost:5000`

## 📡 Endpoints disponibles

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/health` | Vérification de l'état de l'API |
| `POST` | `/api/factures/generate` | Génération d'une facture unique |
| `POST` | `/api/factures/generate-batch` | Génération en lot |
| `GET` | `/api/factures/status` | Statut de toutes les factures |
| `GET` | `/api/factures/<id>` | Détails d'une facture spécifique |
| `GET` | `/api/statistics` | Statistiques globales |

## 🔧 Configuration

### Variables d'environnement
- `PORT`: Port d'écoute (défaut: 5000)
- `FLASK_DEBUG`: Mode debug (0/1)
- `API_HOST`: Hôte d'écoute (défaut: 0.0.0.0)
- `API_TIMEOUT`: Timeout des requêtes (défaut: 30s)

### Fichier de configuration
L'API utilise le fichier `config.json` existant pour :
- Connexion à l'API Dropcolis
- Connexion à Directus
- Chemin du template HTML

## 📊 Fonctionnalités

### 1. Génération de factures individuelles
- Validation des données d'entrée
- Génération de PDF avec WeasyPrint
- Retour du fichier PDF téléchargeable
- Calcul automatique des totaux (subtotal, TPS, TVQ, total TTC)

### 2. Génération en lot
- Traitement automatique de toutes les factures
- Filtrage par statut (A_PAYER, PAYEE, ANNULEE)
- Upload automatique vers Directus
- Mise à jour des montants dans la base

### 3. Consultation des données
- Statut des factures en temps réel
- Détails complets des factures
- Statistiques globales (montants, distribution des statuts)

### 4. Gestion des erreurs
- Validation des données d'entrée
- Gestion des erreurs de génération PDF
- Gestion des erreurs de connexion API
- Logs détaillés pour le débogage

## 🧪 Tests

### Test rapide
```bash
python3 quick_test.py
```

### Tests complets (nécessite l'API en cours d'exécution)
```bash
# Terminal 1: Démarrer l'API
python3 start_api.py

# Terminal 2: Lancer les tests
python3 test_flask_api.py
```

### Test manuel avec curl
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
    "date_service": "2025-09-22T12:00:00",
    "status": "A_PAYER"
  }' \
  --output facture_test.pdf
```

## 🔍 Monitoring et logs

### Logs automatiques
- Initialisation du générateur
- Génération de factures
- Erreurs et exceptions
- Statistiques de performance

### Métriques disponibles
- Nombre de factures traitées
- Temps de génération
- Taux de succès/échec
- Utilisation des ressources

## 🚨 Sécurité et performance

### Sécurité
- Validation stricte des données d'entrée
- Gestion des erreurs sans exposition d'informations sensibles
- Nettoyage automatique des fichiers temporaires

### Performance
- Génération synchrone des PDF
- Gestion efficace de la mémoire
- Nettoyage automatique des ressources

## 🚀 Déploiement

### Développement
```bash
export FLASK_DEBUG=1
export FLASK_ENV=development
python3 start_api.py
```

### Production
```bash
export FLASK_DEBUG=0
export FLASK_ENV=production
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
CMD ["python3", "start_api.py"]
```

## 📝 Modifications apportées

### 1. Template HTML
- Logo intégré en base64 pour éviter les problèmes de chemins
- Couleurs conditionnelles pour les statuts (A_PAYER, PAYEE, ANNULEE)
- Design professionnel ROPCOLIS

### 2. Générateur de factures
- Retour des totaux (pdf_path, grand_total, subtotal)
- Mise à jour automatique des montants dans Directus
- Gestion améliorée des erreurs

### 3. API Flask
- Endpoints REST complets
- Validation des données
- Gestion des erreurs
- Documentation intégrée

## 🤝 Utilisation

### 1. Démarrer l'API
```bash
python3 start_api.py
```

### 2. Tester la santé
```bash
curl http://localhost:5000/health
```

### 3. Générer une facture
Utilisez l'endpoint `/api/factures/generate` avec les données JSON appropriées

### 4. Consulter les statistiques
```bash
curl http://localhost:5000/api/statistics
```

## 🔧 Dépannage

### Problèmes courants
1. **Port déjà utilisé**: Changez la variable `PORT`
2. **Erreur de configuration**: Vérifiez `config.json`
3. **Erreur de génération PDF**: Vérifiez l'installation de WeasyPrint
4. **Erreur de connexion API**: Vérifiez les tokens et URLs dans `config.json`

### Logs et débogage
- Tous les logs sont affichés dans la console
- Utilisez `FLASK_DEBUG=1` pour plus de détails
- Vérifiez l'endpoint `/health` pour l'état du système

## 🎯 Prochaines étapes

### Améliorations possibles
1. **Authentification**: Ajouter JWT ou OAuth2
2. **Rate limiting**: Limiter le nombre de requêtes
3. **Cache**: Mettre en cache les factures fréquemment demandées
4. **Webhooks**: Notifications automatiques lors de la génération
5. **Monitoring**: Métriques Prometheus/Grafana
6. **Tests**: Couverture de tests plus complète

### Intégrations
1. **Frontend**: Interface web pour la génération
2. **Mobile**: Application mobile pour la consultation
3. **Webhooks**: Intégration avec d'autres systèmes
4. **API Gateway**: Gestion centralisée des APIs

## 📞 Support

Pour toute question ou problème :
1. Vérifiez les logs de l'application
2. Testez avec l'endpoint `/health`
3. Consultez la documentation des tests
4. Vérifiez la configuration dans `config.json`

---

**🎉 L'API Flask est maintenant prête à être utilisée !**

Démarrez-la avec `python3 start_api.py` et testez avec `python3 quick_test.py`
