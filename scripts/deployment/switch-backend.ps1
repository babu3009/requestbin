# RequestBin Storage Backend Switcher for Docker Compose (PowerShell)

param(
    [Parameter(Position=0)]
    [ValidateSet('redis', 'postgresql', 'postgres', 'status', '')]
    [string]$Backend
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Function to display usage
function Show-Usage {
    Write-Host "`nRequestBin Storage Backend Switcher" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\switch-backend.ps1 [redis|postgresql|postgres|status]"
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor Yellow
    Write-Host "  redis       - Switch to Redis storage backend"
    Write-Host "  postgresql  - Switch to PostgreSQL storage backend"
    Write-Host "  postgres    - Switch to PostgreSQL storage backend (alias)"
    Write-Host "  status      - Show current storage backend configuration"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\switch-backend.ps1 redis                # Switch to Redis"
    Write-Host "  .\switch-backend.ps1 postgresql           # Switch to PostgreSQL"
    Write-Host "  .\switch-backend.ps1 status               # Show current backend"
    Write-Host ""
    exit 1
}

# Function to show current status
function Show-Status {
    Write-Host ""
    Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "  RequestBin Storage Backend Status" -ForegroundColor White
    Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    
    if (Test-Path ".env") {
        $envContent = Get-Content ".env"
        $currentBackend = ($envContent | Select-String "^STORAGE_BACKEND=").ToString().Split('=')[1]
        
        Write-Host "Current Backend: " -NoNewline -ForegroundColor Green
        Write-Host $currentBackend
        Write-Host ""
        Write-Host "Current Configuration:" -ForegroundColor Yellow
        $envContent | Select-String "^(STORAGE_BACKEND|POSTGRES_|REDIS_)" | ForEach-Object {
            Write-Host "  $_"
        }
    } else {
        Write-Host "No .env file found. Using default (Redis) backend." -ForegroundColor Yellow
    }
    Write-Host ""
}

# Function to switch backend
function Switch-Backend {
    param([string]$BackendType)
    
    $envFile = ""
    $backendName = ""
    
    switch ($BackendType) {
        "redis" {
            $envFile = ".env.redis"
            $backendName = "Redis"
        }
        { $_ -in @("postgresql", "postgres") } {
            $envFile = ".env.postgresql"
            $backendName = "PostgreSQL"
        }
        default {
            Write-Host "Error: Invalid backend '$BackendType'" -ForegroundColor Red
            Show-Usage
        }
    }
    
    if (-not (Test-Path $envFile)) {
        Write-Host "Error: Configuration file '$envFile' not found!" -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
    Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "  Switching to $backendName Storage Backend" -ForegroundColor White
    Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    
    # Backup existing .env if it exists
    if (Test-Path ".env") {
        Write-Host "Backing up current .env to .env.backup" -ForegroundColor Yellow
        Copy-Item ".env" ".env.backup" -Force
    }
    
    # Copy the new configuration
    Write-Host "Copying $envFile to .env" -ForegroundColor Green
    Copy-Item $envFile ".env" -Force
    
    Write-Host ""
    Write-Host "✓ Configuration updated successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Restart the application:"
    Write-Host "     " -NoNewline
    Write-Host "docker-compose restart app" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  2. Or restart all services:"
    Write-Host "     " -NoNewline
    Write-Host "docker-compose down; docker-compose up -d" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  3. View logs:"
    Write-Host "     " -NoNewline
    Write-Host "docker-compose logs -f app" -ForegroundColor Cyan
    Write-Host ""
    
    # Show new configuration
    Show-Status
}

# Main script logic
if ([string]::IsNullOrEmpty($Backend)) {
    Show-Usage
} else {
    switch ($Backend) {
        "redis" { Switch-Backend "redis" }
        { $_ -in @("postgresql", "postgres") } { Switch-Backend "postgresql" }
        "status" { Show-Status }
        default { Show-Usage }
    }
}
