from fastapi import FastAPI
from fastapi import HTTPException, status

import jwt


app = FastAPI()

SECRET_KEY = ""
ALGORITHM = ""

def check_token_validity(token:str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])



@app.get("/awesome_app")
async def ai_function():
    valid = check_token_validity()

    if valid:
        # TODO: Add a real function here
        pass
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})