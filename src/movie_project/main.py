from dotenv import load_dotenv
load_dotenv()
from src.movie_project.services.users import user_selection, remove_user

import statistics as stats
import random as rand
import sys

import matplotlib.pyplot as plt
from fuzzywuzzy import process
from src.movie_project.db import movie_storage_sql as db_sql
import src.movie_project.api.fetch_movie_data as movie_api
from src.movie_project.services import html_generator

import src.movie_project.services.session as session

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
TEMPLATE_PATH = BASE_DIR / "_template" / "index_template.html"
OUTPUT_PATH = BASE_DIR / "_static" / "index.html"


# Source - https://stackoverflow.com/a/287944
class Bcolors:
    """
    holds the used style colors and formats
    """
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_input(prompt, cast_type, error_msg, limit=0, err_skip=False):
    """
    helper-function to validate different input types and respond to the user
    what went wrong if needed

    :param prompt: Print out to get user input
    :param cast_type: the expected input type we want to get from the user
    :param error_msg: in case casting to cast_type fails, this gets printed out
    :param limit: if not specified means no limit; otherwise error message with input limit
    :return: returns the user input in the given cast_type or prints out an error message
    """
    while True:
        if cast_type == str:
            value = input(f"{Bcolors.BOLD}{prompt}{Bcolors.ENDC}")
            if len(value) == 0 and not err_skip:
                print(error_msg)
                continue
            return value

        try:
            value = cast_type(input(prompt))
            if limit != 0 and value > limit:
                print(f"{Bcolors.FAIL}Input {value} is bigger then allowed limit ({limit}). "
                      f"Please try again.{Bcolors.ENDC}")
                continue
            return value
        except ValueError:
            print(error_msg)


def validate_db_not_empty():
    """
    Helper function to validate if database is not empty.
    :return: A tuple with bool for the quote 'db_not_empty' and the actual entire db
    """
    db_data = db_sql.list_movies()
    if len(db_data) == 0:
        return False, None
    return True, db_data


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
    print(f"{Bcolors.CYAN}Menu:")
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
    return get_input(f"{Bcolors.GREEN}Enter choice (0-14): {Bcolors.ENDC}", int,
                     f"{Bcolors.FAIL}Please enter an integer!{Bcolors.ENDC}")


def create_movie():
    """
    Function to create a new movie and add it to the database.
    Ask user for 3 inputs: Name, Year of Release and Rating.
    If given input is not matching expected input value type,
    prints an error message and awaits further, correct input.
    """
    movie_name = get_input(f"{Bcolors.GREEN}Enter a movie name: {Bcolors.ENDC}", str,
                           "Movie name must not be empty! Please try again.")
    movie_exist = db_sql.get_movie_by_title(movie_name)
    if movie_exist[0]:
        print(f"The Database already has a movie called "
              f"{Bcolors.BOLD}{movie_name}{Bcolors.ENDC} "
              f"({Bcolors.BOLD}{movie_exist[1]['year']}{Bcolors.ENDC}) "
              f"with a rating of {Bcolors.BOLD}{movie_exist[1]['rating']}{Bcolors.ENDC}")
    else:
        api_response = movie_api.fetch_movie_data(movie_name)
        if api_response["Response"] == 'True':
            fetched_movie_name = api_response.get("Title") or movie_name
            movie_year = api_response.get("Year", None)
            movie_rating = next(
                (float(r["Value"].split("/")[0]) for r in api_response["Ratings"] if r["Source"] == "Internet Movie Database"),
                None
            )
            movie_poster = api_response.get("Poster", None)
            db_sql.add_movie(fetched_movie_name, movie_year, movie_rating, movie_poster)
        else:
            print(f"Movie with name {movie_name} could not be found on omdapi.com. Please try another name!")
    print()


