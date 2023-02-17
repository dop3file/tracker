import datetime

import bcrypt
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from models.database import base as Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    login = Column(String)
    email = Column(String)
    password = Column(Text)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)

    def verify_password(self, password):
        pwhash = bcrypt.hashpw(password, self.password)
        return self.password == pwhash


