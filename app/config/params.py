"""
Configuration centralisée pour l'application
Ce fichier contient toutes les constantes et paramètres configurables de l'application
"""

import os
import pytz

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Informations de l'application
APP_NAME = os.getenv('APP_NAME', "default_name")
APP_DESCRIPTION = os.getenv('APP_DESCRIPTION', "Une API REST développée avec Flask")
APP_VERSION = os.getenv('APP_VERSION', "1.0.0")
APP_AUTHOR = os.getenv('APP_AUTHOR', "Damien Boehler")
APP_TIMEZONE = os.getenv('APP_TIMEZONE', "Europe/Paris")
APP_LICENSE = "None"
    
# URLs et endpoints
BASE_URL = os.getenv('BASE_URL', 'http://localhost')
API_PREFIX = '/api/v1'

# Authentification
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key-change-in-production')
JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 60))  # en minutes
TOKEN_RATE_LIMIT_PER_MINUTE = int(os.getenv('TOKEN_RATE_LIMIT_PER_MINUTE', 100))  # Limite par token par minute

# Configuration Flask
DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
TESTING = False

# Configuration du serveur
HOST = os.getenv('API_HOST', '0.0.0.0')
PORT = int(os.getenv('API_PORT', 5000))

# Configuration CORS
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

# Configuration des logs
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
LOG_DIR = os.getenv('LOG_DIR', '../logs')
LOG_FILE = f"{LOG_DIR}/{APP_NAME}.log"

# Configuration Rate Limiting
RATE_LIMIT_STORAGE = os.getenv('RATE_LIMIT_STORAGE', 'memory://')
DEFAULT_RATE_LIMIT = os.getenv('DEFAULT_RATE_LIMIT', '100 per hour')

# Configuration Redis
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_URL = os.getenv('REDIS_URL', f'redis://{REDIS_HOST}:{REDIS_PORT}')

# Métadonnées
CREATION_DATE = "2025-09-12"
LAST_UPDATE = datetime.now(pytz.timezone(APP_TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S")
TIMESTAMP = lambda : datetime.now(pytz.timezone(APP_TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S")

# Messages d'erreur standard
ERROR_MESSAGES = {
    '400': 'Bad Request - Requête invalide',
    '401': 'Unauthorized - Non autorisé',
    '403': 'Forbidden - Accès interdit',
    '404': 'Not Found - Ressource non trouvée',
    '429': 'Too Many Requests - Trop de requêtes',
    '500': 'Internal Server Error - Erreur interne du serveur'
}

# Configuration de la base de données (pour futur usage)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///navion.db')