import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db = declarative_base()
engine = create_engine('DATABASE_URL',connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
session = Session()