def get_all_movies():
    """
    Prints out the amount of all movies stored in the database and
    each movie in the format: name (year) : rating
    Also tells the user if there are no movies in the database
    """
    db_data = db_sql.list_movies()

    if len(db_data) == 0:
        print("There are currently zero movies in the database.")
    else:
        print(f"{len(db_data)} movies in total")
        for movie_name, movie_stats in db_data.items():
            print(f"{Bcolors.BOLD}{movie_name} "
                  f"({Bcolors.ENDC}{Bcolors.BOLD}{movie_stats['year']}): "
                  f"{Bcolors.ENDC}{Bcolors.BOLD}{movie_stats['rating']}"
                  f"{Bcolors.ENDC}")
    print()


def update_movie_notes():
    """
    Updates notes for a movie in the database for current user.
    Movie name must be exact match to be updated,
    otherwise prints out that no movie was found.
    """

    movie_name = input(f"{Bcolors.GREEN}Enter a movie name that shall be updated: {Bcolors.ENDC}")
    movie_exist = db_sql.get_movie_by_title(movie_name)
    if movie_exist[0]:
        movie_notes = get_input(f"{Bcolors.GREEN}Enter notes for the move {movie_name}: {Bcolors.ENDC}",
                                str, "", err_skip=True)
        db_sql.update_movie_notes(movie_name, movie_notes)
        print(f"Movie {Bcolors.BOLD}`{movie_name}`{Bcolors.ENDC} successfully updated! ")
    else:
        print(f"{Bcolors.FAIL}Error: `{movie_name}` was not found and thus "
              f"cannot be updated!{Bcolors.ENDC}")
    print()


def delete_movie():
    """
    Deletes a movie from the database. Movie name must be exact match to be updated,
    otherwise prints out that no movie was found.
    """
    movie_name = input("Enter a movie name that shall be deleted: ")
    movie_exist = db_sql.get_movie_by_title(movie_name)
    if movie_exist[0]:
        db_sql.delete_movie_by_title(next(iter(movie_exist[1])))
        print(f"{Bcolors.BOLD}`{movie_name}`{Bcolors.ENDC} was deleted from database")
    else:
        print(f"{Bcolors.FAIL}Error: `{movie_name}` was not found in database and thus "
              f"cannot be deleted!")
    print()


def get_top_and_flop_movies(db_data):
    """
    Helper function to return a tuple of the best and worst rated movie lists
    respectively from given db_data
    :param db_data: data from movies database
    :return: (top_movies, flop_movies)
    """
    max_rating = max(movie["rating"] for movie in db_data.values())
    min_rating = min(movie["rating"] for movie in db_data.values())

    top_movies = [name for name, data in db_data.items() if data["rating"] == max_rating]
    flop_movies = [name for name, data in db_data.items() if data["rating"] == min_rating]

    return top_movies, flop_movies


def get_movie_stats():
    """
    Function to get some statistical information about the movie database.
    Prints out the average rating and median rating of all movies in the database
    and also shows respectively a list of the best and worst rated movies
    with their given rating
    """
    check_for_db_data = validate_db_not_empty()
    if not check_for_db_data[0]:
        print("The database is empty, we cannot show any stats.")
        print()
        return

    db_data = check_for_db_data[1]

    average_rating = stats.mean(movie["rating"] for movie in db_data.values())
    median_rating = stats.median(movie["rating"] for movie in db_data.values())
    best_rated_movie_list, worst_rated_movie_list = get_top_and_flop_movies(db_data)

    print(f"The average rating in the movie database: "
          f"{Bcolors.BOLD}{average_rating: .1f}{Bcolors.ENDC}")
    print(f"The median rating in the movie database: "
          f"{Bcolors.BOLD}{median_rating: .1f}{Bcolors.ENDC}")

    print("The best rated movie/s in the database:")
    for name in best_rated_movie_list:
        print(f"{Bcolors.BOLD}{name}, {db_data[name]['rating']}{Bcolors.ENDC}")
    print("\nThe worst rated movie/s in the database:")
    for name in worst_rated_movie_list:
        print(f"{Bcolors.BOLD}{name}, {db_data[name]['rating']}{Bcolors.ENDC}")
    print()


