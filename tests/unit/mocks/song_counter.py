from services.songs_counter import SongsCounter

# pylint: skip-file


class SongsCounterSaveMock(SongsCounter):
    """Classe para mock do save do json a fim de evitar side effects"""

    def __init__(self, json_path="contador.json") -> None:
        super().__init__(json_path)

    def _save(self): ...
