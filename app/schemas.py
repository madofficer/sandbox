from pydantic import BaseModel, ConfigDict


class PingCountResponse(BaseModel):
    endpoint: str
    count: int


class UserCreate(BaseModel):
    name: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class PostCreate(BaseModel):
    title: str
    body: str


class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    body: str
    user_id: int