"""Módulo de gerenciamento para contagem de músicas tocadas"""

from functools import lru_cache
from sqlalchemy import insert, select, update
from database.connector import Database
from database.models.songs import SongsDao


class SongsCounter:
    """OBS: Se esta classe escalar muito, é justo fazer um repository"""

    songs = SongsDao

    def __init__(self, database_provider=Database()) -> None:
        self.db = database_provider

    def add(self, name: str) -> int:
        if song_count := self.get(name):
            self.db.statement(
                update(self.songs)
                .where(self.songs.name == name)
                .values(count=self.songs.count + 1)
            )
            return song_count + 1
        self.db.statement(insert(self.songs).values(name=name, count=1))
        return 1

    def get(self, name: str) -> int:
        query = self.db.query_one_row(
            select(self.songs.count).where(self.songs.name == name)
        )

        return query["count"] if query else 0

    @lru_cache(maxsize=1)
    def get_all(self) -> list[dict]:
        return self.db.query(select(self.songs.name))
