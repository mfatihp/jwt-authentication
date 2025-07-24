from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import dotenv_values
from contextlib import contextmanager

from .schemas import UserSignup, UserAuth, UserApp

import os
import jwt



# TODO: Create hash function
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
        # TODO: Check db for duplicate username or email
        with self.db_session_scope(self.auth_engine) as session_auth, self.db_session_scope(self.app_engine) as session_app:

            # Insert into auth db
            session_auth.execute(
                insert(UserAuth),
                [
                    {"username": user.username, "email": user.email, "hpass": self.get_password_hash(user.password)}
                ])

            # Insert into app db
            session_app.execute(
                insert(UserApp),
                [
                    {"username": user.username, "email": user.email}
                ])



    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    
    def validate_user(self, username, password, db_session):
        # TODO: Query hashed password for user
        pass
    
    
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None): # data : {"sub": user.username} 
        to_encode = data.copy()
        expire = datetime.now(ZoneInfo("Europe/Istanbul")) + expires_delta
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