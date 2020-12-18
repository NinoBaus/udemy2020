import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db = declarative_base()
engine = create_engine(os.environ.get('postgres://bbovcqkgayqdlh:416b864bee156855f21336a8056f97af781eec03180524674f0396ea9f981f28@ec2-54-75-229-28.eu-west-1.compute.amazonaws.com:5432/d5u116ov25cmpr','sqlite:///database2.db'),connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
session = Session()