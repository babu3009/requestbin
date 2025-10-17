#!/bin/bash
# RequestBin Storage Backend Switcher for Docker Compose

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo -e "${BLUE}RequestBin Storage Backend Switcher${NC}"
    echo ""
    echo "Usage: $0 [redis|postgresql|postgres|status]"
    echo ""
    echo "Commands:"
    echo "  redis       - Switch to Redis storage backend"
    echo "  postgresql  - Switch to PostgreSQL storage backend"
    echo "  postgres    - Switch to PostgreSQL storage backend (alias)"
    echo "  status      - Show current storage backend configuration"
    echo ""
    echo "Examples:"
    echo "  $0 redis                # Switch to Redis"
    echo "  $0 postgresql           # Switch to PostgreSQL"
    echo "  $0 status               # Show current backend"
    exit 1
}

# Function to show current status
show_status() {
    echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  RequestBin Storage Backend Status${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
    echo ""
    
    if [ -f ".env" ]; then
        CURRENT_BACKEND=$(grep "^STORAGE_BACKEND=" .env | cut -d'=' -f2)
        echo -e "${GREEN}Current Backend:${NC} $CURRENT_BACKEND"
        echo ""
        echo -e "${YELLOW}Current Configuration:${NC}"
        grep -E "^(STORAGE_BACKEND|POSTGRES_|REDIS_)" .env | while read line; do
            echo "  $line"
        done
    else
        echo -e "${YELLOW}No .env file found. Using default (Redis) backend.${NC}"
    fi
    echo ""
}

# Function to switch backend
switch_backend() {
    local backend=$1
    local env_file=""
    
    case "$backend" in
        redis)
            env_file=".env.redis"
            backend_name="Redis"
            ;;
        postgresql|postgres)
            env_file=".env.postgresql"
            backend_name="PostgreSQL"
            ;;
        *)
            echo -e "${RED}Error: Invalid backend '$backend'${NC}"
            usage
            ;;
    esac
    
    if [ ! -f "$env_file" ]; then
        echo -e "${RED}Error: Configuration file '$env_file' not found!${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Switching to $backend_name Storage Backend${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Backup existing .env if it exists
    if [ -f ".env" ]; then
        echo -e "${YELLOW}Backing up current .env to .env.backup${NC}"
        cp .env .env.backup
    fi
    
    # Copy the new configuration
    echo -e "${GREEN}Copying $env_file to .env${NC}"
    cp "$env_file" .env
    
    echo ""
    echo -e "${GREEN}✓ Configuration updated successfully!${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "  1. Restart the application:"
    echo "     ${BLUE}docker-compose restart app${NC}"
    echo ""
    echo "  2. Or restart all services:"
    echo "     ${BLUE}docker-compose down && docker-compose up -d${NC}"
    echo ""
    echo "  3. View logs:"
    echo "     ${BLUE}docker-compose logs -f app${NC}"
    echo ""
    
    # Show new configuration
    show_status
}

# Main script logic
case "${1:-}" in
    redis)
        switch_backend "redis"
        ;;
    postgresql|postgres)
        switch_backend "postgresql"
        ;;
    status)
        show_status
        ;;
    *)
        usage
        ;;
esac
