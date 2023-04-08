from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from config import DATABASE_URL


database_url = URL.create(
    drivername="postgresql",
    username="postgres",
    database="postgres",
    host="localhost",
    password="pgpwd4habr"
)
engine = create_engine(
    database_url, echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
