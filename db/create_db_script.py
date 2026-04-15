from sqlalchemy import create_engine, text


# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL)

# Create the movies table if it does not exist
with engine.connect() as create_connection:
    create_connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL
        )
    """))
    create_connection.commit()

# Adding poster image url column after
with engine.connect() as create_connection:
    create_connection.execute(text("""
        ALTER TABLE movies
        ADD COLUMN poster_url TEXT;
    """))
    create_connection.commit()