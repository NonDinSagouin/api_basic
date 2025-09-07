import os
import logging

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

from config.RateLimit import RateLimit

from blueprints.health import health_bp
from blueprints.users import users_bp

ERROR = "Error !"

app = Flask(__name__)
CORS(app)  # Permet les requêtes cross-origin
load_dotenv()

# -------------------- Configuration du logging --------------------
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.FileHandler("logs/server.log"), logging.StreamHandler()],
    encoding = "UTF-8"
)

logger = logging.getLogger(__name__)
app.logger.info('Server launch!')

# -------------------- Configuration du rate limiting --------------------
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[RateLimit.STRICT],
    storage_uri="memory://",
    headers_enabled=True,
)
limiter.init_app(app)

# -------------------- Enregistrement des blueprints --------------------
app.register_blueprint(health_bp)
app.register_blueprint(users_bp)

# Route de base
@app.route('/')
@limiter.limit(RateLimit.STRICT)  # Limite très stricte pour test
def home():
    logger.info(f"Request from {get_remote_address()} to /")
    
    return jsonify({
        "message": "Bienvenue sur l'API Navion",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health/",
            "health_check": "/health/check",
            "users": "/users/get",
        },
        "rate_limiting": {
            "enabled": True,
        }
    })

@app.after_request
def set_secure_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'deny'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"msg": '404 Not Found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"msg": '500 Internal Server Error'}), 500

@app.errorhandler(Exception)
def unhandled_exception(error):
    app.logger.error('Unhandled Exception: %s', (error))
    return jsonify({"msg": '500 Internal Server Error'}), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({"msg": '429 Too Many Requests'}), 429

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)