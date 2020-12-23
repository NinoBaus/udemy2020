import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
DATABASE_URL = os.environ['DATABASE_URL']

db = declarative_base()
# engine = create_engine(os.environ.get('DATABAS_URL','sqlite:///database.db'),connect_args={"check_same_thread": False})
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()