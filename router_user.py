from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from Schemas import *


user_router = APIRouter(prefix="/users", tags=["Users"])


engine = create_async_engine('sqlite+aiosqlite:///monitors.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

@user_router.get("", summary="All users")
async def get_users(session: SessionDep) -> UserSchema:
    query = select(UserModel)
    result = await session.execute(query)
    return result.scalars().all()


@user_router.get("/{user_id}", summary="Get a particular user")
async def get_user(user_id: int, session: SessionDep):
    with engine.connect() as conn:
        users_id = conn.get(UserModel, user_id)

        if users_id == user_id:
            result = await conn.execute(users_id)
            return result.scalars().all()
        raise HTTPException(status_code=404, detail="User not found")


@user_router.post("", summary="Create a new user")
async def create_user(data: Annotated[UserAddSchema, Depends()], session: SessionDep) -> UserAddSchema:
    new_user = UserModel(
        email=data.email,
        username=data.username,
        password=data.password,
    )
    session.add(new_user)
    await session.commit()
    return {"success": True}