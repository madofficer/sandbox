from typing import Annotated

from fastapi import APIRouter, Depends, status

from app import crud, schemas
from app.db import get_session
from app.schemas import UserCreate

router = APIRouter()


# api for counting itself calls
@router.get("/ping", response_model=schemas.PingCountResponse, status_code=status.HTTP_200_OK)
async def ping(db: Annotated[get_session, Depends()]):
    new_val = await crud.increment(db, "/ping")
    return {"message": "pong", "count": new_val}


@router.post("/user/creat", status_code=status.HTTP_201_CREATED)
async def create_user(db: Annotated[get_session, Depends()], name: str):
    user = await crud.create_user(db, name)
    return {"user_id": user.id, "message": "created"}

# @router.post("/post/creat", status_code=status.HTTP_201_CREATED)
# async def create_post(db: Annotated[get_session, Depends()]):
