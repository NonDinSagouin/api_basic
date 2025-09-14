import redis

from flask import jsonify, request
from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token, decode_token
from datetime import timedelta

from core.limiter import limiter
from config import params, rateLimit

# Création du blueprint pour les routes d'authentification
auth_bp = Blueprint('auth', __name__, url_prefix=f"{params.API_PREFIX}/auth")

# Création de l'instance Redis
r = redis.Redis(host=params.REDIS_HOST, port=params.REDIS_PORT, db=0)

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
    
    expires = timedelta(minutes=params.JWT_ACCESS_TOKEN_EXPIRES)

    # Création du token avec durée de vie explicite
    access_token = create_access_token(
        identity=username,
        expires_delta=expires
    )

    # Récupérer le JTI depuis le token décodé
    jti = decode_token(access_token)["jti"]
    
    # Stocker le JTI dans Redis avec un compteur d'utilisations
    r.setex(f"token_use:{jti}", int(expires.total_seconds()), params.TOKEN_RATE_LIMIT_PER_MINUTE)

    return jsonify({"access_token": access_token}), 200
