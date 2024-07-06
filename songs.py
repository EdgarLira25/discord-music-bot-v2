from json import loads, dumps

#NOTE: Idealmente deveria ser usado um database, 
# com uma ORM como SQLAlchemy para contar as músicas
class SongsPlayed():
    def __init__(self) -> None:
        self.dict_count = {}
        self.fail = False

    def save(self):
        if not self.fail:
            with open("contador.json", "w") as songs:
                songs.write(dumps(self.dict_count))

    def load(self):
        try:
            with open("contador.json", "r") as songs:
                self.dict_count = loads(songs.read())
        except Exception as e:
            print("Erro ao Carregar contador de músicas, usando um genérico", e)
            self.fail = True
            self.dict_count = {}


songs = SongsPlayed()
songs.load()