# RequestBin Enterprise

RequestBin Enterprise gives you a URL that will collect requests made to it and let you inspect them in a human-friendly way. Use RequestBin Enterprise to see what your HTTP client is sending or to inspect and debug webhook requests.

## Features

- **Split-Panel Outlook-Style Interface**: Modern UX with tabular request list and detailed view
- **Real-time Request Inspection**: View headers, query parameters, form data, and raw body
- **Multiple Storage Backends**: Memory, Redis, or PostgreSQL
- **Authentication System**: User registration, login, and OTP email verification
- **Password Management**: Change password and forgot password with OTP reset
- **User-Specific Bins**: Each user has their own bin history and management
- **Data Persistence**: Configurable bin TTL (default: 96 hours)
- **RESTful API**: Programmatic bin and request management
- **Docker Support**: Easy deployment with Docker and Docker Compose
- **SAP BTP Ready**: Optimized for SAP Business Technology Platform
- **Modular Architecture**: Clean, organized codebase following Python best practices
- **WebSocket Support**: Real-time auto-updates for bin requests via Socket.IO
- **Modern UI/UX**: Copy-to-clipboard functionality, improved navigation, responsive design

## Real-Time Features

### WebSocket Integration

RequestBin Enterprise includes WebSocket support for real-time updates:

- **Automatic Request Updates**: New requests appear instantly without page refresh
- **Socket.IO Integration**: Robust WebSocket implementation using Flask-SocketIO
- **Room-Based Updates**: Each bin has its own channel for targeted notifications
- **Fallback Support**: Graceful degradation if WebSocket connection fails

**How it Works:**
1. When you open a bin's inspect view, a WebSocket connection is established
2. When new requests arrive, the server emits a `bin_updated` event
3. Your browser automatically refreshes the request list
4. No manual refresh needed - just watch requests stream in real-time

**Technical Details:**
- Uses Flask-SocketIO with gevent async mode
- CORS-enabled for cross-origin support
- Event-driven architecture with join/leave room management
- Compatible with all modern browsers

## Project Structure

The project follows a modular architecture for better maintainability:

```
requestbin/
├── config/              # Deployment configurations
│   ├── manifest.yml     # Cloud Foundry (Redis)
│   ├── manifest-postgresql.yml
│   └── app.json         # Heroku config
├── docs/                # Comprehensive documentation
├── test/                # All test scripts
├── scripts/             # Organized utility scripts
│   ├── admin/          # User management tools
│   ├── database/       # Database scripts
│   ├── deployment/     # Deployment helpers
│   └── debug/          # Diagnostic tools
└── requestbin/          # Main Python package
    ├── views/          # View modules (main, auth, api)
    ├── auth/           # Authentication (models, forms, storage, utils)
    ├── database/       # Database management
    ├── storage/        # Storage backends (memory, redis, postgresql)
    ├── static/         # Static assets (CSS, JS, images)
    └── templates/      # HTML templates
```

### Key Directories

- **`requestbin/`** - Core application package with modular subpackages
- **`scripts/`** - Organized utility scripts for admin, database, deployment, and debugging
- **`config/`** - Centralized deployment configuration files
- **`docs/`** - Comprehensive documentation for all features
- **`test/`** - Test scripts with detailed test coverage

## Application Details

### User Interface Navigation

#### Home Page (`/`)
- **Create a New Bin**: Click the main button to generate a unique bin URL
- **Recent Bins**: View your recently created bins in the right sidebar
- **Authentication**: Login/Register links in the top navigation

#### Bin Inspect View (`/<bin-name>?inspect`)
- **Split-Panel Layout**: 
  - **Left Panel**: Tabular list of all requests with minimal details
    - Request number, timestamp (YYYY-MM-DD HH:mm:ss UTC)
    - HTTP method (color-coded badges: GET=green, POST=blue, PUT=orange, etc.)
    - Content-Type classification (json, xml, form-data, text, binary, raw)
    - Request size and source IP address
  - **Right Panel**: Full request details displayed when clicking a row
    - Complete headers
    - Query parameters
    - Form/POST parameters
    - Raw request body
    - Ready-to-use cURL command with copy-to-clipboard
- **Refresh Button**: Reload the table to see new requests
- **Auto-update**: Requests appear automatically as they arrive

