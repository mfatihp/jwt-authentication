# JWT Authentication Microservice

A distributed authentication and authorization system built using FastAPI and JWT tokens. This project includes an `auth_service` for user management and token handling, and an `app_service` that uses JWT validation to authorize access to protected resources. Designed with modularity, security, and Docker-based deployment in mind.

<br/>

## 🧱 Architecture

- **auth_service**: Handles user registration, login, token creation, refresh token handling.
- **app_service**: Validates JWT access tokens for protected endpoints.
- **auth_db**: Used by auth service to store user data, email and hashed password.
- **app_db**: Used by both services to store user data and email.

<br/>

<p align="center">
<img src="docs/jwt_system.drawio.svg" alt="JWT Auth Flow" width="800"/>
</p>

<br/>

## ✨ Features

### 🧩 Modular Microservice Architecture

- auth_service: Handles user registration, login, and JWT generation

- app_service: Consumes tokens, validates user sessions, and performs app-specific logic

### 🔐 Secure JWT Authentication

- Token creation with expiration and refresh support

- Protected endpoints with token verification

### 🔄 User Sync Mechanism

- Automatically syncs authenticated user data between auth_service and app_service

### 🛢️ Separate Databases

- auth_db for authentication credentials

- app_db for application-specific user data

### 🐳 Dockerized Setup

- Fully containerized with Docker Compose for easy deployment




<br/>

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/mfatihp/jwt-authentication-microservice.git
cd jwt-authentication-microservice
```

### 2. Create environment files

Create your `SECRET_KEY` for password encoding.

```bash
openssl rand -hex 32
```
<br/>

The list of `.env` files' locations.
- app_service

```bash
cd backend/app_service
touch .env
```

```env
SECRET_KEY="your secret key"
ALGORITHM="HS256"

APP_HOST ="app_db"
APP_PORT ="5432"
APP_USER="DB username"
APP_PWD="DB password"
APP_DB="app_db"
```

- app_db

```bash
cd backend/app_db
touch .env
```

```env
POSTGRES_USER="DB username"
POSTGRES_PASSWORD="DB password"
POSTGRES_DB="app_db"
```

- auth_service

```bash
cd backend/auth_service
touch .env
```

```env
SECRET_KEY="your secret key"
ALGORITHM="HS256"

APP_SERVICE_HOST="http://app_service:8001/sync_user"

AUTH_HOST ="auth_db"
AUTH_PORT ="5432"
AUTH_USER="DB username"
AUTH_PWD="DB password"
AUTH_DB="auth_db"
```

### Run with Docker Compose

```bash
docker compose up --build
```



<br/>

## 🧪 Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL
- Docker
- JWT 


<br/>

