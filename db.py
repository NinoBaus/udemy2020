import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
# DATABASE_URL = os.environ['DATABASE_URL']

db = declarative_base()
# engine = create_engine(DATABASE_URL)
engine = create_engine(os.environ.get('DATABAS_URL','sqlite:///database.db'),connect_args={"check_same_thread": False})

# session_factory = sessionmaker(bind=engine)
# Session = scoped_session(session_factory)
# session = Session()

session = scoped_session(
    sessionmaker(
        autoflush=True,
        autocommit=False,
        bind=engine
    )
)