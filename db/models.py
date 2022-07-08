from sqlalchemy import Column, func, UniqueConstraint
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Chat(Base):
    __tablename__ = "chat"
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    vk_id = Column(String(64), unique=True)
    last_pidor = Column(DateTime(timezone=True))
    last_natural = Column(DateTime(timezone=True))

    def __repr__(self):
        return self.name


class History(Base):
    __tablename__ = "pidor_history"
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    vk_id = Column(String(64))
    datetime = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())
    chat = Column(Integer, ForeignKey("chat.id"))

    def __repr__(self):
        return self.name


class HistoryNatural(Base):
    __tablename__ = "natural_history"
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    vk_id = Column(String(64))
    datetime = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())
    chat = Column(Integer, ForeignKey("chat.id"))

    def __repr__(self):
        return self.name
