from dotenv import load_dotenv
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import jwt
import os
import uvicorn

# Custom modules
from utils.schemas import Token, UserSignup
from utils.tmp_db import users_db # Temp test db, will be replaced with postgresql
from utils.password_manager import PwdManager
load_dotenv()



app = FastAPI()
pwd_manager = PwdManager()



@app.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    auth = pwd_manager.validate_user(form_data.username, form_data.password)

    if auth:
        access_token_expires = timedelta(minutes=15)
        access_token = pwd_manager.create_access_token(data = {"sub": form_data.username}, expires_delta=access_token_expires)

        return Token(access_token=access_token, token_type="bearer")
    
    return "Success"

@app.post("/signup")
async def signup(user_info: UserSignup):
    pwd_manager.sign_up(user=user_info)

    return {"msg": "Success!!!"}




if __name__ == "__main__":
    uvicorn.run(app)