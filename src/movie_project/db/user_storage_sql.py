from pathlib import Path
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, text
from src.movie_project.db.movie_storage_sql import delete_movies_by_user_id

# Define the database URL
BASE_DIR = Path(__file__).resolve().parents[3]
DB_PATH = f'{BASE_DIR}/data/movies.db'
# Create the engine
engine = create_engine(f'sqlite:///{DB_PATH}')

def list_users():
    """Returns all users in the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT id, username FROM users ORDER BY id ASC"))
        users = result.fetchall()

    return {user[0]: user[1] for user in users}


def get_username_by_id(user_id):
    """Returns the username associated with the given user_id."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT username FROM users WHERE id = :user_id"),
                                    {"user_id": user_id})
        user = result.fetchone()
    if user is not None:
        return True, user[0]
    return False, None


def add_user(username):
    """Add a new user to the database if username doesn't already exist."""
    with engine.connect() as connection:
        try:
            result = connection.execute(text("INSERT INTO users (username) VALUES (:username)"),
                {"username": username})
            connection.commit()
            user_id = result.lastrowid
            print(f"User {username} was added.")
            print()
            return True, {user_id: username}
        except IntegrityError:
            print(f"User {username} already exists. Try again with a different username.")
        except Exception as e:  #TODO: concrete what to do
            print(f"An error occurred. Please try again or contact the maintainer"
                  f" if the problem persists.")
        return False, None


def delete_user_by_id(user_id):
    """Delete a user from the database, including all rows in movie-table with
     the given user_id as well as the user-table row."""
    # using transaction to be able to roll back user-table changes if needed
    with engine.begin() as connection:
        try:
            connection.execute(text("DELETE FROM users WHERE id = :user_id"),
                {"user_id": user_id})
            #connection.commit()
            print(f"User with id {user_id} deleted successfully. "
                  f"Going on to delete movies with user_id {user_id}.")
            delete_movies_by_user_id(user_id, connection)
        except Exception as e:  #TODO: concrete what to do
            print(e)
            print("An error occurred. Please try again or contact the maintainer "
                  "if the problem persists.\nCurrent attempt got rolled back, "
                  "no changes in database!")
            raise e
