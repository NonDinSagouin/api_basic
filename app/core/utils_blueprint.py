from flask import Blueprint, jsonify

def create_utils_blueprint(redis_client):
    """Crée le blueprint pour les routes utilitaires"""
    utils_bp = Blueprint('utils', __name__)
    
    @utils_bp.route('/redis-test', methods=['GET'])
    def redis_test():
        try:
            keys = redis_client.keys()
            all_vars = {
                key.decode('utf-8'): redis_client.get(key).decode('utf-8') 
                for key in keys
            }
            return jsonify({"redis_test": all_vars}), 200
        except Exception as e:
            utils_bp.logger.error(f"Redis test failed: {e}")
            return jsonify({"error": f"Redis connection failed: {e}"}), 500
    
    @utils_bp.after_request
    def set_secure_headers(response):
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'deny'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response
    
    return utils_bp