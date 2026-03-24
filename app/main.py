from fastapi import FastAPI

from app.db import lifespan
from app.router import router

app = FastAPI(lifespan=lifespan, title="Sandbox")

app.include_router(router=router)