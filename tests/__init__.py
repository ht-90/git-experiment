"""Test postgresql database configuration across tests.common.database"""

from testing.postgresql import PostgresqlFactory


# Configure a test database
USER = "postgres"
HOST = "127.0.0.1"
PORT = 5555
DEFAULT_DATABSE = "test"
DATABASE = "test_db"

DEFAULT_DB_URI = f"postgresql://{USER}@{HOST}:{PORT}/{DEFAULT_DATABSE}"
DB_URI = f"postgresql://{USER}@{HOST}:{PORT}/{DATABASE}"

Postgresql = PostgresqlFactory(
    cache_initialized_db=True,
    user=USER,
    host=HOST,
    port=PORT,
    database=DEFAULT_DATABSE,
)
