from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.db import get_session
from app.schemas import UserCreate

router = APIRouter()


# api for counting itself calls
@router.get("/ping", response_model=schemas.PingCountResponse, status_code=status.HTTP_200_OK)
async def ping(db: Annotated[get_session, Depends()]):
    new_val = await crud.increment(db, "/ping")
    return {"message": "pong", "count": new_val}


@router.post("/creat/user", status_code=status.HTTP_201_CREATED)
async def create_user(db: Annotated[get_session, Depends()], name: str):
    user = await crud.create_user(db, name)
    return {"user_id": user.id, "message": "created"}


@router.post("/creat/post", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(db: Annotated[get_session, Depends()], user_id: int, title: str, body: str):
    post = await crud.create_post(db, user_id=user_id, title=title, body=body)

    return {"id": post.id, "user_id": post.user_id, "title": post.title, "body": post.body}


@router.get("/get/user_posts_bad", status_code=status.HTTP_200_OK)
async def get_user_posts_bad(db: Annotated[get_session, Depends()]):
    return await crud.n_plus_one_bad(db)


@router.get("/get/user_posts_good", status_code=status.HTTP_200_OK)
async def get_user_posts_good(db: Annotated[get_session, Depends()]):
    return await crud.n_plus_one_good(db)
