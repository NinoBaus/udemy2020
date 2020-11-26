from db import db
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

class All_ads(db):
    __tablename__ = "all_ads"
    id = Column(Integer(), primary_key=True)
    name = Column(String(80))
    price = Column(Integer())
    picture = Column(String())
    expire = Column(String())
    link = Column(String())
    search = Column(String())
    show = Column(Integer(), default=1)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    user_id = Column(Integer())