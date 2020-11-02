from db import db
from datetime import datetime

class All_ads(db.Model):
    __tablename__ = "all_ads"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    picture = db.Column(db.String)
    expire = db.Column(db.String)
    link = db.Column(db.String)
    search = db.Column(db.String)
    show = db.Column(db.Boolean, default=True)
    # created_at = db.Column(db.DateTime, default=datetime.now)


'''
    def __init__(self, name, price, picture, expire, link, search):
        self.name = name
        self.price = price
        self.picture = picture
        self.expire = expire
        self.link = link
        self.search = search

'''