from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

import os
import jwt


# TODO: Create DB session, hash function
class PwdManager:
    def __init__(self):

        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

        self.SECRET_KEY = os.environ.get("SECRET_KEY")
        self.ALGORITHM = os.environ.get("ALGORITHM")


    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    
    def validate_user(self, username, password, db_session):
        # TODO: Query hashed password for user
        matched = True
        return matched
    
    
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None): # data : {"sub": user.username} 
        to_encode = data.copy()
        expire = datetime.now(ZoneInfo("Europe/Istanbul")) + expires_delta
        print(datetime.now(ZoneInfo("Europe/Istanbul")))
        print(expire)
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt