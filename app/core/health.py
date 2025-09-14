from flask import Blueprint, jsonify, current_app
from datetime import datetime

from config import params

# Création du blueprint pour les routes de santé
health_bp = Blueprint('health', __name__, url_prefix="/health")

@health_bp.route('/check', methods=['GET'])
def health_check():
    """Endpoint de vérification de santé de l'API avec rate limiting"""
    
    return jsonify({
        "status": "healthy",
        "timestamp": params.TIMESTAMP(),
        "service": params.APP_NAME,
        "version": params.APP_VERSION,
        "description": params.APP_DESCRIPTION,
        "launch_time": params.LAST_UPDATE,
    })