from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from src.Settings import settings

DB_URL = settings.sqlalchemy_database_url

engine = create_engine(DB_URL)
session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

"""
Create Session for access to DB
"""
def get_db():
    """
    :return: instance of Session object
    :type: Session
    """
    db = session()
    try:
        yield db
    finally:
        db.close()
