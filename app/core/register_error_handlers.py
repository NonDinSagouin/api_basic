from flask import jsonify
from config import params

def register_error_handlers(app):
    """Enregistre tous les gestionnaires d'erreurs"""
    
    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({"msg": params.ERROR_MESSAGES['400']}), 400

    @app.errorhandler(401)
    def unauthorized_error(error):
        return jsonify({"msg": params.ERROR_MESSAGES['401']}), 401

    @app.errorhandler(403)
    def forbidden_error(error):
        return jsonify({"msg": params.ERROR_MESSAGES['403']}), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"msg": params.ERROR_MESSAGES['404']}), 404

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({"msg": params.ERROR_MESSAGES['429']}), 429

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"msg": params.ERROR_MESSAGES['500']}), 500

    @app.errorhandler(Exception)
    def unhandled_exception(error):
        app.logger.error('Unhandled Exception: %s', error)
        return jsonify({"msg": params.ERROR_MESSAGES['500']}), 500