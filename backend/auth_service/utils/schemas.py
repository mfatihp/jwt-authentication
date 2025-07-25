from pydantic import BaseModel, EmailStr

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String



# Database Schemas
Base = declarative_base()

class UserAuth(Base):
    __tablename__ = "users_auth"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hpass = Column(String, nullable=False)


class UserApp(Base):
    __tablename__ = "users_app"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)


# FastAPI Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    email: EmailStr
    password: str
