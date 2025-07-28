from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from passlib.context import CryptContext

from sqlalchemy import create_engine, insert, select
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values
from contextlib import contextmanager

from .schemas import User, UserAuth, UserApp, Token

import os
import jwt



class PwdManager:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

        self.SECRET_KEY = os.environ.get("SECRET_KEY")
        self.ALGORITHM = os.environ.get("ALGORITHM")

        env_info = dotenv_values(".env")

        auth_db_url = f"postgresql+psycopg2://{env_info["AUTH_USER"]}:{env_info["AUTH_PWD"]}@{env_info["AUTH_HOST"]}:{env_info["AUTH_PORT"]}/{env_info["AUTH_DB"]}"
        app_db_url = f"postgresql+psycopg2://{env_info["APP_USER"]}:{env_info["APP_PWD"]}@{env_info["APP_HOST"]}:{env_info["APP_PORT"]}/{env_info["APP_DB"]}"

        self.auth_engine = create_engine(auth_db_url)
        self.app_engine = create_engine(app_db_url)
    

    def sign_up(self, user: User):
        with self.db_session_scope(self.auth_engine) as session_auth, self.db_session_scope(self.app_engine) as session_app:
            db_check_username = session_auth.execute(select(UserAuth).where(UserAuth.username == user.username))
            db_check_email = session_auth.execute(select(UserAuth).where(UserAuth.email == user.email))

            # Check db for duplicate username or email
            if (len(db_check_email.all()) <= 0) and (len(db_check_username.all()) <= 0):
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
                
                # Return initial token
                expire = timedelta(minutes=15)
                token = self.create_access_token(data={"sub": user.username}, expires_delta=expire)

                return Token(access_token=token, token_type="bearer") 
            
            else:
                print("Email or username already in use")


    def login(self, user: User):
        user_flag = self.validate_user(user_fv=user)

        if user_flag:
            expire = timedelta(minutes=15)
            token = self.create_access_token(data={"sub": user.username}, expires_delta=expire)

            return Token(access_token=token, token_type="bearer")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Incorrect username or password",
                                headers={"WWW-Authenticate": "Bearer"})


    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    
    def validate_user(self, user_fv: User):
        # Query hashed password for user
        with self.db_session_scope(self.auth_engine) as session_auth:
            db_user_info = session_auth.execute(select(UserAuth).where(UserAuth.username == user_fv.username)).scalars().first()

            hpass = db_user_info.hpass
        
        # hashed_pwd = self.get_password_hash(user_fv.password)

        return self.pwd_context.verify(user_fv.password, hpass)
    
    
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
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