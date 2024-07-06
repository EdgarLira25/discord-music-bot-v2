import unicodedata
import string

help_message = """
```-p ou -play <Musica> -> Adiciona Música na Fila
-pause -> Pausa e Despausa a Música
-s ou -skip -> Pula para próxima música da Fila
-c ou -clear -> Limpa Fila De Músicas
-k ou -kill-> Reinicia Todas as Variáveis - Usado Caso o Bot Bug
-q ou -queue -> Mostra a Fila De Músicas 
-help -> Lista Comandos```
"""

def clean_word(word: str):
    def remover_acentos(word: str):
        nfkd = unicodedata.normalize("NFD", word)
        return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")

    word = word.lower()
    word = remover_acentos(word)
    word = word.translate(str.maketrans("", "", string.punctuation))
    word = word.replace(" ", "")

    return word


def mapper_command(key: str):
    map_command = {
        "-p": "-play",
        "-s": "-skip",
        "-c": "-clear",
        "-k": "-kill",
        "-q": "-queue",
        "-help": "-help",
    }

    return map_command.get(key, key)
