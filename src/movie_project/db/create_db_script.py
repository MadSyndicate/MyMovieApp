from pathlib import Path
from sqlalchemy import create_engine, text

# Projekt-Root
BASE_DIR = Path(__file__).resolve().parents[3]

# DB Pfad
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "movies.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)

print(f"DB_PATH: {DB_PATH}")

engine = create_engine(f"sqlite:///{DB_PATH}")

with engine.connect() as create_connection:
    create_connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_URL TEXT,
            user_id INTEGER NOT NULL,
            user_notes TEXT,
            imdb_id TEXT
        )
    """))
    create_connection.commit()

with engine.connect() as create_connection:
    create_connection.execute(text("""
         CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """))
    create_connection.commit()