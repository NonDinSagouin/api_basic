from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import config

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[config.DEFAULT_RATE_LIMIT],
    storage_uri=config.REDIS_URL,
    headers_enabled=True,
)