from services.songs_counter import SongsCounter


def test_add():
    counter = SongsCounter()
    counter.add("Teste")
    assert counter.get("Teste") == 1


def test_get_not_exists():
    counter = SongsCounter()
    assert counter.get("Não Existe") == 0


def test_add_plus_one():
    counter = SongsCounter()
    counter.add("Dois")
    counter.add("Dois")
    assert counter.get("Dois") == 2
