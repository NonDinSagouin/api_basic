"""
Configuration centralisée pour l'application
Ce fichier contient toutes les constantes et paramètres configurables de l'application
"""

import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration de base pour l'application"""

    # Informations de l'application
    APP_NAME = "default_name"
    APP_DESCRIPTION = "Une API REST développée avec Flask"
    APP_VERSION = "1.0.0"
    APP_AUTHOR = "Damien Boehler"
    APP_LICENSE = "None"
    
    # URLs et endpoints
    BASE_URL = os.getenv('BASE_URL', 'http://localhost')
    API_PREFIX = '/api/v1'
    
    # Configuration Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
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
    
    # Métadonnées
    CREATION_DATE = "2025-09-12"
    LAST_UPDATE = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
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
    
    @classmethod
    def get_app_info(cls):
        """Retourne les informations de l'application sous forme de dictionnaire"""
        return {
            'name': cls.APP_NAME,
            'description': cls.APP_DESCRIPTION,
            'version': cls.APP_VERSION,
            'author': cls.APP_AUTHOR,
            'license': cls.APP_LICENSE,
            'base_url': cls.BASE_URL,
            'creation_date': cls.CREATION_DATE,
            'last_update': cls.LAST_UPDATE
        }