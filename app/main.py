import core
import blueprints

from config import params

def create_application():
    """Fonction principale pour créer et configurer l'application"""
    # Configuration de base
    app = core.create_app()
    logger = core.setup_logging()
    redis_client = core.create_redis_client()
    
    logger.info('Server launch!')
    
    # Configuration JWT
    core.setup_jwt(app, redis_client)
    
    # Gestionnaires d'erreurs
    core.register_error_handlers(app)
    
    # Enregistrement des blueprints core
    app.register_blueprint(core.create_auth_blueprint(redis_client), url_prefix=f"{params.API_PREFIX}/auth")
    app.register_blueprint(core.create_utils_blueprint(redis_client), url_prefix=f"{params.API_PREFIX}/utils")
    app.register_blueprint(core.create_health_blueprint(), url_prefix=f"/health")

    # Enregistrement des blueprints d'application
    app.register_blueprint(blueprints.create_basic_endpoint(), url_prefix=f"{params.API_PREFIX}/basic")
    
    return app

# Initialisation de l'application
app = create_application()

if __name__ == '__main__':
    app = create_application()
    app.run(host=params.HOST, port=params.PORT, debug=params.DEBUG)