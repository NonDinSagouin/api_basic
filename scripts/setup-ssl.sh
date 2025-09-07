#!/bin/bash

# Script pour configurer SSL avec Let's Encrypt
# Usage: ./setup-ssl.sh your-domain.com

DOMAIN=$1

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

if [ -z "$DOMAIN" ]; then
    echo "Usage: $0 <domain>"
    echo "Example: $0 api.monsite.com"
    exit 1
fi

echo "Configuration SSL pour le domaine: $DOMAIN"

# Aller dans le répertoire du projet
cd "$PROJECT_DIR"

# Arrêter les conteneurs existants
cd docker && docker-compose -f docker-compose.prod.yml down
cd ..

# Installer certbot si nécessaire
if ! command -v certbot &> /dev/null; then
    echo "Installation de certbot..."
    sudo apt update
    sudo apt install -y certbot
fi

# Obtenir le certificat SSL
echo "Obtention du certificat SSL..."
sudo certbot certonly --standalone \
    --preferred-challenges http \
    --email your-email@example.com \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN

# Copier les certificats vers le dossier ssl
sudo cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem ./ssl/cert.pem
sudo cp /etc/letsencrypt/live/$DOMAIN/privkey.pem ./ssl/private.key
sudo chown $USER:$USER ./ssl/*.pem ./ssl/*.key

# Mettre à jour la configuration nginx
sed -i "s/137.74.193.55/$DOMAIN/g" docker/nginx/nginx.conf

echo "Configuration SSL terminée pour $DOMAIN"
echo "Vous pouvez maintenant lancer: 'make start' ou 'cd docker && docker-compose up -d'"
