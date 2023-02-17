from fastapi import FastAPI, APIRouter, status, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from models.schemas import SearchQuery
from models.db_models import User
from models.database import get_db

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/')
async def get_search_query(search_query: SearchQuery):
    return search_query
