from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import dotenv_values
from contextlib import contextmanager

from schemas import UserSignup

import os
import jwt





# TODO: Create DB session, hash function
class PwdManager:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

        self.SECRET_KEY = os.environ.get("SECRET_KEY")
        self.ALGORITHM = os.environ.get("ALGORITHM")

        env_info = dotenv_values(".env")

        auth_db_url = f"postgresql+psycopg2://{env_info["AUTH_USER"]}:{env_info["AUTH_PWD"]}@{env_info["AUTH_HOST"]}:{env_info["AUTH_PORT"]}/{env_info["AUTH_DB"]}"
        app_db_url = f"postgresql+psycopg2://{env_info["APP_USER"]}:{env_info["APP_PWD"]}@{env_info["APP_HOST"]}:{env_info["APP_PORT"]}/{env_info["APP_DB"]}"

        self.auth_engine = create_engine(auth_db_url)
        self.app_engine = create_engine(app_db_url)
    

    def sign_up(self, user:UserSignup):
        with self.db_session_scope(self.auth_engine) as session_auth, self.db_session_scope(self.app_engine) as session_app:

            # TODO: Insert into auth db

            # TODO: Insert into app db

            pass



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
    
    @contextmanager
    def db_session_scope(self, engine):
        SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        session = SessionLocal()
        
        try:
            yield session
            session.commit()
        
        except Exception:
            session.rollback()
            raise
        
        finally:
            session.close()