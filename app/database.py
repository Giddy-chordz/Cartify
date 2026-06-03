#====POSTGRES DATABASE CONNECTION SETUP====#
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL

#create database connection url
SQLALCHEMY_DATABASE_URL = DATABASE_URL

#set up the database engine for connecting to the PostgreSQL database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#configure sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#base class for our models
Base = declarative_base()

#dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()