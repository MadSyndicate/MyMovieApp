from sqlalchemy import create_engine, text
from sqlalchemy.engine import row

# Define the database URL
DB_URL = "sqlite:///./db/movies.db"

# Create the engine
engine = create_engine(DB_URL)


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating FROM movies"))
        movies = result.fetchall()

    return {movie[0]: {"year": movie[1], "rating": movie[2]} for movie in movies}


def get_specific_movie(title):
    """Retrieve a specific movie by title from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating FROM movies WHERE title = :title"),
                                    {"title": title})
        movie = result.fetchall()
    if title in movie:
        return True, {movie[0]: {"year": movie[1], "rating": movie[2]}}
    return False, None


def add_movie(title, year, rating):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating) VALUES (:title, :year, :rating)"),
                               {"title": title, "year": year, "rating": rating})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("DELETE FROM movies WHERE title = :title"),
                               {"title": title})
            connection.commit()
            print(f"Movie '{title}' deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("UPDATE movies SET rating = :rating WHERE title = :title"),
                               {"title": title, "rating": rating})
            connection.commit()
            print(f"Movie '{title}' updated successfully.")
        except Exception as e:
            print(f"Error: {e}")
