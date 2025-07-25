from dotenv import load_dotenv
from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
import uvicorn

# Custom modules
from utils.schemas import User
from utils.password_manager import PwdManager
load_dotenv()



app = FastAPI()
pwd_manager = PwdManager()



@app.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return pwd_manager.login(user=form_data)


@app.post("/signup")
async def signup(user_info: User):
    pwd_manager.sign_up(user=user_info)

    return {"msg": "Success!!!"}




if __name__ == "__main__":
    uvicorn.run(app)