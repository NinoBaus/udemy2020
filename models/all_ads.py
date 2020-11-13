from db import db
from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime
from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:')

class All_ads(db):
    __tablename__ = "all_ads"

    id = Column(Integer(), primary_key=True)
    name = Column(String(80))
    price = Column(Integer())
    picture = Column(String())
    expire = Column(String())
    link = Column(String())
    search = Column(String())
    show = Column(Boolean(), default=True)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    user_id = Column(Integer())

    # user = relationship("User", backref=backref('user', order_by=id))


'''
    def __init__(self, name, price, picture, expire, link, search):
        self.name = name
        self.price = price
        self.picture = picture
        self.expire = expire
        self.link = link
        self.search = search

'''