#### User Profile (`/profile`)
- View account information
- Change your password
- Manage your bins
- See account statistics

#### Password Management
- **Change Password** (`/auth/change-password`): Update password while logged in
- **Forgot Password** (`/auth/forgot-password`): Request OTP via email
- **Reset Password** (`/auth/reset-password`): Reset password using OTP verification
- **Security Features**:
  - OTP codes expire after 24 hours
  - Single-use OTP for password reset
  - Minimum 8-character password requirement
  - Password confirmation to prevent typos
  - Secure password hashing with Werkzeug

#### Admin Panel (`/admin/users`) - Admin Only
- User management
- Approve/reject pending users
- System statistics
- Application monitoring

### How to Use

1. **Create a Bin**:
   ```bash
   # Via Web UI: Visit http://localhost:3200 and click "Create a RequestBin"
   # Via API: 
   curl -X POST http://localhost:3200/api/v1/bins
   ```

2. **Send Requests to Your Bin**:
   ```bash
   curl -X POST http://localhost:3200/<your-bin-id> \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'
   ```

3. **Inspect Requests**:
   - Open `http://localhost:3200/<your-bin-id>?inspect` in your browser
   - Click any request in the left panel to view full details
   - Use the refresh button to update the list
   - Copy cURL commands for replaying requests

4. **Share Your Bin**:
   - Share the bin URL with your webhook provider
   - Configure your application to send requests to the bin
   - Debug and test HTTP integrations in real-time

## Quick Start with Docker

### Simple Start (Redis Backend)

Launch your own RequestBin Enterprise instance with Docker:

```bash
docker run -p "8000:8000" babu3009/requestbin:latest
```

