import asyncio

from fastapi import FastAPI, APIRouter, status, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from schemas.schemas import SearchQuery
from models.db_models import User
from models.database import get_db
from controllers.services.genius import Genius

import config


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins,
)

genius = Genius(config.GENIUS_ACCESS_TOKEN)

@app.post('/')
async def get_search_query(search_query: SearchQuery):
    artist_id = await genius.get_artist_id(search_query.artist_name)
    artist = await genius.get_artist(artist_id)
    return artist.json()
