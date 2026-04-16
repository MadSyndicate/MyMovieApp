from src.movie_project.db.movie_storage_sql import add_movie, list_movies, delete_movie_by_title, update_movie_notes
from src.movie_project.db.user_storage_sql import add_user, list_users, delete_user_by_id
from src.movie_project.services import session

test_user = add_user("test_user")
for user_id, _ in test_user[1].items():
    session.current_user_id = user_id

add_movie("Inception",
          2010,
          8.8,
          'https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SX300.jpg',
          imdb_id='tt1375666')
print(list_movies())

# Test listing movies
movies = list_movies()
print(movies)

# Test updating a movie's rating
update_movie_notes("Inception", 'Test-Note')

# Test deleting a movie
delete_movie_by_title("Inception")
print(list_movies())  # Should be empty if it was the only movie
delete_user_by_id(session.current_user_id)
print(list_users()) # Should be empty if it was the only user