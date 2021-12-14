from unittest import TestCase
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, Integer
import warnings

from . import Postgresql, DATABASE, DEFAULT_DB_URI, DB_URI


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
        # Build a new database
        self.db.build()
        # Get extension names installed
        with self.db.engine.connect() as con:
            res = con.execute("SELECT * FROM pg_extension;")
            extensions = [ext["extname"] for ext in res]
        # Ensure database is built with extensions
        self.assertEqual(self.db.engine.url.database, DATABASE)
        self.assertTrue("postgis" in extensions)

    def tearDown(self):
        """Drop a test database"""
        self.db.default_engine.dispose()
        self.db.engine.dispose()
        self.postgresql.stop()


class TestCreateSchema(TestCase):

    def setUp(self):
        """Create a test database and engine"""
        warnings.simplefilter("ignore", ResourceWarning)
        self.postgresql = Postgresql()
        self.engine = create_engine(self.postgresql.url())

    def test_create_schema(self):
        """Test creating a new schema"""
        # Create a schema
        test_schema = "test_schema"
        create_schema(self.engine, test_schema)
        # Get a list of databases
        insp = inspect(self.engine)
        schema_list = insp.get_schema_names()
        self.assertTrue(test_schema in schema_list)

    def tearDown(self):
        """Drop a test database"""
        self.engine.dispose()
        self.postgresql.stop()


class TestTruncateSchemaTable(TestCase):

    def setUp(self):
        """Create a test database and engine"""
        warnings.simplefilter("ignore", ResourceWarning)
        self.postgresql = Postgresql()
        self.engine = create_engine(self.postgresql.url())

    def test_truncate_schema_table(self):
        """Test truncating a table"""
        # Create a test table
        Base.metadata.create_all(bind=self.engine)
        # Create db connection
        Session = sessionmaker(bind=self.engine)

        with Session() as session:
            # Add data to a test table
            test_data = TestTable(name="test")
            session.add(test_data)
            session.commit()
            test_data_count = len(session.query(TestTable).all())

        # Truncate data in a test table
        truncate_schema_table(TestTable, self.engine)
        with Session() as session:
            test_data_count_trunc = len(session.query(TestTable).all())

        # Check data counts
        self.assertEqual(test_data_count, 1)
        self.assertEqual(test_data_count_trunc, 0)

    def tearDown(self):
        """Drop a test database"""
        self.engine.dispose()
        self.postgresql.stop()
