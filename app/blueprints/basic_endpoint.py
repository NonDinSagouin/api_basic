from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from config import rateLimit
from core import limiter

def create_basic_endpoint():
    """Crée le blueprint pour les routes de base"""
    basic_endpoint_bp = Blueprint('basic_endpoint', __name__)
    
    @basic_endpoint_bp.route('', methods=['GET'])
    @limiter.limit(rateLimit.STRICT)
    @jwt_required()
    def test_endpoint():
        """Endpoint de test de l'API"""
        return jsonify({"msg": "Test endpoint"}), 200

    return basic_endpoint_bp