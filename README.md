# RequestBin

RequestBin gives you a URL that will collect requests made to it and let you inspect them in a human-friendly way. Use RequestBin to see what your HTTP client is sending or to inspect and debug webhook requests.

## Features

- **Split-Panel Outlook-Style Interface**: Modern UX with tabular request list and detailed view
- **Real-time Request Inspection**: View headers, query parameters, form data, and raw body
- **Multiple Storage Backends**: Memory, Redis, or PostgreSQL
- **Authentication System**: User registration, login, and OTP verification
- **Data Persistence**: Configurable bin TTL (default: 96 hours)
- **RESTful API**: Programmatic bin and request management
- **Docker Support**: Easy deployment with Docker and Docker Compose
- **SAP BTP Ready**: Optimized for SAP Business Technology Platform

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
- Manage your bins
- See account statistics

#### Admin Panel (`/admin/users`) - Admin Only
- User management
- System statistics
- Application monitoring

### How to Use

1. **Create a Bin**:
   ```bash
   # Via Web UI: Visit http://localhost:4000 and click "Create a RequestBin"
   # Via API: 
   curl -X POST http://localhost:4000/api/v1/bins
   ```

2. **Send Requests to Your Bin**:
   ```bash
   curl -X POST http://localhost:4000/<your-bin-id> \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'
   ```

3. **Inspect Requests**:
   - Open `http://localhost:4000/<your-bin-id>?inspect` in your browser
   - Click any request in the left panel to view full details
   - Use the refresh button to update the list
   - Copy cURL commands for replaying requests

4. **Share Your Bin**:
   - Share the bin URL with your webhook provider
   - Configure your application to send requests to the bin
   - Debug and test HTTP integrations in real-time

## Quick Start with Docker

### Simple Start (Redis Backend)

Launch your own RequestBin instance with Docker:

```bash
docker run -p "8000:8000" babu3009/requestbin:latest
```

The pre-build image is available in the Docker central repository as [babu3009/requestbin](https://hub.docker.com/r/babu3009/requestbin).

### Docker Compose with Storage Options

Run RequestBin with persistent storage using Docker Compose. You can choose between **Redis** (default) or **PostgreSQL** storage backends.

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
- **[DOCKER_QUICK_START.md](DOCKER_QUICK_START.md)** - Quick reference and commands
- **[DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)** - Comprehensive deployment guide  

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

For detailed deployment instructions, see [SAP_BTP_DEPLOYMENT.md](SAP_BTP_DEPLOYMENT.md).

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

This will run the automated build of the RequestBin image and then pull down the trusted `redis` image and run with a mounted volume as a linked container to the RequestBin app. RequestBin would be exposed on the port `8000`.  


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

```
go install github.com/mattn/goreman@latest
goreman start
# now you can keep editing, it would auto reflect.
```

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
- **Flask-Bcrypt** - Password hashing
- **itsdangerous** - Secure token generation for OTP

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
