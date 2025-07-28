from fastapi import FastAPI
from fastapi import HTTPException, status
from dotenv import load_dotenv
from pydantic import BaseModel
from datetime import datetime
from zoneinfo import ZoneInfo

import os
import jwt

load_dotenv()

app = FastAPI()

class Payload(BaseModel):
    access_token: str
    msg: str

datetime.now(ZoneInfo("Europe/Istanbul"))


def check_token_validity(token:str):
    payload = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=[os.environ.get("ALGORITHM")])
    exp_timestamp = payload.get("exp")
    exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=ZoneInfo("Europe/Istanbul"))
    
    # Check expiration date 
    if exp_datetime > datetime.now(ZoneInfo("Europe/Istanbul")):
        return True
    else: 
        return False



@app.get("/awesome_app")
async def ai_function(data: Payload):
    valid = check_token_validity(token=data.access_token)

    if valid:
        return {"msg": "You accessed!!!"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})