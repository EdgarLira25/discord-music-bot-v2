"""Módulo de gerenciamento para contagem de músicas tocadas"""

from sqlalchemy import insert, select, update
from database.connector import Database
from database.models.songs import SongsDao


class SongsCounter:
    """OBS: Se esta classe escalar muito, é justo fazer um repository"""

    songs = SongsDao

    def __init__(self, database_provider=Database()) -> None:
        self.db = database_provider

    def add(self, name: str) -> None:
        song = self.db.query_one_row(
            select(self.songs.name).where(self.songs.name == name)
        )
        if not song:
            self.db.statement(insert(self.songs).values(name=name, count=1))
        else:
            self.db.statement(
                update(self.songs)
                .where(self.songs.name == name)
                .values(count=self.songs.count + 1)
            )

    def get(self, name: str) -> int:
        query = self.db.query_one_row(
            select(self.songs.count).where(self.songs.name == name)
        )

        return query["count"] if query else 0
