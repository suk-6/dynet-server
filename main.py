import base64
import uvicorn
from models import *
from db import userDB
from manage import Manage
from fastapi import FastAPI

app = FastAPI()
userDBC = userDB()
vpnManage = Manage()


@app.get("/")
async def root():
    return {"message": "Welcome to the DY-NET!"}


@app.post("/api/user/signup")
async def signup(user: SignupUser):
    userData = userDBC.insert(**user.model_dump())
    vpnManage.addPeer(email=userData[1])
    return {"message": "Success"}


@app.post("/api/user/signin")
async def signin(user: SigninUser):
    userData = userDBC.getUser(**user.model_dump())
    peer = vpnManage.getPeer(email=userData[1])
    peer = base64.b64encode(peer.encode()).decode()
    return {"message": "Success", "peer": peer}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
