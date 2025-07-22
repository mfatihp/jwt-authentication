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
from utils.tokens import Token
from utils.tmp_db import users_db # Temp test db, will be replaced with postgresql

load_dotenv()



app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")



def get_password_hash(password):
    return pwd_context.hash(password)



def validate_user(username, password):
    # Query user hashed password
    if username in users_db:
        user_dict = users_db[username]
        hashed_pwd = user_dict["hashed_password"]

        # Verify password
        matched = pwd_context.verify(password, hashed_pwd)
    else: 
        matched = False
    return matched




def create_access_token(data: dict, expires_delta: timedelta | None = None): # data : {"sub": user.username} 
    to_encode = data.copy()
    expire = datetime.now(ZoneInfo("Europe/Istanbul")) + expires_delta
    print(datetime.now(ZoneInfo("Europe/Istanbul")))
    print(expire)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




@app.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    auth = validate_user(form_data.username, form_data.password)

    if auth:
        access_token_expires = timedelta(minutes=15)
        access_token = create_access_token(data = {"sub": form_data.username}, expires_delta=access_token_expires)

        return Token(access_token=access_token, token_type="bearer")
    
    return "Success"

@app.post("/signup")
async def signup(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # TODO: Create and save hashed password into auth db

    # TODO: Save the user info into ai service db

    pass




if __name__ == "__main__":
    uvicorn.run(app)