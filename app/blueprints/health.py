from config.Config import Config
from flask import Blueprint, jsonify, current_app
from datetime import datetime

# Création du blueprint pour les routes de santé
health_bp = Blueprint('health', __name__, url_prefix="/health")

@health_bp.route('/check', methods=['GET'])
def health_check():
    """Endpoint de vérification de santé de l'API avec rate limiting"""
    
    return jsonify({
        "status": "healthy",
        "timestamp": Config.LAST_UPDATE,
        "service": Config.APP_NAME,
        "version": Config.APP_VERSION,
    })