from sqlalchemy import Column, String, Integer
from database.models.base import Base

# pylint: disable=too-few-public-methods


class SongsDao(Base):
    __tablename__ = "songs_counter"
    name = Column(String(255), primary_key=True)
    count = Column(Integer, nullable=False)
