from unittest import TestCase
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, Integer
import warnings

from . import Postgresql, DATABASE, DEFAULT_DB_URI, DB_URI
from pkg.database.database import Database

Base = declarative_base()


def tearDownModule():
    """Clear database cache after all tests"""
    Postgresql.clear_cache()


class TestTable(Base):

    __tablename__ = "test_table"

    _id = Column(Integer, primary_key=True)
    name = Column(String)


class TestDatabase(TestCase):

    def setUp(self):
        """Create a test database"""
        warnings.simplefilter("ignore", ResourceWarning)
        self.postgresql = Postgresql()
        self.db = Database(DEFAULT_DB_URI, DB_URI)

    def test_build(self):
        """Test building a new database"""
        self.db.build()

    def tearDown(self):
        """Drop a test database"""
        self.db.default_engine.dispose()
        self.db.engine.dispose()
        self.postgresql.stop()
