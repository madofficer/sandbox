from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import User, Post, ApiCounter
from app.tools import timer


async def log_api_call(db: AsyncSession, endpoint: str) -> ApiCounter:
    row = ApiCounter(endpoint=endpoint)
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row


async def get_api_call_count(db: AsyncSession, endpoint: str) -> int:
    statement = select(func.count(ApiCounter.id)).where(ApiCounter.endpoint == endpoint)
    result = await db.scalar(statement)
    return result or 0


async def increment(db: AsyncSession, endpoint: str) -> int:
    sql = text("""
               INSERT INTO api_counter (endpoint, value, created_at)
               VALUES (:endpoint, 1, NOW())
               ON CONFLICT (endpoint)
                   DO UPDATE SET value = api_counter.value + 1
               RETURNING value
               """)
    result = await db.execute(sql, {"endpoint": endpoint})
    new_val = result.scalar_one()
    await db.commit()
    return new_val


async def create_user(db: AsyncSession, name: str) -> User:
    user = User(name=name)
    db.add(user)

    await db.commit()
    await db.refresh(user)
    return user


async def create_post(db: AsyncSession, user_id: int, title: str, body: str) -> Post:
    post = Post(user_id=user_id, title=title, body=body)

    db.add(post)
    await db.commit()
    await db.refresh(post)

    return post


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    return await db.get(User, user_id)


# n + 1 problem
@timer
async def n_plus_one_bad(db: AsyncSession) -> list[dict[str, str | int]]:
    result = []

    users = (await db.execute(select(User).order_by(User.id))).scalars().all()
    for user in users:
        posts = (await db.execute(select(Post).where(Post.user_id == user.id))).scalars().all()
        result.append({"user": user.name, "posts": [post.title for post in posts]})
    return result


@timer
async def n_plus_one_good(db: AsyncSession) -> list[dict[str, str]]:
    statement = select(User).options(selectinload(User.posts)).order_by(User.id)
    users = (await db.execute(statement)).scalars().all()
    result = []

    for user in users:
        result.append({"user": user.name, "posts": [post.title for post in user.posts]})

    return result
