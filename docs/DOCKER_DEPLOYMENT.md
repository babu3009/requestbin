# Docker Deployment Guide

This guide explains how to deploy RequestBin using Docker Compose with either Redis or PostgreSQL as the storage backend.

## Quick Start

### Default (Redis Backend)

The simplest way to start RequestBin with Redis storage:

```bash
docker-compose up -d
```

This will start:
- RequestBin application on port 8000
- Redis for storage (with persistent volume)
- PostgreSQL (running but not used)

### Switch to PostgreSQL Backend

To use PostgreSQL instead of Redis:

1. **Copy the PostgreSQL environment file:**
   ```bash
   # Windows PowerShell
   Copy-Item .env.postgresql .env
   
   # Linux/Mac
   cp .env.postgresql .env
   ```

2. **Start the services:**
   ```bash
   docker-compose up -d
   ```

### Switch to Redis Backend

To switch back to Redis:

1. **Copy the Redis environment file:**
   ```bash
   # Windows PowerShell
   Copy-Item .env.redis .env
   
   # Linux/Mac
   cp .env.redis .env
   ```

2. **Restart the services:**
   ```bash
   docker-compose restart app
   ```

## Storage Backend Comparison

| Feature | Redis | PostgreSQL |
|---------|-------|------------|
| **Speed** | Very Fast | Fast |
| **Persistence** | Good (AOF enabled) | Excellent (ACID compliant) |
| **Data Integrity** | Good | Excellent |
| **Memory Usage** | Higher | Lower |
| **Scalability** | Excellent | Excellent |
| **Best For** | High-speed caching, temporary data | Long-term storage, production use |

## Configuration Options

### Environment Variables

You can customize the deployment by editing the `.env` file or setting environment variables:

#### Storage Backend
```bash
# Choose your storage backend
STORAGE_BACKEND=requestbin.storage.redis.RedisStorage
# or
STORAGE_BACKEND=requestbin.storage.postgresql.PostgreSQLStorage
```

#### PostgreSQL Settings
```bash
POSTGRES_HOST=postgres          # PostgreSQL host (default: postgres)
POSTGRES_PORT=5432              # PostgreSQL port (default: 5432)
POSTGRES_DB=requestbin          # Database name
POSTGRES_USER=requestbin        # Database user
POSTGRES_PASSWORD=requestbin123 # Database password
POSTGRES_SCHEMA=requestbin_app  # Schema name
```

#### Redis Settings
```bash
REDIS_URL=//redis:6379          # Redis connection URL
```

#### Application Settings
```bash
MAX_REQUESTS=200                # Maximum requests per bin
BIN_TTL=345600                  # Bin lifetime in seconds (96 hours)
WORKERS=2                       # Number of Gunicorn workers
```

## Advanced Usage

### Build and Run

```bash
# Build the image
docker-compose build

# Start services in detached mode
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down

# Stop and remove volumes (WARNING: This deletes all data!)
docker-compose down -v
```

### Using Custom Configuration

Create your own `.env` file with custom settings:

```bash
# .env
STORAGE_BACKEND=requestbin.storage.postgresql.PostgreSQLStorage
POSTGRES_PASSWORD=your_secure_password_here
MAX_REQUESTS=500
BIN_TTL=172800  # 48 hours
```

Then start the services:

```bash
docker-compose up -d
```

### Accessing Services

- **RequestBin Web UI:** http://localhost:8000
- **PostgreSQL Database:** localhost:5432 (from host machine)
- **Redis:** localhost:6379 (if you expose the port)

### Expose Database Ports (Optional)

To access the databases from your host machine, add port mappings:

```yaml
# In docker-compose.yml
postgres:
  ports:
    - "5432:5432"

redis:
  ports:
    - "6379:6379"
```

## Data Persistence

Both Redis and PostgreSQL use Docker volumes for data persistence:

- **redis-data:** Stores Redis AOF files
- **postgres-data:** Stores PostgreSQL database files

### Backup PostgreSQL Data

```bash
# Create backup
docker-compose exec postgres pg_dump -U requestbin requestbin > backup.sql

# Restore backup
docker-compose exec -T postgres psql -U requestbin requestbin < backup.sql
```

### Backup Redis Data

```bash
# Create backup
docker-compose exec redis redis-cli SAVE
docker cp $(docker-compose ps -q redis):/data/dump.rdb ./redis-backup.rdb

# Restore backup
docker cp ./redis-backup.rdb $(docker-compose ps -q redis):/data/dump.rdb
docker-compose restart redis
```

## Troubleshooting

### Check Service Health

```bash
# Check all services status
docker-compose ps

# Check specific service logs
docker-compose logs app
docker-compose logs postgres
docker-compose logs redis
```

### PostgreSQL Connection Issues

```bash
# Check if PostgreSQL is ready
docker-compose exec postgres pg_isready -U requestbin

# Connect to PostgreSQL
docker-compose exec postgres psql -U requestbin -d requestbin

# Verify schema
docker-compose exec postgres psql -U requestbin -d requestbin -c "\dn"
```

### Redis Connection Issues

```bash
# Check Redis connectivity
docker-compose exec redis redis-cli ping

# Check Redis info
docker-compose exec redis redis-cli INFO
```

### Application Issues

```bash
# Check environment variables
docker-compose exec app env | grep -E 'STORAGE|POSTGRES|REDIS'

# Restart application
docker-compose restart app

# View real-time logs
docker-compose logs -f app
```

### Database Migration

If you want to switch from Redis to PostgreSQL (or vice versa) and preserve data:

1. **Export data from current backend** (if applicable)
2. **Switch to new backend** by updating `.env`
3. **Restart services:**
   ```bash
   docker-compose down
   docker-compose up -d
   ```

**Note:** Data is NOT automatically migrated between storage backends. Each backend maintains its own data store.

## Production Deployment

For production deployments, consider:

1. **Use PostgreSQL** for better data integrity and persistence
2. **Set strong passwords** in your `.env` file
3. **Enable SSL/TLS** for database connections
4. **Use environment secrets** instead of `.env` files
5. **Set up regular backups**
6. **Monitor resource usage**
7. **Configure log rotation**
8. **Use a reverse proxy** (nginx, traefik) for HTTPS

Example production `.env`:

```bash
STORAGE_BACKEND=requestbin.storage.postgresql.PostgreSQLStorage
POSTGRES_PASSWORD=your_very_secure_password_here
MAX_REQUESTS=1000
BIN_TTL=604800  # 7 days
WORKERS=4
```

## Resource Requirements

### Minimum Requirements
- **CPU:** 1 core
- **RAM:** 512 MB
- **Disk:** 2 GB

### Recommended for Production
- **CPU:** 2+ cores
- **RAM:** 2 GB+
- **Disk:** 10 GB+ (depending on usage)

## Support

For issues and questions:
- GitHub Issues: https://github.com/babu3009/requestbin/issues
- Documentation: See README.md

## License

MIT License - See LICENSE file for details
