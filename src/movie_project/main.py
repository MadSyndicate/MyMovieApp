from dotenv import load_dotenv
load_dotenv()
import sys

import src.movie_project.services.movies as movie_ops
import src.movie_project.services.visualize_data as vis_ops
import src.movie_project.services.users as user_ops
import src.movie_project.services.session as session
import src.movie_project.services.helper as helper


def shutdown_application():
    """
    Gracefully shuts down the application
    """
    print("Bye!")
    sys.exit()


def show_menu_and_get_input():
    """
    Function to show all available menu and get user input. Is getting called
    before each next command input is expected
    :return: The user input as integer; printing out an error message instead if no
    integer valid input was given
    """
    print(f"{helper.Bcolors.CYAN}Menu:")
    print("0. Exit")
    print("1. List movies")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Update movie")
    print("5. Stats")
    print("6. Random movie")
    print("7. Search movie")
    print("8. Movies sorted by rating")
    print("9. Movies sorted by year")
    print("10. Filter Movies")
    print(f"11. Movie-rating histogram")
    print(f"12. Generate Website")
    print(f"13. Switch User")
    print(f"14. Delete Current User")
    print()
    return helper.get_input(f"{helper.Bcolors.GREEN}Enter choice (0-14): {helper.Bcolors.ENDC}", int,
                     f"{helper.Bcolors.FAIL}Please enter an integer!{helper.Bcolors.ENDC}")


def await_enter_input():
    """
    Function to check enter input after each command final execution.
    :return: True if user does an 'enter' input, otherwise False
    """
    enter_input_check = input(f"{helper.Bcolors.GREEN}Press enter to continue! {helper.Bcolors.ENDC}")
    if enter_input_check == "":
        print()
        return True
    return False


def get_program_functions():
    """
    Helper function to set all function markers.
    :return: dictionary for available program function markers
    """
    func_options = {
        0: shutdown_application,
        1: movie_ops.get_all_movies,
        2: movie_ops.create_movie,
        3: movie_ops.delete_movie,
        4: movie_ops.update_movie_notes,
        5: movie_ops.get_movie_stats,
        6: movie_ops.rng_movie,
        7: movie_ops.fuzzy_movie_search,
        8: movie_ops.get_movies_sorted_rating,
        9: movie_ops.get_movies_sorted_year,
        10: movie_ops.get_filtered_movies,
        11: vis_ops.draw_rating_histogram_to_file,
        12: vis_ops.generate_website,
        13: user_ops.user_selection,
        14: user_ops.remove_user
    }
    return func_options


def main():
    """
    Entry point for the program. Uses function dispatcher to respond to user command inputs.
    """
    print(f"{helper.Bcolors.HEADER}********* My Movie Database *********{helper.Bcolors.ENDC}")

    print()
    function_collection = get_program_functions()
    while True:
        if session.current_user_id is None:
            user_ops.user_selection()
        menu_choice = show_menu_and_get_input()
        try:
            function_collection[menu_choice]()
        except KeyError as e:
            print(f"[ERROR] {e}")
            print(f"{helper.Bcolors.FAIL}Unknown Command {menu_choice}! "
                  f"Enter a integer from 0-{len(function_collection.keys())-1}!{helper.Bcolors.ENDC}")
            print()
        finally:
            if menu_choice != 0:
                while True:
                    if await_enter_input():
                        break


if __name__ == "__main__":
    main()
