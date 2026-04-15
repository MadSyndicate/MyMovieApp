from pathlib import Path
from sqlalchemy import create_engine, text


# Define the database URL
BASE_DIR = Path(__file__).resolve().parents[3]
DB_PATH = f'{BASE_DIR}/data/movies.db'
# Create the engine
engine = create_engine(DB_PATH)

# Create the movies table if it does not exist
with engine.connect() as create_connection:
    create_connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_URL TEXT
        )
    """))
    create_connection.commit()
