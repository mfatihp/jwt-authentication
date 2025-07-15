from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer



router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# DB
# Classes maybe
users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

