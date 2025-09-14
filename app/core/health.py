from flask import Blueprint, jsonify, current_app
from datetime import datetime

from config import params

def create_health_blueprint():
    """Crée le blueprint pour les routes de santé"""
    health_bp = Blueprint('health', __name__)
    
    @health_bp.route('/check', methods=['GET'])
    def health_check():
        """Endpoint de vérification de santé de l'API """
        
        return jsonify({
            "status": "healthy",
            "timestamp": params.TIMESTAMP(),
            "service": params.APP_NAME,
            "version": params.APP_VERSION,
            "description": params.APP_DESCRIPTION,
            "launch_time": params.LAST_UPDATE,
        })
    
    return health_bp