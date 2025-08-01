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

### 2. Run with Docker Compose

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

