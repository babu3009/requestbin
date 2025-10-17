import os
import json
from urllib import parse
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
# override=False means environment variables take precedence over .env file
load_dotenv(override=False)

DEBUG = True
REALM = os.environ.get('REALM', 'local')

ROOT_URL = "http://localhost:3200"

PORT_NUMBER = 3200

ENABLE_CORS = False
CORS_ORIGINS = "*"

FLASK_SESSION_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", "N1BKhJLnBqLpexOZdklsfDKFJDKFadsfs9a3r324YB7B73AglRmrHMDQ9RhXz35")

BIN_TTL = 96*3600
# Storage backend can be overridden by environment variable
STORAGE_BACKEND = os.environ.get('STORAGE_BACKEND', "requestbin.storage.memory.MemoryStorage")
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

# PostgreSQL configuration defaults
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = int(os.environ.get('POSTGRES_PORT', 5432))
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'requestbin')
POSTGRES_SCHEMA = os.environ.get('POSTGRES_SCHEMA', 'requestbin_app')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', '')
POSTGRES_SSLMODE = os.environ.get('POSTGRES_SSLMODE', 'prefer')

# Authentication configuration
AUTO_APPROVE_DOMAINS = os.environ.get('AUTO_APPROVE_DOMAINS', 'tarento.com,ivolve.ai').split(',')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@requestbin.local')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')  # Change this in production!

# SMTP Email configuration for OTP verification
SMTP_HOST = os.environ.get('SMTP_HOST', None)
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USER = os.environ.get('SMTP_USER', None)
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', None)
SMTP_USE_TLS = os.environ.get('SMTP_USE_TLS', 'true').lower() == 'true'
SMTP_FROM_EMAIL = os.environ.get('SMTP_FROM_EMAIL', SMTP_USER)

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

# Function to parse SAP BTP VCAP_SERVICES for PostgreSQL
def get_postgres_config_from_vcap():
    vcap_services = os.getenv('VCAP_SERVICES')
    if vcap_services:
        try:
            services = json.loads(vcap_services)
            # Look for PostgreSQL service in various possible service names
            postgres_services = services.get('postgresql', [])
            if not postgres_services:
                postgres_services = services.get('postgresql-db', [])
            if not postgres_services:
                postgres_services = services.get('postgres', [])
            
            if postgres_services:
                credentials = postgres_services[0]['credentials']
                return {
                    'host': credentials.get('hostname') or credentials.get('host'),
                    'port': credentials.get('port', 5432),
                    'database': credentials.get('dbname') or credentials.get('database') or credentials.get('name'),
                    'user': credentials.get('username') or credentials.get('user'),
                    'password': credentials.get('password'),
                    'sslmode': 'require' if credentials.get('sslmode') == 'require' else 'prefer'
                }
        except (json.JSONDecodeError, KeyError, IndexError):
            pass
    return None

# Load PostgreSQL configuration from environment (works for both local and prod)
if STORAGE_BACKEND == "requestbin.storage.postgresql.PostgreSQLStorage":
    vcap_postgres_config = get_postgres_config_from_vcap()
    
    if vcap_postgres_config:
        # Use SAP BTP PostgreSQL service
        POSTGRES_HOST = vcap_postgres_config['host']
        POSTGRES_PORT = vcap_postgres_config['port']
        POSTGRES_DB = vcap_postgres_config['database']
        POSTGRES_USER = vcap_postgres_config['user']
        POSTGRES_PASSWORD = vcap_postgres_config['password']
        POSTGRES_SSLMODE = vcap_postgres_config['sslmode']
    else:
        # Fallback to environment variables
        POSTGRES_HOST = os.environ.get('POSTGRES_HOST', POSTGRES_HOST)
        POSTGRES_PORT = int(os.environ.get('POSTGRES_PORT', POSTGRES_PORT))
        POSTGRES_DB = os.environ.get('POSTGRES_DB', POSTGRES_DB)
        POSTGRES_USER = os.environ.get('POSTGRES_USER', POSTGRES_USER)
        POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', POSTGRES_PASSWORD)
        POSTGRES_SSLMODE = os.environ.get('POSTGRES_SSLMODE', POSTGRES_SSLMODE)

# Load Redis configuration from environment (works for both local and prod)
if STORAGE_BACKEND == "requestbin.storage.redis.RedisStorage":
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

BUGSNAG_KEY = ""

if REALM == 'prod':
    DEBUG = False
    ROOT_URL = "http://requestb.in"

    FLASK_SESSION_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", FLASK_SESSION_SECRET_KEY)
    
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
