from fastapi import FastAPI
import sec.auth



app = FastAPI()
app.include_router(sec.auth)


@app.get("/")
def hello():
    return {"msg": "Hello World"}