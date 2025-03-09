from sqlalchemy.sql.expression import Executable
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine
from database.models.base import Base
from settings.consts import DATABASE_URI

engine = create_engine(
    url=DATABASE_URI, enable_from_linting=False, pool_recycle=1800, pool_pre_ping=True
)


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
