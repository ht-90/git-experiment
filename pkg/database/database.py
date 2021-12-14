from sqlalchemy import create_engine, inspect
from sqlalchemy.schema import CreateSchema
from sqlalchemy.exc import ProgrammingError


class Database:
    """Database with postgis extension"""

    def __init__(self, default_db_uri, db_uri):
        self.default_database_uri = default_db_uri
        self.database_uri = db_uri
        self.database_name = self.database_uri.split("/")[-1]
        self.default_engine = create_engine(self.default_database_uri)
        self.engine = None

    def build(self):
        """Build a new database with extensions"""
        try:
            with self.default_engine.connect() as con:
                self._create_database(con)
                self._connect_database()

            with self.engine.connect() as con:
                self._create_postgis(con)

        except ProgrammingError as e:
            raise e

    def _create_database(self, con):
        con.execute("commit")
        con.execute(f"CREATE DATABASE {self.database_name};")

    def _connect_database(self):
        self.engine = create_engine(self.database_uri)

    @staticmethod
    def _create_postgis(con):
        con.execute("commit")
        con.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
