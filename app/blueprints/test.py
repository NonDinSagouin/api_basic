from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from config import params, rateLimit
from core import limiter

# Création du blueprint pour les routes de test
test_bp = Blueprint('api_test', __name__, url_prefix=f"{params.API_PREFIX}/test")

@test_bp.route('', methods=['GET'])
@limiter.limit(rateLimit.STRICT)
@jwt_required()
def test_endpoint():
    """Endpoint de test de l'API"""
    return jsonify({"msg": "Test endpoint"}), 200