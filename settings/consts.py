import os

TIME = 1 if os.environ.get("ENV", "PROD") != "TEST" else 0
DATABASE_URI = (
    os.environ.get("DATABASE_URI", "sqlite:///music.db")
    if os.environ.get("ENV", "PROD") != "TEST"
    else "sqlite:///teste.db"
)
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET", "")
