from redis import Redis

from app.core.config import appconfig

# redis_client = Redis(
#     host=appconfig.REDIS_HOST,
#     port=appconfig.REDIS_PORT,
#     db=appconfig.REDIS_DB,
#     decode_responses=True,
#     socket_timeout=5,
# )

_redis_kwargs = {
    "host": appconfig.REDIS_HOST,
    "port": appconfig.REDIS_PORT,
    "db": appconfig.REDIS_DB,
    "decode_responses": True,
    "socket_timeout": 30,
    "socket_connect_timeout": 10,
    "socket_keepalive": True,
    "health_check_interval": 30,
    "retry_on_timeout": True,
}

# ElastiCache: AUTH token (only set if encryption-in-transit + auth are enabled)
if appconfig.REDIS_AUTH_TOKEN:
    _redis_kwargs["password"] = appconfig.REDIS_AUTH_TOKEN

# ElastiCache: encryption in transit
if appconfig.REDIS_SSL:
    _redis_kwargs["ssl"] = True
    _redis_kwargs["ssl_cert_reqs"] = None  # ElastiCache uses AWS-issued certs

redis_client = Redis(**_redis_kwargs)
