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


@app.post("/signin")
async def signin(user: SigninUser):
    try:
        userData = userDBC.getUser(**user.model_dump())
        peer = vpnManage.getPeer(uuid=userData[0])
        peer = base64.b64encode(peer.encode()).decode()
        return {"message": "Success", "peer": peer}
    except Exception as e:
        return {"message": str(e)}


@app.post("/password-change")
async def password_change(user: PasswordChange):
    try:
        userDBC.updatePassword(**user.model_dump())
        return {"message": "Success"}
    except Exception as e:
        return {"message": str(e)}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
