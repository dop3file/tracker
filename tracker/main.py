import asyncio

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
        get_artist_ids_tasks = [
            genius.get_artist_id(search_query.artist_name),
            spotify.get_artist_id(search_query.artist_name)
        ]
        artist_ids = await asyncio.gather(*get_artist_ids_tasks)
        tasks = [
            genius.get_artist(artist_ids[0]),
            spotify.get_artist_top_tracks(artist_ids[1])
        ]
        stats = await asyncio.gather(*tasks)
        all_stats = AllStats(
            genius=stats[0],
            spotify_tracks=stats[1]
        )
    except exceptions.SearchInvalidException as error_msg:
        return {"error": str(error_msg)}
    return all_stats.json()
