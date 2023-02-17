from fastapi import FastAPI, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.schemas import SearchQuery
from models.db_models import User


app = FastAPI()


@app.get('/query')
async def get_notes(session: AsyncSession, search_query: SearchQuery):
    result = User()
    session.add(result)
    session.rollback()
    return 1
