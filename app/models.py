from datetime import datetime, UTC

from sqlalchemy import Integer, String, DateTime, Index, ForeignKey, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class ApiCounter(Base):
    __tablename__ = "api_counter"
    endpoint: Mapped[str] = mapped_column(String, primary_key=True)
    value: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC), nullable=False)


Index("ix_api_call_log_endpoint_created_at", ApiCounter.endpoint, ApiCounter.created_at)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user")


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(32), nullable=False)
    body: Mapped[str] = mapped_column(String(1024), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    user: Mapped["User"] = relationship("User", back_populates="posts")



