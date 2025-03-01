"""Módulo de gerenciamento para contagem músicas tocadas"""

from json import JSONDecodeError, loads, dumps
from threading import Lock


class MetaClassSongsCounter(type):
    """Metaclasse para singleton seguro entre threads"""

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class SongsCounter(metaclass=MetaClassSongsCounter):

    def __init__(self) -> None:
        self._dict_count: dict[str, int] = self._load()
        self._load()
        self.fail = False

    def _save(self):
        if not self.fail:
            with open("contador.json", "w", encoding="utf-8") as songs:
                songs.write(dumps(self._dict_count))

    def _load(self) -> dict[str, int]:
        try:
            with open("contador.json", "r", encoding="utf-8") as songs:
                return loads(songs.read())
        except (JSONDecodeError, TypeError, ValueError, FileNotFoundError) as e:
            print("Erro ao Carregar contador de músicas, usando um genérico", e)
            self.fail = True
            return {}

    def add(self, name: str):
        if name in self._dict_count:
            self._dict_count[name] += 1
        else:
            self._dict_count[name] = 1

        self._save()

    def get(self, name: str) -> int:
        return self._dict_count.get(name, 0)
