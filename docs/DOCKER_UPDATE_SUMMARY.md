# Docker Compose Update Summary

## Overview

The docker-compose.yml has been completely updated to support **both Redis and PostgreSQL** storage backends with easy switching between them.

## What's New

### 1. Enhanced docker-compose.yml

**New Features:**
- ✅ PostgreSQL service with persistent storage
- ✅ Redis service with AOF persistence
- ✅ Environment-based backend switching
- ✅ Health checks for all services
- ✅ Named volumes for data persistence
- ✅ Custom network for service isolation
- ✅ Automatic schema initialization for PostgreSQL

**Services Included:**
- `app` - RequestBin application (port 8000)
- `postgres` - PostgreSQL 15 Alpine (port 5432)
- `redis` - Redis 7 Alpine (port 6379)

### 2. Environment Configuration Files

**Three configuration files:**
- `.env` - Active configuration (used by docker-compose)
- `.env.redis` - Redis backend template
- `.env.postgresql` - PostgreSQL backend template

**Key Environment Variables:**
```bash
STORAGE_BACKEND          # Which storage to use
POSTGRES_HOST            # PostgreSQL host
POSTGRES_PORT            # PostgreSQL port (5432)
POSTGRES_DB              # Database name
POSTGRES_USER            # Database user
POSTGRES_PASSWORD        # Database password
POSTGRES_SCHEMA          # Schema name (requestbin_app)
REDIS_URL                # Redis connection URL
MAX_REQUESTS             # Max requests per bin (200)
BIN_TTL                  # Bin lifetime in seconds (345600 = 96 hours)
```

### 3. Backend Switching Scripts

**PowerShell (Windows):**
```powershell
.\switch-backend.ps1 redis          # Switch to Redis
.\switch-backend.ps1 postgresql     # Switch to PostgreSQL
.\switch-backend.ps1 status         # Show current backend
```

**Bash (Linux/Mac):**
```bash
./switch-backend.sh redis           # Switch to Redis
./switch-backend.sh postgresql      # Switch to PostgreSQL
./switch-backend.sh status          # Show current backend
```

**Features:**
- Automatic backup of current .env
- Color-coded output
- Configuration validation
- Usage instructions
- Status display

### 4. Documentation Files

**New Documentation:**
- `DOCKER_DEPLOYMENT.md` - Comprehensive deployment guide
  - Storage backend comparison
  - Configuration options
  - Advanced usage
  - Backup/restore procedures
  - Troubleshooting
  - Production deployment tips

- `DOCKER_QUICK_START.md` - Quick reference
  - Common commands
  - Database access
  - Troubleshooting
  - Default credentials

**Updated Documentation:**
- `README.md` - Added Docker Compose section with backend switching

### 5. Updated .gitignore

**Changes:**
- Ignore `.env` (active config - may contain secrets)
- Keep `.env.redis` and `.env.postgresql` (templates)
- Ignore `.env.backup` (auto-created backups)
- Added Docker and database ignores

## Usage

### Quick Start - Redis (Default)

```bash
# Clone the repository
git clone https://github.com/babu3009/requestbin.git
cd requestbin

# Start with Redis (default)
docker-compose up -d

# Access RequestBin
open http://localhost:8000
```

### Quick Start - PostgreSQL

```bash
# Clone the repository
git clone https://github.com/babu3009/requestbin.git
cd requestbin

# Switch to PostgreSQL
# Windows:
Copy-Item .env.postgresql .env

# Linux/Mac:
cp .env.postgresql .env

# Start services
docker-compose up -d

# Access RequestBin
open http://localhost:8000
```

### Switching Backends

**Method 1: Using Scripts (Recommended)**

Windows:
```powershell
.\switch-backend.ps1 postgresql
docker-compose restart app
```

Linux/Mac:
```bash
chmod +x switch-backend.sh
./switch-backend.sh postgresql
docker-compose restart app
```

**Method 2: Manual**

```bash
# Copy desired configuration
cp .env.postgresql .env  # For PostgreSQL
# or
cp .env.redis .env       # For Redis

# Restart application
docker-compose restart app
```

## Architecture

```
┌─────────────────────────────────────────────────┐
│                RequestBin App                    │
│              (Port 8000)                         │
│                                                  │
│  Environment Variable: STORAGE_BACKEND           │
└───────────┬─────────────────────────┬───────────┘
            │                         │
            │                         │
    ┌───────▼────────┐      ┌────────▼────────┐
    │     Redis      │      │   PostgreSQL    │
    │  (Port 6379)   │      │   (Port 5432)   │
    │                │      │                 │
    │  Volume:       │      │  Volume:        │
    │  redis-data    │      │  postgres-data  │
    └────────────────┘      └─────────────────┘
```

## Storage Backend Comparison

| Feature | Redis | PostgreSQL |
|---------|-------|------------|
| **Speed** | ⚡⚡⚡ Very Fast | ⚡⚡ Fast |
| **Persistence** | ✅ Good (AOF) | ✅✅ Excellent (ACID) |
| **Data Integrity** | ✅ Good | ✅✅ Excellent |
| **Memory Usage** | Higher | Lower |
| **Best For** | Caching, temporary | Production, long-term |
| **Setup Complexity** | Simple | Simple |
| **Backup** | Redis SAVE/BGSAVE | pg_dump |

## Data Persistence

Both backends use Docker named volumes for persistent storage:

- **redis-data** - Stores Redis AOF files
- **postgres-data** - Stores PostgreSQL database

