import os
import json
from urllib import parse

DEBUG = True
REALM = os.environ.get('REALM', 'local')

ROOT_URL = "http://localhost:4000"

PORT_NUMBER = 4000

ENABLE_CORS = False
CORS_ORIGINS = "*"

FLASK_SESSION_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", "N1BKhJLnBqLpexOZdklsfDKFJDKFadsfs9a3r324YB7B73AglRmrHMDQ9RhXz35")

BIN_TTL = 96*3600
STORAGE_BACKEND = "requestbin.storage.memory.MemoryStorage"
MAX_RAW_SIZE = int(os.environ.get('MAX_RAW_SIZE', 1024*10))
IGNORE_HEADERS = []
MAX_REQUESTS = int(os.environ.get('MAX_REQUESTS', 100))
CLEANUP_INTERVAL = 3600

# Redis configuration defaults
REDIS_URL = ""
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_DB = 9
REDIS_SSL = False
REDIS_SSL_CERT_REQS = None

REDIS_PREFIX = "requestbin"

# Function to parse SAP BTP VCAP_SERVICES for Redis
def get_redis_config_from_vcap():
    vcap_services = os.getenv('VCAP_SERVICES')
    if vcap_services:
        try:
            services = json.loads(vcap_services)
            # Look for Redis service in various possible service names
            redis_services = services.get('redis-enterprise-cloud', [])
            if not redis_services:
                redis_services = services.get('redis', [])
            if not redis_services:
                redis_services = services.get('redis-cache', [])
            
            if redis_services:
                credentials = redis_services[0]['credentials']
                return {
                    'host': credentials.get('hostname'),
                    'port': credentials.get('port'),
                    'password': credentials.get('password'),
                    'ssl': credentials.get('tls', False),
                    'url': credentials.get('uri')
                }
        except (json.JSONDecodeError, KeyError, IndexError):
            pass
    return None

BUGSNAG_KEY = ""

if REALM == 'prod':
    DEBUG = False
    ROOT_URL = "http://requestb.in"

    FLASK_SESSION_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", FLASK_SESSION_SECRET_KEY)

    STORAGE_BACKEND = "requestbin.storage.redis.RedisStorage"

    # Try to get Redis config from SAP BTP VCAP_SERVICES first
    vcap_redis_config = get_redis_config_from_vcap()
    
    if vcap_redis_config:
        # Use SAP BTP Redis service
        REDIS_HOST = vcap_redis_config['host']
        REDIS_PORT = vcap_redis_config['port']
        REDIS_PASSWORD = vcap_redis_config['password']
        REDIS_SSL = vcap_redis_config['ssl']
        REDIS_DB = 0  # SAP BTP Redis typically uses DB 0
        if vcap_redis_config['ssl']:
            import ssl
            REDIS_SSL_CERT_REQS = ssl.CERT_REQUIRED
    else:
        # Fallback to environment variable (for other deployments)
        REDIS_URL = os.environ.get("REDIS_URL")
        if REDIS_URL:
            url_parts = parse.urlparse(REDIS_URL)
            REDIS_HOST = url_parts.hostname
            REDIS_PORT = url_parts.port
            REDIS_PASSWORD = url_parts.password
            REDIS_DB = url_parts.fragment or 0
            # Check if URL uses rediss:// (SSL)
            REDIS_SSL = url_parts.scheme == 'rediss'
            if REDIS_SSL:
                import ssl
                REDIS_SSL_CERT_REQS = ssl.CERT_REQUIRED

    BUGSNAG_KEY = os.environ.get("BUGSNAG_KEY", BUGSNAG_KEY)

    IGNORE_HEADERS = """
X-Varnish
X-Forwarded-For
X-Heroku-Dynos-In-Use
X-Request-Start
X-Heroku-Queue-Wait-Time
X-Heroku-Queue-Depth
X-Real-Ip
X-Forwarded-Proto
X-Via
X-Forwarded-Port
""".split("\n")[1:-1]