def rng_movie():
    """
    Prints out the movie information of a randomly chosen movie from the database
    """
    check_for_db_data = validate_db_not_empty()
    if not check_for_db_data[0]:
        print("The database is empty, we cannot show any random movie.")
        print()
        return

    data = check_for_db_data[1]
    rand_movie_title = rand.choice(list(data.keys()))
    print(f"Randomly chosen movie: {Bcolors.BOLD}{rand_movie_title} "
          f"({data[rand_movie_title]['year']}), "
          f"{data[rand_movie_title]['rating']}{Bcolors.ENDC}")
    print()


def fuzzy_movie_search():
    """
    Advanced search with fuzzy matching. Score cutoff is set relative low to higher the
    chances to get a wider overview of possible options. In case even that fails,
    the highest possible score match on search input is printed out as option.
    If search input is exact match with movie title, prints out the movie information.
    """
    search_input = input("Enter part of movie name: ")
    data = db_sql.get_movie_by_title(search_input)
    if data[0]:
        movie_title_db = next(iter(data[1]))
        print(f"{Bcolors.BOLD}{movie_title_db}: {data[1][movie_title_db]}{Bcolors.ENDC}")
    else:
        fuzzy_data = db_sql.list_movies()
        all_matches = process.extractBests(search_input, fuzzy_data.keys(), score_cutoff=60)
        print(f"{Bcolors.WARNING}The movie "
              f"{Bcolors.BOLD}{search_input}{Bcolors.ENDC}{Bcolors.WARNING} "
              f"does not exist."
              f" Did you mean: {Bcolors.ENDC}")
        if len(all_matches) > 0:
            for match, _ in all_matches:
                print(f"{Bcolors.BOLD}{match}{Bcolors.ENDC}")
        else:
            fallback_minimum_match = process.extractOne(search_input, fuzzy_data.keys())
            print(f"{Bcolors.BOLD}{fallback_minimum_match[0]}{Bcolors.ENDC}")


def get_movies_sorted_rating():
    """
    Prints out all movies in the database by rating in ascending order
    """
    data = db_sql.list_movies()
    sorted_by_rating = sorted(data.items(), key=lambda m: m[1]["rating"])
    for movie, data in sorted_by_rating:
        print(f"{Bcolors.BOLD}{movie} ({data['year']}), "
              f"{data['rating']}{Bcolors.ENDC}")
    print()


def get_movies_sorted_year():
    """
    Prints out all movies in the database by year of release. Order can be controlled by user input
    """
    data = db_sql.list_movies()
    sort_order_unknown = True
    sorted_by_year = []
    while sort_order_unknown:
        sort_input = input("Do you want the latest movie first? (Y/N):")
        if sort_input.lower() == "y":
            sorted_by_year = sorted(data.items(), key=lambda m: m[1]['year'], reverse=True)
            sort_order_unknown = False
        elif sort_input.lower() == "n":
            sorted_by_year = sorted(data.items(), key=lambda m: m[1]['year'])
            sort_order_unknown = False
        else:
            print("Please enter either 'Y' or 'N'!")

    for movie, data in sorted_by_year:
        print(f"{Bcolors.BOLD}{movie} ({data['year']}), "
              f"{data['rating']}{Bcolors.ENDC}")
    print()


def await_enter_input():
    """
    Function to check enter input after each command final execution.
    :return: True if user does an 'enter' input, otherwise False
    """
    enter_input_check = input(f"{Bcolors.GREEN}Press enter to continue! {Bcolors.ENDC}")
    if enter_input_check == "":
        print()
        return True
    return False


def draw_rating_histogram_to_file():
    """
    Function to print a simple histogram of movie rating and number of movies
    in the database in a .png-file.
    """
    data = db_sql.list_movies()
    file_name_input = input(f"{Bcolors.GREEN}Enter a file name to "
                            f"put the histogram: {Bcolors.ENDC}")
    rating_list = [m["rating"] for m in data.values()]
    plt.hist(rating_list)
    plt.title("Histogram of movie ratings")
    plt.xlabel("Rating")
    plt.ylabel("Number of movies")
    plt.savefig(file_name_input + '.png')
    print(f"created file {Bcolors.BOLD}{file_name_input}.png{Bcolors.ENDC}")
    print()


