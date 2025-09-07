from flask import Blueprint, jsonify, current_app
from datetime import datetime

# Création du blueprint pour les routes de santé
health_bp = Blueprint('health', __name__, url_prefix='/health')

@health_bp.route('/check', methods=['GET'])
def health_check():
    """Endpoint de vérification de santé de l'API avec rate limiting"""
    
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Navion API",
        "version": "1.0.0",
        "rate_limit_info": "50 requests per minute for health checks"
    })

@health_bp.route('/', methods=['GET'])
def health_status():
    """Endpoint simple de statut"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })
