from fastapi import FastAPI, HTTPException, Depends, Response
import uvicorn
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import Annotated

from router_monitors import monitor_router
from router_user import user_router
from authorization import *
from Schemas import *


app = FastAPI()
app.include_router(monitor_router)
app.include_router(user_router)

engine = create_async_engine('sqlite+aiosqlite:///monitors.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]

@app.post("/login", tags=["auth"])
async def login(creds:UserLoginSchema, response:Response):
    if creds.username == "test" and creds.password == "test":
        token = security.create_access_token(uid="12345")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Incorrect username or password")


@app.get("/protected", tags=["auth"], dependencies=[Depends(security.access_token_required)])
def protected():
    return {"data": "Secret message"}
    raise HTTPException(status_code=403, detail="Log in for this action")



@app.post("/setup_db", tags=["Database"], summary="Setup db")
async def setup_monitors_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"success": True}





if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)