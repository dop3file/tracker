import datetime

import bcrypt
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

from .database import engine

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    login = Column(String)
    email = Column(String)
    password = Column(Text)
    creation_date = Column(DateTime, server_default=func.now())

    def verify_password(self, password):
        pwhash = bcrypt.hashpw(password, self.password)
        return self.password == pwhash

class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, autoincrement=True, primary_key=True)
    genius_id = Column(Integer)
    parse_date = Column(DateTime, server_default=func.now())
    json = Column(Text)


def create_db():
    Base.metadata.create_all(bind=engine)






