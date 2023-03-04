import asyncio

import uvicorn
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from schemas.schemas import SearchQuery
from schemas.service_schemas import AllStats
from models.db_models import User
from models.database import get_db

from controllers.services.genius import GeniusAPI
from controllers.services.spotify import SpotifyAPI

import config
import exceptions
from controllers.artist import get_artist


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins,
)

genius = GeniusAPI(config.GENIUS_ACCESS_TOKEN)
spotify = SpotifyAPI(config.SPOTIFY_ACCESS_TOKEN)

@app.post('/')
async def get_search_query(search_query: SearchQuery):
    try:
        artist = await get_artist(genius, spotify, search_query.artist_name)
    except exceptions.SearchInvalidException as error_msg:
        return {"error": str(error_msg)}
    return artist.json()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)