def ask_for_filter_input(prompt, cast_type, error_msg):
    """
    Helper-Function for the get_filtered_movies function. Works similar to get_input-function;
    since for filters we also need to accept 'None' inputs and in theory don't require
    any limits, this function is specialized for that to ensure code readability.
    :param prompt: Print out to get user input
    :param cast_type: the expected input type we want to get from the user
    :param error_msg: in case casting to cast_type fails, this gets printed out
    :return: the user input converted to cast_type, an error if input was not castable to
        required type, None if no input
    """
    filter_input = input(prompt)
    while True:
        if filter_input != "":
            try:
                value = cast_type(filter_input)
                return value
            except ValueError:
                filter_input = input(error_msg)
                continue
        return None


def generate_website():
    movie_data = db_sql.list_movies()
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as fr:
        template = fr.read()
        html_output = html_generator.generate_html_from_template(template, "Masterschool's Movie App", movie_data)
        with open(OUTPUT_PATH, "w") as fw:
            fw.write(html_output)
        print("Website generated!")


def get_filtered_movies():
    """
    Function to print out a list for the given filter criteria. User is asked for a minimum rating,
    start and end year. If no input is given for any of those criteria, they are considered
    to not exist.
    """
    db_data = db_sql.list_movies()

    minimum_rating = ask_for_filter_input(
        f"{Bcolors.GREEN}Enter a minimum rating (leave blank for no minimum): {Bcolors.ENDC}",
        float,
        f"{Bcolors.FAIL}Please enter an float or leave blank!: {Bcolors.ENDC}")
    start_year = ask_for_filter_input(
        f"{Bcolors.GREEN}Enter a minimum year (leave blank for no minimum year): {Bcolors.ENDC}",
        int,
        f"{Bcolors.FAIL}Please enter an integer or leave blank!: {Bcolors.ENDC}")
    end_year = ask_for_filter_input(
        f"{Bcolors.GREEN}Enter a maximum year (leave blank for no maximum year): {Bcolors.ENDC}",
        int,
        f"{Bcolors.FAIL}Please enter an integer or leave blank!: {Bcolors.ENDC}")
    for movie, data in db_data.items():

        if minimum_rating is not None and data["rating"] < minimum_rating:
            continue
        if start_year is not None and data["year"] < start_year:
            continue
        if end_year is not None and data["year"] > end_year:
            continue

        print(f"{movie} ({data['year']}): {data['rating']}")
        print()


def get_program_functions():
    """
    Helper function to set all function markers.
    :return: dictionary for available program function markers
    """
    func_options = {
        0: shutdown_application,
        1: get_all_movies,
        2: create_movie,
        3: delete_movie,
        4: update_movie_notes,
        5: get_movie_stats,
        6: rng_movie,
        7: fuzzy_movie_search,
        8: get_movies_sorted_rating,
        9: get_movies_sorted_year,
        10: get_filtered_movies,
        11: draw_rating_histogram_to_file,
        12: generate_website,
        13: user_selection,
        14: remove_user
    }
    return func_options


def main():
    """
    Entry point for the program. Uses function dispatcher to respond to user command inputs.
    """
    print(f"{Bcolors.HEADER}********* My Movie Database *********{Bcolors.ENDC}")

    print()
    function_collection = get_program_functions()
    while True:
        if session.current_user_id is None:
            user_selection()
        menu_choice = show_menu_and_get_input()
        try:
            function_collection[menu_choice]()
        except KeyError as e:
            print(f"[ERROR] {e}")
            print(f"{Bcolors.FAIL}Unknown Command {menu_choice}! "
                  f"Enter a integer from 0-{len(function_collection.keys())-1}!{Bcolors.ENDC}")
            print()
        finally:
            if menu_choice != 0:
                while True:
                    if await_enter_input():
                        break


if __name__ == "__main__":
    main()
