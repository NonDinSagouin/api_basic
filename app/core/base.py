import os
import logging
from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import redis

from config import params

def create_app():
    """Factory pattern pour créer l'application Flask"""
    app = Flask(__name__)
    CORS(app)
    
    # Configuration JWT
    app.config['SECRET_KEY'] = params.JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=params.JWT_ACCESS_TOKEN_EXPIRES)
    
    return app

def setup_logging():
    """Configuration du système de logging"""
    os.makedirs(params.LOG_DIR, exist_ok=True)
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[
            logging.FileHandler(params.LOG_FILE),
            logging.StreamHandler()
        ],
        encoding="UTF-8"
    )
    
    return logging.getLogger(__name__)

def create_redis_client():
    """Création du client Redis"""
    return redis.Redis(
        host=params.REDIS_HOST,
        port=params.REDIS_PORT,
        password=params.REDIS_PASSWORD,
        db=0
    )