from pathlib import Path
from sqlalchemy import create_engine, text
import src.movie_project.services.session as session

# Define the database URL
BASE_DIR = Path(__file__).resolve().parents[3]
DB_PATH = f'{BASE_DIR}/data/movies.db'
# Create the engine
engine = create_engine(f'sqlite:///{DB_PATH}')


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster_url, user_notes, imdb_id FROM movies WHERE user_id = :user_id"),
                                    {"user_id": session.current_user_id})
        movies = result.fetchall()

    return {movie[0]: {"year": movie[1], "rating": movie[2], "poster_url": movie[3], "user_notes": movie[4], "imdb_id": movie[5]} for movie in movies}


def get_movie_by_title(title):
    """Retrieve a specific movie by title from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating FROM movies WHERE LOWER(title) = LOWER(:title) AND user_id = :user_id"),
                                    {"title": title, "user_id": session.current_user_id})
        movie = result.fetchone()
    if movie is not None:
        return True, {movie[0]: {"year": movie[1], "rating": movie[2]}}
    return False, None


def add_movie(title, year, rating, poster, imdb_id):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating, poster_url, user_id, imdb_id) VALUES (:title, :year, :rating, :poster, :user_id, :imdb_id)"),
                               {"title": title, "year": year, "rating": rating, "poster": poster, "user_id": session.current_user_id, "imdb_id": imdb_id})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:  #TODO: concrete what to do
            print(f"An error occurred. Please try again or contact the maintainer if the problem persists.")


def delete_movie_by_title(title):
    """Delete a movie from the database for a user with given title"""
    with engine.connect() as connection:
        try:
            connection.execute(text("""
            DELETE FROM movies 
            WHERE 
                user_id = :user_id 
            AND
                title = :title"""),
    {"user_id": session.current_user_id, "title": title})
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")
            raise e


def delete_movies_by_user_id(user_id, connection):
    """Delete all movies from the database for given user_id.
    Used after User is deleted for cleanup table movies"""
    try:
        connection.execute(text("DELETE FROM movies WHERE user_id = :user_id"),
                           {"user_id": user_id})
        print(f"Movies for user_id '{user_id}' deleted successfully.")
    except Exception as e:
        print(f"Error: {e}")
        raise e


def update_movie_notes(title, notes):
    """Update a movie's notes in the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("UPDATE movies SET user_notes = :notes WHERE title = :title AND user_id = :user_id"),
                               {"title": title, "notes": notes, "user_id": session.current_user_id})
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")