The pre-build image is available in the Docker central repository as [babu3009/requestbin](https://hub.docker.com/r/babu3009/requestbin).

### Docker Compose with Storage Options

Run RequestBin Enterprise with persistent storage using Docker Compose. You can choose between **Redis** (default) or **PostgreSQL** storage backends.

#### Start with Redis (Default)
```bash
docker-compose up -d
```

#### Start with PostgreSQL
```bash
# Windows PowerShell
Copy-Item .env.postgresql .env
docker-compose up -d

# Linux/Mac
cp .env.postgresql .env
docker-compose up -d
```

#### Switch Between Backends

Use the provided scripts to easily switch storage backends:

**Windows PowerShell:**
```powershell
.\switch-backend.ps1 postgresql    # Switch to PostgreSQL
.\switch-backend.ps1 redis         # Switch to Redis
.\switch-backend.ps1 status        # Check current backend
docker-compose restart app         # Apply changes
```

**Linux/Mac:**
```bash
chmod +x switch-backend.sh         # First time only
./switch-backend.sh postgresql     # Switch to PostgreSQL
./switch-backend.sh redis          # Switch to Redis
./switch-backend.sh status         # Check current backend
docker-compose restart app         # Apply changes
```

**📚 For detailed Docker deployment instructions, see:**
- **[DOCKER_QUICK_START.md](docs/DOCKER_QUICK_START.md)** - Quick reference and commands
- **[DOCKER_DEPLOYMENT.md](docs/DOCKER_DEPLOYMENT.md)** - Comprehensive deployment guide  

## Deploy to SAP BTP (Business Technology Platform)

This repository is configured for deployment to SAP BTP Cloud Foundry environment with Redis service.

### Prerequisites
1. CF CLI installed and configured
2. Access to SAP BTP space
3. Redis service instance created

### Deployment Steps

1. **Login to SAP BTP:**
   ```bash
   cf login -a <api-endpoint> -o <org> -s <space>
   ```

2. **Create Redis service (if not already created):**
   ```bash
   cf create-service redis-enterprise-cloud <plan> redis
   ```

3. **Deploy the application:**
   ```bash
   cf push -f manifest.yml
   ```

### Configuration Features
- **Automatic Redis Detection:** Automatically detects and configures Redis service via VCAP_SERVICES
- **SSL/TLS Support:** Supports encrypted Redis connections required by SAP BTP
- **Environment Variables:** Configurable request history size and bin TTL
- **Python Version:** Compatible with SAP BTP Python buildpack

### Environment Variables
- `MAX_REQUESTS`: Number of requests to keep per bin (default: 200 on SAP BTP)
- `BIN_TTL`: Bin lifetime in seconds (default: 96 hours)
- `REALM`: Set to 'prod' for production deployment

For detailed deployment instructions, see [SAP_BTP_DEPLOYMENT.md](docs/SAP_BTP_DEPLOYMENT.md).

## Run it with persistence

Clone the project from github

```
$ git clone https://github.com/babu3009/requestbin.git
```

From the project directory, run `docker-compose`:  

```
$ cd requestbin  
$ docker-compose up  
```  

This will run the automated build of the RequestBin Enterprise image and then pull down the trusted `redis` image and run with a mounted volume as a linked container to the RequestBin Enterprise app. RequestBin Enterprise would be exposed on the port `8000`.  


## Run it manually  

Pull the image down from the Docker central repository:  

```
$ docker run -d -p "8000:8000" babu3009/requestbin:latest
```

This will start the container with the requestbin app available externally on port 8000.  To run the image with a Redis back end, you need to startup redis first. Preferably with a mounted volume.

```
$ docker run -d -v /usr/data:/data \
      --name some-redis  \
      redis redis-server --appendonly yes

$ docker run -d --link some-redis:redis  \
	  -e "REALM=prod" -e REDIS_URL="//redis:6379" \
	  -p "8000:8000" \
	  babu3009/requestbin
```


## API Documentation

Documenting these details here, since many folks have tried to create custom APIs that provide the same feature. These are only for programmatic use. For General use, directly use the WebUI

### Bin Management

- **Create a new bin**
  - `POST /api/v1/bins`
  - **Description:** Creates a new request bin.  
    Optional form data:
    - `private`: (true/on) If set, creates a private bin.
    - `custom_name`: Custom name for the bin.

- **Get bin details**
  - `GET /api/v1/bins/<name>`
  - **Description:** Retrieves metadata/details for a specific bin.


### Requests Management

- **List all requests for a bin**
  - `GET /api/v1/bins/<bin>/requests`
  - **Description:** Returns all the requests made to the specified bin.

- **Get a specific request**
  - `GET /api/v1/bins/<bin>/requests/<name>`
  - **Description:** Retrieves details for a specific request captured by the bin.


### Statistics

- **Get global statistics**
  - `GET /api/v1/stats`
  - **Description:** Returns statistics such as:
    - `bin_count`: Total number of bins.
    - `request_count`: Total number of requests.
    - `avg_req_size_kb`: Average request size (in KB).


## Developing on local

```bash
# Using the deployment scripts
cd requestbin

# Run with PostgreSQL backend
.\scripts\deployment\run-postgres.bat        # Windows
./scripts/deployment/run-local-postgres.ps1  # PowerShell

# Run with Memory backend
./scripts/deployment/run-local-memory.ps1

# Switch between backends
.\scripts\deployment\switch-backend.ps1 postgresql
.\scripts\deployment\switch-backend.ps1 memory
```

### Development Tools

**Admin Tools:**
```bash
# Create admin user
python scripts/admin/create_admin.py

# Change user password
python scripts/admin/change_password.py
```

**Database Tools:**
```bash
# Initialize PostgreSQL schema
python scripts/database/init_postgres_schema.py
```

**Debug Tools:**
```bash
# Diagnose issues
python scripts/debug/diagnose.py

# Debug bin creation
python scripts/debug/debug_bin_creation.py
```

## Testing

### Running Tests

The project includes a comprehensive test suite covering all major functionality:

```bash
# Run all tests
python test/run_all_tests.py

# Run specific test suites
python test/test_smoke.py          # Quick sanity checks
python test/test_websocket.py      # WebSocket functionality
python test/test_ui_features.py    # UI/UX features
python test/test_auth.py           # Authentication system
python test/test_workflow.py       # Complete workflows
python test/test_all_modules.py    # Module imports
```

### Test Coverage

- **test_smoke.py**: Quick smoke tests (8 tests)
  - Package imports
  - Flask app initialization
  - WebSocket setup
  - Database connections

- **test_websocket.py**: WebSocket tests (18 tests)
  - SocketIO configuration
  - Client-side code
  - Event emission
  - Dependencies

- **test_ui_features.py**: UI/UX tests (22 tests)
  - Layout improvements
  - Bin URL display
  - Copy functionality
  - CSS styling
  - Password routes

- **test_auth.py**: Authentication tests
  - User model
  - Login/logout
  - Registration
  - OTP verification
  - Password management

- **test_workflow.py**: Integration tests
  - Complete user workflows
  - Bin creation and management
  - Request capture and inspection

### Test Configuration

Tests use memory storage by default for speed:

```bash
# Set before running tests
export STORAGE_BACKEND='requestbin.storage.memory.MemoryStorage'
```

For detailed test documentation, see [test/README.md](test/README.md) and [test/TEST_SUMMARY.md](test/TEST_SUMMARY.md).

## Environment Variables

### Core Configuration

- **`STORAGE_BACKEND`**: Storage backend to use
  - `requestbin.storage.memory.MemoryStorage` (default, development)
  - `requestbin.storage.redis.RedisStorage` (production)
  - `requestbin.storage.postgresql.PostgreSQLStorage` (production)

- **`PORT`**: Application port (default: `3200`)
- **`DEBUG`**: Enable debug mode (default: `True` in development)
- **`REALM`**: Environment identifier (`dev`, `prod`)
- **`FLASK_SESSION_SECRET_KEY`**: Secret key for session encryption

### PostgreSQL Configuration

- **`POSTGRES_HOST`**: PostgreSQL host (default: `localhost`)
- **`POSTGRES_PORT`**: PostgreSQL port (default: `5432`)
- **`POSTGRES_USER`**: Database user (default: `postgres`)
- **`POSTGRES_PASSWORD`**: Database password
- **`POSTGRES_DB`**: Database name (default: `requestbin`)
- **`POSTGRES_SCHEMA`**: Schema name (default: `requestbin_app`)

### Redis Configuration

- **`REDIS_URL`**: Redis connection URL (e.g., `redis://localhost:6379`)
- **`REDIS_HOST`**: Redis host (alternative to URL)
- **`REDIS_PORT`**: Redis port (default: `6379`)
- **`REDIS_PASSWORD`**: Redis authentication password

### Email Configuration (for OTP)

- **`SMTP_HOST`**: SMTP server hostname
- **`SMTP_PORT`**: SMTP server port (default: `587`)
- **`SMTP_USER`**: SMTP username
- **`SMTP_PASSWORD`**: SMTP password
- **`SMTP_FROM_EMAIL`**: Sender email address
- **`SMTP_USE_TLS`**: Enable TLS (default: `True`)

### Application Settings

- **`MAX_REQUESTS`**: Max requests per bin (default: `20` dev, `200` prod)
- **`BIN_TTL`**: Bin time-to-live in seconds (default: `345600` = 96 hours)
- **`ENABLE_CORS`**: Enable CORS support (default: `False`)
- **`CORS_ORIGINS`**: Allowed CORS origins (default: `*`)
- **`AUTO_APPROVE_DOMAINS`**: Comma-separated list of auto-approved email domains

### Example .env File

```bash
# Storage
STORAGE_BACKEND=requestbin.storage.postgresql.PostgreSQLStorage

# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=55234
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=requestbin
POSTGRES_SCHEMA=requestbin_app

# Application
PORT=3200
DEBUG=True
REALM=dev
FLASK_SESSION_SECRET_KEY=your-secret-key-here

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_USE_TLS=True

# Features
MAX_REQUESTS=100
BIN_TTL=345600
ENABLE_CORS=False
```

## Troubleshooting

### Common Issues

#### 1. WebSocket Connection Errors

**Symptom**: `Error on request: AssertionError: write() before start_response`

**Solution**: Update SocketIO async mode to `gevent`:
```python
# In requestbin/__init__.py
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')
```

Restart the application after the change.

#### 2. Database Connection Failed

**Symptom**: `psycopg2.OperationalError: could not connect to server`

**Solutions**:
- Verify PostgreSQL is running: `pg_isready -h localhost -p 5432`
- Check connection settings in `.env` file
- Ensure database exists: `psql -l | grep requestbin`
- Initialize schema: `python scripts/database/init_postgres_schema.py`

#### 3. Module Import Errors

**Symptom**: `ModuleNotFoundError: No module named 'requestbin'`

**Solutions**:
- Ensure you're in the project root directory
- Install dependencies: `pip install -r requirements.txt`
- Check Python path: `echo $PYTHONPATH`
- Activate virtual environment: `conda activate requestbin`

#### 4. Authentication Not Working

**Symptom**: Unable to login or register users

**Solutions**:
- Check auth storage backend matches main storage backend
- Verify admin user exists: Check database or run `python scripts/admin/create_admin.py`
- Clear browser cookies and try again
- Check Flask session secret key is set

#### 5. Requests Not Persisting

**Symptom**: Requests disappear after server restart

**Solutions**:
- Verify you're using PostgreSQL or Redis backend (not memory)
- Check database connection is active
- Verify schema is initialized: `psql -d requestbin -c "\\dt requestbin_app.*"`
- Check bin TTL hasn't expired

#### 6. Docker Container Issues

**Symptom**: Container fails to start or exits immediately

**Solutions**:
- Check logs: `docker logs <container-id>`
- Verify environment variables: `docker inspect <container-id>`
- Ensure ports are not in use: `netstat -an | grep 8000`
- Check docker-compose.yml configuration
- Rebuild image: `docker-compose build --no-cache`

### Getting Help

If you encounter issues not covered here:

1. **Check Documentation**: Review the comprehensive docs in the `docs/` directory
2. **Run Diagnostics**: Use `python scripts/debug/diagnose.py`
3. **Check Logs**: Review application logs for error details
4. **GitHub Issues**: Search existing issues or create a new one
5. **Community Support**: Reach out to the community for assistance

### Debug Tools

Use the provided debug scripts:

```bash
# General diagnostics
python scripts/debug/diagnose.py

# Debug bin creation
python scripts/debug/debug_bin_creation.py
```

## Contributing

### How to Contribute

We welcome contributions! Here's how you can help:

1. **Fork the Repository**
   ```bash
   git clone https://github.com/babu3009/requestbin.git
   cd requestbin
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Follow the existing code style
   - Add tests for new features
   - Update documentation as needed

4. **Run Tests**
   ```bash
   python test/run_all_tests.py
   ```

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

6. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Go to GitHub and create a PR from your branch
   - Describe your changes clearly
   - Reference any related issues

### Development Guidelines

- **Code Style**: Follow PEP 8 for Python code
- **Modular Design**: Keep code organized in appropriate packages
- **Documentation**: Update README.md and docs/ for new features
- **Testing**: Add tests for all new functionality
- **Commit Messages**: Use clear, descriptive commit messages

### Areas for Contribution

- **Features**: New storage backends, UI improvements, API enhancements
- **Testing**: Expand test coverage, add integration tests
- **Documentation**: Improve guides, add examples, create tutorials
- **Bug Fixes**: Fix reported issues, improve error handling
- **Performance**: Optimize queries, improve response times
- **Deployment**: Support for new platforms, improve Docker setup

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## Open Source Contributors

This project builds upon the work of many contributors:

### Core Contributors
- **Jeff Lindsay** ([@progrium](http://progrium.com)) - Original creator of RequestBin
- **babu3009** - PostgreSQL support, SAP BTP deployment, modern UI enhancements
- **Kinshuk Bairagi** ([@kingster](https://github.com/kingster)) - Maintenance and enhancements
- **Barry Carlyon** - Code contributions

### Libraries and Technologies Used

#### Backend
- **Flask 3.1.2** - Web framework
- **PostgreSQL** - Persistent storage backend (via psycopg2)
- **Redis** - Alternative storage backend
- **Flask-Login** - User session management
- **Flask-WTF** - Form validation and CSRF protection
- **Werkzeug** - Password hashing and security utilities
- **python-dotenv** - Environment variable management
- **psycopg2** - PostgreSQL database adapter

#### Frontend
- **Bootstrap 2.x** - UI framework
- **jQuery** - JavaScript library
- **Font Awesome** - Icon library
- **Google Code Prettify** - Syntax highlighting

#### Deployment
- **Docker** - Containerization
- **Gunicorn** - WSGI HTTP server
- **Werkzeug** - WSGI utility library

#### Development Tools
- **python-dotenv** - Environment variable management
- **Jinja2** - Template engine

### License
MIT License - See LICENSE file for details

### Special Thanks
- Original RequestBin project by Jeff Lindsay
- All contributors who have helped improve this project
- Open source community for the amazing tools and libraries

## 📚 Documentation

Comprehensive documentation is available in the [`docs/`](docs/) directory:

### Getting Started
- **[QUICKSTART.md](docs/QUICKSTART.md)** - Quick start guide for new users
- **[DOCKER_QUICK_START.md](docs/DOCKER_QUICK_START.md)** - Docker quick reference
- **[POSTGRESQL_QUICKSTART.md](docs/POSTGRESQL_QUICKSTART.md)** - PostgreSQL quick setup

### Deployment Guides
- **[DOCKER_DEPLOYMENT.md](docs/DOCKER_DEPLOYMENT.md)** - Comprehensive Docker deployment guide
- **[SAP_BTP_DEPLOYMENT.md](docs/SAP_BTP_DEPLOYMENT.md)** - SAP Business Technology Platform deployment
- **[POSTGRESQL_DEPLOYMENT.md](docs/POSTGRESQL_DEPLOYMENT.md)** - PostgreSQL deployment guide

### Configuration & Setup
- **[POSTGRESQL_SETUP.md](docs/POSTGRESQL_SETUP.md)** - PostgreSQL database setup
- **[POSTGRES_SCHEMA.md](docs/POSTGRES_SCHEMA.md)** - Database schema documentation
- **[CONFIG_UPDATE.md](docs/CONFIG_UPDATE.md)** - Configuration management guide
- **[DOCKER_UPDATE_SUMMARY.md](docs/DOCKER_UPDATE_SUMMARY.md)** - Docker configuration updates

### Authentication & Security
- **[AUTHENTICATION.md](docs/AUTHENTICATION.md)** - Authentication system overview
- **[AUTH_IMPLEMENTATION.md](docs/AUTH_IMPLEMENTATION.md)** - Technical authentication implementation
- **[PASSWORD_MANAGEMENT.md](docs/PASSWORD_MANAGEMENT.md)** - Password management features
- **[OTP_VERIFICATION.md](docs/OTP_VERIFICATION.md)** - OTP email verification system

### Features & Updates
- **[INSPECT_VIEW_UPDATE.md](docs/INSPECT_VIEW_UPDATE.md)** - Bin inspect view documentation
- **[DATA_PERSISTENCE_FIX.md](docs/DATA_PERSISTENCE_FIX.md)** - Data persistence improvements
- **[SUCCESS.md](docs/SUCCESS.md)** - Implementation success stories

### Testing & Development
- **[TEST_RESULTS.md](docs/TEST_RESULTS.md)** - Testing results and reports
- **[TEST_INSPECT_VIEW.md](docs/TEST_INSPECT_VIEW.md)** - Inspect view testing guide

### Test Scripts
All test scripts are located in the [`test/`](test/) directory - see [test/README.md](test/README.md) for details.

### Utility Scripts
All utility scripts are organized in the [`scripts/`](scripts/) directory:

#### Admin Tools (`scripts/admin/`)
- **create_admin.py** - Create admin user via Python
- **create_admin.ps1** - Create admin user via PowerShell
- **change_password.py** - Change user password directly in database
- **generate_password_sql.py** - Generate SQL for password changes

#### Database Scripts (`scripts/database/`)
- **schema.sql** - Complete PostgreSQL database schema
- **change_admin_password.sql** - SQL template for admin password change
- **init_postgres_schema.py** - Initialize PostgreSQL schema and admin user
- **init_postgres_schema.ps1** - PowerShell wrapper for schema initialization

#### Deployment Scripts (`scripts/deployment/`)
- **run_local_memory.ps1** - Run locally with memory backend
- **run_local_postgres.ps1** - Run locally with PostgreSQL backend
- **run_postgres.bat** - Batch script to run with PostgreSQL
- **switch_backend.ps1** - Switch between storage backends (PowerShell)
- **switch_backend.sh** - Switch between storage backends (Bash)

#### Debug Tools (`scripts/debug/`)
- **debug_bin_creation.py** - Debug bin creation issues
- **diagnose.py** - Diagnostic tool for troubleshooting

### Configuration Files
Deployment configuration files are located in the [`config/`](config/) directory:
- **manifest.yml** - Cloud Foundry manifest (Redis backend)
- **manifest-postgresql.yml** - Cloud Foundry manifest (PostgreSQL backend)
- **app.json** - Heroku configuration
