from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from app.core.database import engine

from app.api.users import router as user_router
from app.api.products import router as product_router

from app.models.user import User
from app.models.product import Product




@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    yield

app  = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(product_router)

@app.get("/")
def root():
    return {"message":"Inventory Api"}