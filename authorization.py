from fastapi import FastAPI, HTTPException
from authx import AuthX, AuthXConfig



app = FastAPI()

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)



@app.get("/protected")
async def protected():
    ...