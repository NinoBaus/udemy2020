from db import db
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:')

class User(db):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False, unique=True)
    password = Column(String(80))