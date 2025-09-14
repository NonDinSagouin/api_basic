import os
import logging

from datetime import timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token

from core import limiter, health_bp, auth_bp
from config import params
from blueprints import *

ERROR = "Error !"

app = Flask(__name__)
CORS(app)  # Permet les requêtes cross-origin

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

# -------------------- Configuration du rate limiting --------------------
limiter.init_app(app)

# -------------------- Configuration de l'authentification JWT --------------------
app.config['SECRET_KEY'] = params.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=params.JWT_ACCESS_TOKEN_EXPIRES)

jwt = JWTManager(app)

# -------------------- Enregistrement des blueprints --------------------
# core
app.register_blueprint(health_bp)
app.register_blueprint(auth_bp)
# blueprints
app.register_blueprint(test_bp)

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