import logging
from flask_jwt_extended import JWTManager

logger = logging.getLogger(__name__)

def setup_jwt(app, redis_client):
    """Configuration du JWT avec blocklist Redis"""
    jwt = JWTManager(app)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_is_blocked(_, jwt_payload):
        """Vérifie si le token a encore des utilisations disponibles"""
        try:
            jti = jwt_payload["jti"]
            key = f"token_use:{jti}"

            if not redis_client.exists(key):
                logger.warning(f"Token {jti} not found in Redis")
                return True

            current_uses = int(redis_client.get(key))
            
            if current_uses <= 0:
                redis_client.delete(key)
                logger.info(f"Token {jti} already used and removed")
                return True
            
            remaining = redis_client.decr(key)
            logger.debug(f"Token {jti} used, {remaining} uses remaining")

            if remaining <= 0:
                redis_client.delete(key)
                logger.info(f"Token {jti} exhausted and removed")
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking token blocklist: {e}")
            return True
    
    return jwt