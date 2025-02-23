from json import loads, dumps


# NOTE: Idealmente deveria ser usado um database,
# com uma ORM como SQLAlchemy para contar as músicas
class SongsCounter:
    def __init__(self) -> None:
        self._dict_count: dict[str, int] = self._load()
        self._load()
        self.fail = False

    def _save(self):
        if not self.fail:
            with open("contador.json", "w") as songs:
                songs.write(dumps(self._dict_count))

    def _load(self) -> dict[str, int]:
        try:
            with open("contador.json", "r") as songs:
                return loads(songs.read())
        except Exception as e:
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
