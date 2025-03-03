import os
from sqlalchemy.sql.expression import Executable
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine
from database.models.base import Base

DATABASE_URI = (
    os.environ.get("DATABASE_URI", "sqlite:///music.db")
    if os.environ.get("ENV", "PROD") != "TEST"
    else "sqlite:///teste.db"
)

engine = create_engine(url=DATABASE_URI, enable_from_linting=False)


class Database:

    def query_one_row(self, query: Executable) -> dict:
        session = sessionmaker(bind=engine)
        with session() as session:
            result = session.execute(query).fetchone()
            session.close()
            if not result:
                return {}
            return result._asdict()

    def statement(self, statement: Executable):
        session = sessionmaker(bind=engine)
        with session() as session:
            session.execute(statement)
            session.commit()
            session.close()

    def migrate_all(self):
        Base.metadata.create_all(engine)
