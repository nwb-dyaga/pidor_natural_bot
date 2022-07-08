from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from db import Base
from db.base import DATABASE


def connect_db() -> sessionmaker():
    engine = create_engine(URL.create(**DATABASE))
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    return session()
