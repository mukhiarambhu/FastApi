from sqlmodel import select
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from .database import SessionDep, create_db_and_tables
from .models import Product

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    create_db_and_tables()
    yield
    print("Shutting down...")    
app = FastAPI(lifespan=lifespan)

    