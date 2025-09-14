import os
import logging
import redis

from datetime import timedelta
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required

from core import limiter, health_bp, auth_bp
from config import params
from blueprints import *

ERROR = "Error !"

app = Flask(__name__)
CORS(app)  # Permet les requêtes cross-origin

# -------------------- Instance Redis --------------------
r = redis.Redis(host=params.REDIS_HOST, port=params.REDIS_PORT, db=0)

# -------------------- Configuration du logging --------------------
os.makedirs(params.LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.FileHandler(params.LOG_FILE), logging.StreamHandler()],
    encoding = "UTF-8"
)

logger = logging.getLogger(__name__)
app.logger.info('Server launch!')


# -------------------- Configuration de l'authentification JWT --------------------
app.config['SECRET_KEY'] = params.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=params.JWT_ACCESS_TOKEN_EXPIRES)
    
jwt = JWTManager(app)

def init_jwt(app):
    
    @jwt.token_in_blocklist_loader
    def check_if_token_is_blocked(_, jwt_payload):
        """
        Vérifie si le token a encore des utilisations disponibles
        """
        try:
            jti = jwt_payload["jti"]
            key = f"token_use:{jti}"

            if not r.exists(key):
                logger.warning(f"Token {jti} not found in Redis")
                return True

            # Récupère le compteur actuel
            current_uses = int(r.get(key))
            
            # Si déjà utilisé, bloquer
            if current_uses <= 0:
                r.delete(key)
                logger.info(f"Token {jti} already used and removed")
                return True
            
            # Décrémente le compteur pour marquer l'utilisation
            remaining = r.decr(key)
            logger.debug(f"Token {jti} used, {remaining} uses remaining")

            # Si c'était la dernière utilisation, nettoyer
            if remaining <= 0:
                r.delete(key)
                logger.info(f"Token {jti} exhausted and removed")
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking token blocklist: {e}")
            return True  # Sécurité : bloquer en cas d'erreur

init_jwt(app)

# -------------------- Enregistrement des blueprints --------------------
# core
app.register_blueprint(health_bp)
app.register_blueprint(auth_bp)
# blueprints
app.register_blueprint(test_bp)

@app.route('/redis-test')
def redis_test():
    try:
        keys = r.keys()
        all_vars = {key.decode('utf-8'): r.get(key).decode('utf-8') for key in keys}
        return jsonify({"redis_test": all_vars}), 200
    except Exception as e:
        app.logger.error(f"Redis test failed: {e}")
        return jsonify({"error": f"Redis connection failed: {e}"}), 500

@app.after_request
def set_secure_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'deny'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.errorhandler(400) # Bad Request
def bad_request_error(error):
    return jsonify({"msg": params.ERROR_MESSAGES['400']}), 400

@app.errorhandler(401) # Unauthorized
def unauthorized_error(error):
    return jsonify({"msg": params.ERROR_MESSAGES['401']}), 401

@app.errorhandler(403) # Forbidden
def forbidden_error(error):
    return jsonify({"msg": params.ERROR_MESSAGES['403']}), 403

@app.errorhandler(404) # Not Found
def not_found_error(error):
    return jsonify({"msg": params.ERROR_MESSAGES['404']}), 404

@app.errorhandler(429) # Too Many Requests
def ratelimit_handler(e):
    return jsonify({"msg": params.ERROR_MESSAGES['429']}), 429

@app.errorhandler(500) # Internal Server Error
def internal_error(error):
    return jsonify({"msg": params.ERROR_MESSAGES['500']}), 500

@app.errorhandler(Exception) # Unhandled Exception
def unhandled_exception(error):
    app.logger.error('Unhandled Exception: %s', (error))
    return jsonify({"msg": params.ERROR_MESSAGES['500']}), 500

if __name__ == '__main__':
    app.run(host=params.HOST, port=params.PORT, debug=params.DEBUG)