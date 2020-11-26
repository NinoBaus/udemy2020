from db import db
from sqlalchemy import Column, Integer, String

class User(db):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False, unique=True)
    password = Column(String(80))