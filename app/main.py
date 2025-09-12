import os
import logging

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config.RateLimit import RateLimit

from blueprints.health import health_bp
from blueprints.users import users_bp

from config.Config import Config

ERROR = "Error !"

app = Flask(__name__)
CORS(app)  # Permet les requêtes cross-origin

# Configuration de l'application
app.config.from_object(Config)

# -------------------- Configuration du logging --------------------
os.makedirs(Config.LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.FileHandler(Config.LOG_FILE), logging.StreamHandler()],
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

@app.route("/", methods=["GET"])
def index():
    return jsonify({"msg": Config.HOST}), 200

@app.after_request
def set_secure_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'deny'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({"msg": Config.ERROR_MESSAGES['400']}), 400

@app.errorhandler(401)
def unauthorized_error(error):
    return jsonify({"msg": Config.ERROR_MESSAGES['401']}), 401

@app.errorhandler(403)
def forbidden_error(error):
    return jsonify({"msg": Config.ERROR_MESSAGES['403']}), 403

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"msg": Config.ERROR_MESSAGES['404']}), 404

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({"msg": Config.ERROR_MESSAGES['429']}), 429

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"msg": Config.ERROR_MESSAGES['500']}), 500

@app.errorhandler(Exception)
def unhandled_exception(error):
    app.logger.error('Unhandled Exception: %s', (error))
    return jsonify({"msg": Config.ERROR_MESSAGES['500']}), 500


if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)