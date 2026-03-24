from typing import Annotated

from fastapi import APIRouter, Depends

from app import crud
from app.db import get_session

router = APIRouter()


@router.get("/ping")
async def ping(db: Annotated[get_session, Depends()]):
    new_val = await crud.increment(db, "/ping")
    return {"message": "pong", "count": new_val}