from src.movie_project.db import user_storage_sql as user_db
from src.movie_project.db import movie_storage_sql as movie_db
import src.movie_project.services.session as session


def create_new_user():
    user_name = ''
    while True:
        user_name = input("Please enter your name: ")   #TODO making sure correct/length type is used
        result = user_db.add_user(user_name)
        if result[0]:
            return result[1]


def user_selection():
    user_dict = user_db.list_users()

    if len(user_dict) > 0:
        print("Select an active user:")
        user_items = list(user_dict.items())
        while True:
            tracker = 0
            for i, (user_id, username) in enumerate(user_items, start=1):
                print(f"{i}: {username}")
                tracker = i
            tracker += 1
            print(f"{tracker}: Add a new user")
            chosen_user_inp = int(input("Please enter your choice: "))

            if 1 <= chosen_user_inp <= len(user_items) and chosen_user_inp != tracker:
                actual_user = user_items[chosen_user_inp - 1]
                session.current_user_id = actual_user[0]
                session.current_user_name = actual_user[1]
                break
            elif chosen_user_inp == tracker:
                new_user = create_new_user()
                for user_id, name in new_user.items():
                    session.current_user_id = user_id
                    session.current_name = name
                print(f"New user {session.current_user_name} created and set as active user")
                break
            else:
                print("Invalid choice, try again.")
    else:
        print("No users to select from in database. Creating user now...")
        new_user = create_new_user()
        for user_id, name in new_user.items():
            session.current_user_id = user_id
            session.current_name = name

    print(f"New user {session.current_user_name} set as active user")
    return


def remove_user():
    print(f"You are about to delete the current user {session.current_user_name} and all movies"
          f"in the database connected to this user. This cannot be reverted!")
    user_inp = input("Please enter 'DELETE' if you are sure, or anything else to cancel: ")
    if user_inp == "DELETE":
        try:
            user_db.delete_user_by_id(session.current_user_id)
            movie_db.delete_movies_by_user_id(session.current_user_id)
            session.current_user_id = None
            session.current_name = None
            return
        except Exception as e:
            print(e)
            print("[ERROR]: error while deleting user with id {session.current_user_id}")
    else:
        print("Deleting user was cancelled.")
        return