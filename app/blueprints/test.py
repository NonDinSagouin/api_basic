from config.Config import Config
from flask import Blueprint, jsonify, current_app
from datetime import datetime

# Création du blueprint pour les routes de test
test_bp = Blueprint('api_test', __name__, url_prefix=f"{Config.API_PREFIX}/test")

@test_bp.route('', methods=['GET'])
def test_endpoint():
    """Endpoint de test de l'API"""
    return jsonify({"msg": "Test endpoint"}), 200