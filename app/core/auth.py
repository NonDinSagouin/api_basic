from flask import jsonify, request
from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token

from core.limiter import limiter
from config import params, rateLimit

# Création du blueprint pour les routes d'authentification
auth_bp = Blueprint('auth', __name__, url_prefix=f"{params.API_PREFIX}/auth")

@auth_bp.route('', methods=['GET'])
@limiter.limit(rateLimit.STRICT)
def authentification():
    """ Endpoint d'authentification pour obtenir un token JWT """
    if not request.is_json:
        return jsonify({"msg": "Content-Type must be application/json"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Missing username or password parameter"}), 400

    if not password == params.SECRET_KEY or not username == "admin":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token}), 200
