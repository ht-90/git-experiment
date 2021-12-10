from unittest import TestCase
from testing.postgresql import PostgresqlFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, Integer
import warnings


# Configure a test database
USER = "postgres"
HOST = "127.0.0.1"
PORT = 5555
DEFAULT_DATABSE = "test"
DEFAULT_DB_URI = f"postgresql://{USER}@{HOST}:{PORT}/{DEFAULT_DATABSE}"

Postgresql = PostgresqlFactory(
    cache_initialized_db=True,
    user=USER,
    host=HOST,
    port=PORT,
    database=DEFAULT_DATABSE,
)


Base = declarative_base()


def tearDownModule():
    """Clear database cache after all tests"""
    Postgresql.clear_cache()


class TestTable(Base):
    __tablename__ = "test_table"
    _id = Column(Integer, primary_key=True)
    name = Column(String)


class CreateSchema(TestCase):

    def setUp(self):
        """Create a test database and engine"""
        warnings.simplefilter("ignore", ResourceWarning)
        self.postgresql = Postgresql()
        self.engine = create_engine(self.postgresql.url())

    def test_create_schema(self):
        """Test creating a schema"""
        Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)

        with Session() as session:
            # Add data to a test table
            test_data = TestTable(name="test")
            session.add(test_data)
            session.commit()
            test_data_count = len(session.query(TestTable).all())

        self.assertEqual(test_data_count, 1)

    def tearDown(self):
        """Drop a test database"""
        self.engine.dispose()
        self.postgresql.stop()
