from dotenv import dotenv_values
from sqlalchemy import create_engine, insert, select
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from .schemas import UserApp, NewUser



class SignupManager:
    def __init__(self):
        env_info = dotenv_values(".env")
        app_db_url = f"postgresql+psycopg2://{env_info["APP_USER"]}:{env_info["APP_PWD"]}@{env_info["APP_HOST"]}:{env_info["APP_PORT"]}/{env_info["APP_DB"]}"

        self.db_engine = create_engine(app_db_url)
    
    
    def sign_up(self, user_info: NewUser):
        with self.db_session_scope(self.db_engine) as session_app:
            session_app.execute(
                insert(UserApp),
                    [
                        {"username": user_info.username, "email": user_info.email}
                    ])


    def test_db(self, user_info: str):
        with self.db_session_scope(self.db_engine) as session_app:
            stmt = select(UserApp).where(UserApp.username == user_info)

            result = session_app.scalars(stmt).one()
        
            return result.username


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