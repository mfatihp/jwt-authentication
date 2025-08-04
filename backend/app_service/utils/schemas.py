from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String




# Database Schemas
Base = declarative_base()

class UserApp(Base):
    __tablename__ = "users_app"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)

# API Schemas
class Payload(BaseModel):
    access_token: str
    msg: str


class NewUser(BaseModel):
    username: str
    email: str
