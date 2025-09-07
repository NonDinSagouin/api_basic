# 🚀 Navion API
Une API REST développée avec Flask et déployée avec Docker.

## 📁 Structure du projet
```
navion/
├── app/                            # Code de l'application Flask
│   ├── main.py                     # Application principale
│   ├── Dockerfile                  # Image Docker de l'app
│   └── .dockerignore               # Fichiers ignorés par Docker
├── docker/                         # Configuration Docker
│   ├── docker-compose.yml          # Dev avec SSL
│   └── nginx/                      # Configuration Nginx
│       ├── nginx.conf              # Config avec SSL
│       └── nginx-simple.conf       # Config sans SSL
├── scripts/                        # Scripts utilitaires
│   └── setup-ssl.sh                # Configuration SSL automatique
├── docs/                           # Documentation
│   ├── README.md                   # Documentation de l'API
│   └── DEPLOYMENT.md               # Guide de déploiement
├── ssl/                            # Certificats SSL
├── Makefile                        # Commandes simplifiées
├── requirements.txt                # Dépendances Python
└── __pycache__/                    # Cache Python
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

### Endpoints
- `GET /` - Accueil
- `GET /health` - Santé de l'API
- `GET /api/users` - Liste des utilisateurs
- `POST /api/users` - Créer un utilisateur

## 📚 Documentation

- [Guide de l'API](docs/README.md)
- [Guide de déploiement](docs/DEPLOYMENT.md)

## 🛠️ Technologies

- **Backend** : Python 3.11, Flask 2.3.3
- **Serveur** : Gunicorn + Nginx
- **Containerisation** : Docker + Docker Compose
- **SSL** : Let's Encrypt (optionnel)

---

*Développé avec ❤️ pour des Navion*
