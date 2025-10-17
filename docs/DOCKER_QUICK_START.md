# RequestBin Docker Compose - Quick Reference

## Quick Commands

### Start with Redis (default)
```bash
docker-compose up -d
```

### Start with PostgreSQL
```bash
# Windows PowerShell
Copy-Item .env.postgresql .env
docker-compose up -d

# Linux/Mac
cp .env.postgresql .env
docker-compose up -d
```

### Switch Between Backends

#### Windows PowerShell
```powershell
# Switch to Redis
.\switch-backend.ps1 redis
docker-compose restart app

# Switch to PostgreSQL
.\switch-backend.ps1 postgresql
docker-compose restart app

# Check current backend
.\switch-backend.ps1 status
```

#### Linux/Mac
```bash
# Make script executable (first time only)
chmod +x switch-backend.sh

# Switch to Redis
./switch-backend.sh redis
docker-compose restart app

# Switch to PostgreSQL
./switch-backend.sh postgresql
docker-compose restart app

# Check current backend
./switch-backend.sh status
```

### View Services Status
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

### Stop Services
```bash
# Stop (keep data)
docker-compose down

# Stop and remove volumes (delete all data!)
docker-compose down -v
```

### Rebuild After Code Changes
```bash
docker-compose build
docker-compose up -d
```

## Access Points

- **Web UI:** http://localhost:8000
- **API:** http://localhost:8000/api/v1/
- **About Page:** http://localhost:8000/about

## Database Access

### PostgreSQL
```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U requestbin -d requestbin

# Run query
docker-compose exec postgres psql -U requestbin -d requestbin -c "SELECT * FROM requestbin_app.bins;"

# Backup
docker-compose exec postgres pg_dump -U requestbin requestbin > backup.sql

# Restore
docker-compose exec -T postgres psql -U requestbin requestbin < backup.sql
```

### Redis
```bash
# Connect to Redis CLI
docker-compose exec redis redis-cli

# Check connection
docker-compose exec redis redis-cli ping

# Get all keys
docker-compose exec redis redis-cli KEYS '*'

# Backup
docker-compose exec redis redis-cli SAVE
```

## Troubleshooting

### Check if services are healthy
```bash
docker-compose ps
```

### Restart a specific service
```bash
docker-compose restart app
docker-compose restart postgres
docker-compose restart redis
```

### View environment variables
```bash
docker-compose exec app env | grep -E 'STORAGE|POSTGRES|REDIS'
```

### Clean restart
```bash
docker-compose down
docker-compose up -d
docker-compose logs -f app
```

## Storage Backend Info

| Backend | Speed | Persistence | Best For |
|---------|-------|-------------|----------|
| Redis | Very Fast | Good | Temporary, high-speed |
| PostgreSQL | Fast | Excellent | Production, long-term |

## Default Credentials

### PostgreSQL
- **Host:** localhost (or postgres inside container)
- **Port:** 5432
- **Database:** requestbin
- **User:** requestbin
- **Password:** requestbin123
- **Schema:** requestbin_app

### Redis
- **Host:** localhost (or redis inside container)
- **Port:** 6379
- **No password** (default)

⚠️ **Security Note:** Change these credentials in production by editing `.env` file!

## Configuration Files

- **docker-compose.yml** - Main Docker Compose configuration
- **.env** - Active environment configuration (git-ignored)
- **.env.redis** - Redis backend template
- **.env.postgresql** - PostgreSQL backend template
- **switch-backend.ps1** - PowerShell backend switcher
- **switch-backend.sh** - Bash backend switcher

## More Information

See `DOCKER_DEPLOYMENT.md` for comprehensive deployment guide.