**Data survives container restarts** but is lost if you run:
```bash
docker-compose down -v  # ⚠️ WARNING: Deletes all data!
```

## Backup and Restore

### PostgreSQL Backup
```bash
# Backup
docker-compose exec postgres pg_dump -U requestbin requestbin > backup.sql

# Restore
docker-compose exec -T postgres psql -U requestbin requestbin < backup.sql
```

### Redis Backup
```bash
# Backup
docker-compose exec redis redis-cli SAVE
docker cp $(docker-compose ps -q redis):/data/dump.rdb ./redis-backup.rdb

# Restore
docker cp ./redis-backup.rdb $(docker-compose ps -q redis):/data/dump.rdb
docker-compose restart redis
```

## Troubleshooting

### Check Services Status
```bash
docker-compose ps
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f app
docker-compose logs -f postgres
docker-compose logs -f redis
```

### Check Database Connection

**PostgreSQL:**
```bash
docker-compose exec postgres pg_isready -U requestbin
docker-compose exec postgres psql -U requestbin -d requestbin -c "SELECT version();"
```

**Redis:**
```bash
docker-compose exec redis redis-cli ping
docker-compose exec redis redis-cli INFO
```

### Verify Storage Backend
```bash
docker-compose exec app env | grep STORAGE_BACKEND
```

### Clean Restart
```bash
docker-compose down
docker-compose up -d
docker-compose logs -f app
```

## Security Notes

⚠️ **Default credentials are NOT secure for production!**

For production deployment:

1. **Change PostgreSQL password** in `.env`:
   ```bash
   POSTGRES_PASSWORD=your_very_secure_password_here
   ```

2. **Use environment secrets** instead of `.env` file

3. **Enable SSL/TLS** for database connections

4. **Use a reverse proxy** (nginx, traefik) for HTTPS

5. **Set up firewall rules** to restrict database access

6. **Regular backups** of data volumes

## Files Changed/Added

### New Files
- `.env` - Active environment configuration
- `.env.redis` - Redis backend template
- `.env.postgresql` - PostgreSQL backend template
- `switch-backend.ps1` - PowerShell backend switcher
- `switch-backend.sh` - Bash backend switcher
- `DOCKER_DEPLOYMENT.md` - Comprehensive deployment guide
- `DOCKER_QUICK_START.md` - Quick reference guide
- `DOCKER_UPDATE_SUMMARY.md` - This file

### Modified Files
- `docker-compose.yml` - Complete rewrite with PostgreSQL support
- `README.md` - Added Docker Compose section
- `.gitignore` - Added environment and Docker ignores

### Unchanged Files
- `schema.sql` - PostgreSQL schema (already existed)
- `Dockerfile` - Application container build
- `requirements.txt` - Python dependencies
- Application code - No changes needed

## Migration Path

### From Old docker-compose.yml

If you were using the old docker-compose.yml with only Redis:

1. **Backup your data** (if needed):
   ```bash
   docker-compose exec redis redis-cli SAVE
   ```

2. **Stop the old stack**:
   ```bash
   docker-compose down
   ```

3. **Update docker-compose.yml** (already done in this update)

4. **Start new stack**:
   ```bash
   docker-compose up -d
   ```

5. **Verify** everything works:
   ```bash
   docker-compose ps
   docker-compose logs -f app
   ```

### From Memory Storage to Docker

If you were using memory storage locally:

1. **No data migration** needed (memory storage is temporary)

2. **Choose backend** (Redis or PostgreSQL)

3. **Start Docker Compose**:
   ```bash
   docker-compose up -d
   ```

4. **Verify** in browser at http://localhost:8000

## Testing the Setup

### 1. Start Services
```bash
docker-compose up -d
```

### 2. Create a Test Bin
```bash
# Create bin via API
curl -X POST http://localhost:8000/api/v1/bins

# Or visit http://localhost:8000 in browser
```

### 3. Send Test Request
```bash
curl -X POST http://localhost:8000/<your-bin-id> \
  -H "Content-Type: application/json" \
  -d '{"test": "data", "storage": "docker"}'
```

### 4. Inspect Requests
```bash
# Via browser
open http://localhost:8000/<your-bin-id>?inspect

# Via API
curl http://localhost:8000/api/v1/bins/<your-bin-id>/requests
```

### 5. Test Backend Switching

**Switch to PostgreSQL:**
```bash
# Windows
.\switch-backend.ps1 postgresql
docker-compose restart app

# Linux/Mac
./switch-backend.sh postgresql
docker-compose restart app
```

**Verify:**
```bash
docker-compose logs app | grep -i storage
```

### 6. Test Persistence

**Stop and restart:**
```bash
docker-compose down
docker-compose up -d
```

**Check if bins still exist:**
```bash
curl http://localhost:8000/api/v1/bins/<your-bin-id>
```

## Next Steps

1. **Choose your storage backend** (Redis for speed, PostgreSQL for production)
2. **Review security settings** before production deployment
3. **Set up backups** if using in production
4. **Configure monitoring** (optional)
5. **Set up reverse proxy** for HTTPS (recommended for production)

## Support

For issues and questions:
- **GitHub Issues:** https://github.com/babu3009/requestbin/issues
- **Documentation:** See README.md, DOCKER_DEPLOYMENT.md, DOCKER_QUICK_START.md

## License

MIT License - See LICENSE file for details

---

**Last Updated:** October 17, 2025  
**Version:** 2.0 (Docker Compose with dual backend support)
