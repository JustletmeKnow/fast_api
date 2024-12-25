from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from Schemas import *


monitor_router = APIRouter(prefix="/monitors", tags=["Monitors"])

engine = create_async_engine('sqlite+aiosqlite:///monitors.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


@monitor_router.get("", summary="All monitors")
async def get_monitors(session: SessionDep):
    query = select(MonitorModel)
    result = await session.execute(query)
    return result.scalars().all()


@monitor_router.get("/{monitor_id}", summary="Get a particular monitor")
async def get_monitor(monitor_id: int, session: SessionDep):
    query = select(MonitorModel).where(MonitorModel.id == monitor_id)
    if query == monitor_id:
        result = await session.execute(query)
        return result.scalars().all()
    raise HTTPException(status_code=404, detail="Monitor not found")


@monitor_router.post("", summary="Create a new monitor")
async def create_monitor(data: Annotated[MonitorAddSchema, Depends()], session: SessionDep):
    new_monitor = MonitorModel(
        title = data.title,
        model = data.model,
        description = data.description,
    )
    session.add(new_monitor)
    await session.commit()
    return {"success": True}