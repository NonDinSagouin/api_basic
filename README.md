# 🚀 API Basic
Une API REST développée avec Flask et déployée avec Docker.

## 📁 Structure du projet
```
api_basic/
├── app/                            # Code de l'application Flask
│   ├── main.py                     # Application principale Flask
│   ├── requirements.txt            # Dépendances Python
│   ├── .env                        # Variables d'environnement
│   ├── blueprints/                 # Modules de l'API
│   │   ├── __init__.py             # Initialisation des blueprints
│   │   ├── auth.py                 # Authentification
│   │   ├── health.py               # Endpoint de santé
│   │   └── users.py                # Gestion des utilisateurs
│   └── config/                     # Configuration de l'app
│       ├── auth.py                 # Configuration auth
│       └── RateLimit.py            # Limitation de taux
├── docker/                         # Configuration Docker
│   ├── docker-compose.yml          # Environnement de développement
│   ├── docker-compose.prod.yml     # Environnement de production
│   ├── api/                        # Image Docker de l'API
│   │   └── Dockerfile              # Dockerfile pour l'API
│   └── nginx/                      # Configuration Nginx
│       ├── nginx.conf              # Config avec SSL
│       └── nginx-simple.conf       # Config sans SSL
├── scripts/                        # Scripts utilitaires
│   └── setup-ssl.sh                # Configuration SSL automatique
├── Makefile                        # Commandes simplifiées
├── .gitignore                      # Fichiers ignorés par Git
└── README.md                       # Documentation du projet
```

## 📋 Commandes disponibles

```bash
make help          # Affiche toutes les commandes
make build         # Construit les images
make start         # Démarre
make stop          # Arrête les conteneurs
make restart       # Redémarre
make logs          # Affiche les logs
make status        # Statut des conteneurs
make test          # Teste l'API
make clean         # Nettoie tout
```

## 🌐 Accès à l'API

- **Local** : http://localhost
- **Production** : http://137.74.193.55

### Endpoints disponibles
- `GET /` - Page d'accueil de l'API
- `GET /health` - Vérification de l'état de santé de l'API
- `GET /api/users` - Récupération de la liste des utilisateurs
- `POST /api/users` - Création d'un nouvel utilisateur
- `PUT /api/users/<id>` - Mise à jour d'un utilisateur
- `DELETE /api/users/<id>` - Suppression d'un utilisateur

## 📚 Documentation et développement

### Structure de l'API
L'API est organisée en blueprints pour une meilleure modularité :
- **health** : Endpoints de monitoring et santé
- **users** : Gestion des utilisateurs
- **auth** : Authentification et autorisation (à venir)

### Limitation de taux
L'API inclut une limitation de taux configurée via Flask-Limiter pour prévenir les abus.

### CORS
Support CORS activé pour permettre les requêtes cross-origin depuis les applications frontend.

## 🔧 Développement

### Tests de l'API
```bash
# Tester tous les endpoints
make test

# Tester manuellement
curl http://localhost/health
curl http://localhost/api/users
```

### Logs
```bash
# Voir les logs en temps réel
make logs

# Logs d'un service spécifique
docker-compose -f docker/docker-compose.yml logs api
```

## 🛠️ Technologies utilisées

- **Backend** : Python 3.11, Flask 2.3.3
- **Middleware** : Flask-CORS 4.0.0, Flask-Limiter 3.5.0
- **Serveur WSGI** : Gunicorn 21.2.0
- **Proxy inverse** : Nginx
- **Containerisation** : Docker + Docker Compose
- **SSL** : Let's Encrypt (optionnel)
- **Configuration** : Variables d'environnement (.env)

## 🚀 Installation et démarrage

### Prérequis
- Docker et Docker Compose installés
- Make (optionnel, pour utiliser les commandes simplifiées)

### Démarrage rapide
```bash
# Cloner le repository
git clone <your-repo-url>
cd api_basic


# Construire et démarrer l'application
make build && make start

# Ou avec Docker Compose directement
docker-compose -f docker/docker-compose.yml up --build
```

### Variables d'environnement
Créez un fichier `.env` dans le dossier `app/` avec les variables suivantes :
```env
FLASK_ENV=development
FLASK_DEBUG=True
API_HOST=0.0.0.0
API_PORT=5000
```

---

## 📝 Auteur

*Développé avec ❤️ pour Navion*
