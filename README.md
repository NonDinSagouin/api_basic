# 🚀 API Basic

[![Version](https://img.shields.io/badge/Version-1.0.0-brightgreen.svg)]()
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-21.2.0-yellow.svg)](https://gunicorn.org/)
[![Redis](https://img.shields.io/badge/Redis-6.4.0-DC382D?logoColor=white)](https://redis.io/)
[![Nginx](https://img.shields.io/badge/Nginx-Proxy-brightgreen.svg)](https://nginx.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)


Une API REST développée avec Flask et déployée avec Docker.

## 🛠️ Technologies utilisées

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Make](https://img.shields.io/badge/GNU%20Make-427819.svg?style=for-the-badge&logo=gnu&logoColor=white)

![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)

- **Backend** : Python 3.11, Flask 2.3.3
- **Middleware** : Flask-CORS 4.0.0, Flask-Limiter 3.5.0
- **Cache/Database** : Redis 7
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
make dev-build && make dev-up

# Ou avec Docker Compose directement
docker-compose -f docker/docker-compose.yml up --build
```

## 🔧 Développement

### Tests de l'API
```bash

# Tester la santé de l'API, Redis et tous les conteneurs
make tests

# Tester manuellement
curl http://localhost/health/check
```

## 📁 Structure du projet
```
api_basic/
├── .git/                           # Données du repository Git
├── .gitignore                      # Fichiers ignorés par Git
├── Makefile                        # Commandes simplifiées Make
├── README.md                       # Documentation du projet
├── __pycache__/                    # Cache Python (généré automatiquement)
├── app/                            # Code de l'application Flask
│   ├── main.py                     # Application principale Flask
│   ├── requirements.txt            # Dépendances Python
│   ├── __pycache__/                # Cache Python de l'app
│   ├── blueprints/                 # Modules de l'API (blueprints)
│   │   ├── __init__.py             # Initialisation des blueprints
│   │   ├── basic_endpoint.py       # Endpoints de base et test
│   │   └── __pycache__/            # Cache Python des blueprints
│   ├── config/                     # Configuration de l'application
│   │   ├── __init__.py             # Initialisation config
│   │   ├── .env                    # Variables d'environnement
│   │   ├── params.py               # Paramètres de configuration
│   │   ├── rateLimit.py            # Configuration limitation de taux
│   │   └── __pycache__/            # Cache Python config
│   └── core/                       # Modules core de l'application
│       ├── __init__.py             # Initialisation core
│       ├── auth.py                 # Authentification et autorisation
│       ├── base.py                 # Factory et configuration Flask
│       ├── health.py               # Endpoints de santé et monitoring
│       ├── limiter.py              # Gestionnaire de limitation de taux
│       ├── register_error_handlers.py # Gestionnaire d'erreurs
│       ├── setup_jwt.py            # Configuration JWT
│       ├── utils_blueprint.py      # Utilitaires pour blueprints
│       └── __pycache__/            # Cache Python core
├── docker/                         # Configuration Docker
│   ├── docker-compose.yml          # Environnement de développement
│   ├── docker-compose.prod.yml     # Environnement de production
│   ├── api/                        # Image Docker de l'API
│   │   ├── .dockerignore           # Fichiers ignorés par Docker
│   │   └── Dockerfile              # Dockerfile pour l'API
│   └── nginx/                      # Configuration Nginx
│       ├── nginx.conf              # Config avec SSL
│       └── nginx-simple.conf       # Config sans SSL
└── scripts/                        # Scripts utilitaires
    └── setup-ssl.sh                # Configuration SSL automatique
```

## 📋 Commandes disponibles

### 🛠️ Commandes principales
```bash
make help          # Affiche l'aide avec toutes les commandes disponibles
make dev-build     # Construit l'environnement de développement
make dev-up        # Lance le développement sans rebuild
make dev-down      # Arrête l'environnement de développement
make dev-restart   # Redémarre les conteneurs de développement
```

### 🚀 Production
```bash
make prod          # Lance l'environnement de production (build + start)
make up            # Démarre les conteneurs de production
make down          # Arrête les conteneurs de production
make restart       # Redémarre les conteneurs de production
```

### 📊 Monitoring et logs
```bash
make logs          # Affiche les logs de tous les services
make logs-api      # Affiche les logs de l'API uniquement
make logs-nginx    # Affiche les logs de Nginx uniquement
make status        # Affiche le statut des conteneurs
```

### � Tests
```bash
make tests            # Exécute tous les tests 
make test-health      # Teste la santé de l'API
make test-redis       # Teste la connexion et les opérations Redis
make test-containers  # Teste le statut de tous les conteneurs
```

### �🧹 Maintenance
```bash
make clean         # Nettoie les conteneurs et images
make clean-redis   # Nettoie les données Redis
make ssl DOMAIN=exemple.com  # Configure SSL avec Let's Encrypt
```

## 🌐 Accès à l'API

- **Local** : http://localhost
- **Production** : http://137.74.193.55

### Endpoints disponibles

#### 🏥 Santé et monitoring
- `GET /health/check` - Vérification de santé de l'API avec informations détaillées
  - Retourne : statut, timestamp, nom du service, version, description, temps de lancement
  - Rate limiting : Aucun
  - Authentification : Non requise

#### 🔐 Authentification  
- `GET /api/v1/auth` - Authentification pour obtenir un token JWT
  - Body JSON requis : `{"username": "admin", "password": "secret_key"}`
  - Retourne : `{"access_token": "jwt_token"}`
  - Rate limiting : Strict
  - Authentification : Non requise (endpoint d'authentification)

#### 🧪 Endpoints de base (Authentification requise)
- `GET /api/v1/basic` - Endpoint de test protégé par JWT
  - Headers requis : `Authorization: Bearer <jwt_token>`
  - Retourne : `{"msg": "Test endpoint"}`
  - Rate limiting : Strict
  - Authentification : JWT requis

#### 🛠️ Utilitaires (Développement)
- `GET /api/v1/utils/redis-test` - Test de connexion Redis et affichage des variables stockées
  - Retourne : `{"redis_test": {...}}`
  - Rate limiting : Aucun
  - Authentification : Non requise
  - Usage : Développement et debugging

## 📝 Auteur

*Développé avec ❤️ pour Navion*
