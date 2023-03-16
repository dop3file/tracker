import asyncio

import uvicorn
from fastapi import FastAPI, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from schemas.schemas import SearchQuery, UserAuth
from schemas.service_schemas import AllStats
from models.db_models import User
from models.database import get_db

from controllers.services.genius import GeniusAPI, GeniusParser
from controllers.services.spotify import SpotifyAPI

import config
import exceptions
from controllers.artist import ArtistController
from models.database import SessionLocal
from models.db_models import User
from logger import Logger

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
genius_parser = GeniusParser()
spotify = SpotifyAPI(config.SPOTIFY_ACCESS_TOKEN)
artist_controller = ArtistController(
    db=SessionLocal(),
    spotify=spotify,
    genius=genius,
    genius_parser=genius_parser
)
logger = Logger()


@app.post('/')
async def get_search_query(search_query: SearchQuery, db = Depends(get_db)):
    try:
        artist = await artist_controller. get_artist(search_query.artist_name)
    except exceptions.SearchInvalidException as error_msg:
        return {"error": str(error_msg)}
    except Exception as error_msg:
        logger.log_info(error_msg)
        return {"error": "Server error"}
    return artist.json()

@app.post('/login')
async def login(user_auth: UserAuth):
    ...

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)