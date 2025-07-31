# JWT Authentication Microservice

A distributed authentication and authorization system built using FastAPI and JWT tokens. This project includes an `auth_service` for user management and token handling, and an `app_service` that uses JWT validation to authorize access to protected resources. Designed with modularity, security, and Docker-based deployment in mind.

<br/>

## 🧱 Architecture

- **auth_service**: Handles user registration, login, token creation, refresh token handling.
- **app_service**: Validates JWT access tokens for protected endpoints.
- **auth_db**: Used by auth service to store user data, email and hashed password.
- **app_db**: Used by both services to store user data and email.


<br/>

## ✨ Features





<br/>

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/mfatihp/["reponame"]
cd ["repo name"]
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
- SQLAlchemy
- Docker & Docker Compose
- JWT (PyJWT)
- Passlib


<br/>

