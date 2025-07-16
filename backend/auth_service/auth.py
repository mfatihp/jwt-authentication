from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

# Custom modules
from utils.tokens import Token
from utils.tmp_db import users_db # Temp test db, will be replaced with postgresql


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def validate_user(username, password):
    # Query user hashed password
    if username in users_db:
        user_dict = users_db[username]
        hashed_pwd = user_dict["hashed_password"]

        # Verify password
        matched = pwd_context.verify(password, hashed_pwd)


def create_access_token(data: dict, expires_delta: timedelta | None = None): # data : {"sub": user.username} 

    return None


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    auth = validate_user(form_data.username, form_data.password)

    if auth:
        access_token_expires = timedelta(minutes=15)
        access_token = create_access_token()

        return Token(access_token=access_token, token_type="bearer")