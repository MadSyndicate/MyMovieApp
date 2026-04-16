import statistics as stats
import random as rand

from fuzzywuzzy import process

from src.movie_project.services import helper
import src.movie_project.api.fetch_movie_data as movie_api
from src.movie_project.db import movie_storage_sql as db_movie


def create_movie():
    """
    Function to create a new movie and add it to the database.
    Ask user for 3 inputs: Name, Year of Release and Rating.
    If given input is not matching expected input value type,
    prints an error message and awaits further, correct input.
    """
    movie_name = helper.get_input(f"{helper.Bcolors.GREEN}Enter a movie name: "
                                  f"{helper.Bcolors.ENDC}", str,
                           "Movie name must not be empty! Please try again.")
    movie_exist = db_movie.get_movie_by_title(movie_name)
    if movie_exist[0]:
        print(f"The Database already has a movie called "
              f"{helper.Bcolors.BOLD}{movie_name}{helper.Bcolors.ENDC} "
              f"({helper.Bcolors.BOLD}{movie_exist[1]['year']}{helper.Bcolors.ENDC})"
              f"with a rating of {helper.Bcolors.BOLD}{movie_exist[1]['rating']}"
              f"{helper.Bcolors.ENDC}")
    else:
        api_response = movie_api.fetch_movie_data(movie_name)
        if api_response["Response"] == 'True':
            fetched_movie_name = api_response.get("Title") or movie_name
            movie_year = api_response.get("Year", None)
            movie_rating = next(
                (float(r["Value"].split("/")[0])
                 for r in api_response["Ratings"] if r["Source"] == "Internet Movie Database"),
                None
            )
            movie_poster = api_response.get("Poster", None)
            movie_imdb_id = api_response.get("imdbID", None)
            db_movie.add_movie(
                fetched_movie_name,
                movie_year,
                movie_rating,
                movie_poster,
                movie_imdb_id
            )
        else:
            print(f"Movie with name {movie_name} could not be found on omdapi.com."
                  f" Please try another name!")
    print()


def movie_table_not_empty():
    """
    Helper function to validate if database is not empty.
    :return: A tuple with bool for the quote 'db_not_empty' and the actual entire db
    """
    db_data = db_movie.list_movies()
    if len(db_data) == 0:
        return False, None
    return True, db_data

def get_all_movies():
    """
    Prints out the amount of all movies stored in the database and
    each movie in the format: name (year) : rating
    Also tells the user if there are no movies in the database
    """
    db_data = db_movie.list_movies()

    if len(db_data) == 0:
        print("There are currently zero movies in the database.")
    else:
        print(f"{len(db_data)} movies in total")
        for movie_name, movie_stats in db_data.items():
            print(f"{helper.Bcolors.BOLD}{movie_name} "
                  f"({helper.Bcolors.ENDC}{helper.Bcolors.BOLD}{movie_stats['year']}): "
                  f"{helper.Bcolors.ENDC}{helper.Bcolors.BOLD}{movie_stats['rating']}"
                  f"{helper.Bcolors.ENDC}")
    print()
    

def update_movie_notes():
    """
    Updates notes for a movie in the database for current user.
    Movie name must be exact match to be updated,
    otherwise prints out that no movie was found.
    """

    movie_name = input(f"{helper.Bcolors.GREEN}Enter a movie name that "
                       f"shall be updated: {helper.Bcolors.ENDC}")
    movie_exist = db_movie.get_movie_by_title(movie_name)
    if movie_exist[0]:
        movie_notes = helper.get_input(
            f"{helper.Bcolors.GREEN}Enter notes for the move {movie_name}: {helper.Bcolors.ENDC}",
            str, "")
        db_movie.update_movie_notes(movie_name, movie_notes)
        print(f"Movie {helper.Bcolors.BOLD}`{movie_name}`{helper.Bcolors.ENDC} successfully updated! ")
    else:
        print(f"{helper.Bcolors.FAIL}Error: `{movie_name}` was not found and thus "
              f"cannot be updated!{helper.Bcolors.ENDC}")
    print()


def delete_movie():
    """
    Deletes a movie from the database. Movie name must be exact match to be updated,
    otherwise prints out that no movie was found.
    """
    movie_name = input("Enter a movie name that shall be deleted: ")
    movie_exist = db_movie.get_movie_by_title(movie_name)
    if movie_exist[0]:
        db_movie.delete_movie_by_title(next(iter(movie_exist[1])))
        print(f"{helper.Bcolors.BOLD}`{movie_name}`{helper.Bcolors.ENDC} was deleted from database")
    else:
        print(f"{helper.Bcolors.FAIL}Error: `{movie_name}` was not found in database and thus "
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
    check_for_db_data = movie_table_not_empty()
    if not check_for_db_data[0]:
        print("The database is empty, we cannot show any stats.")
        print()
        return

    db_data = check_for_db_data[1]

    average_rating = stats.mean(movie["rating"] for movie in db_data.values())
    median_rating = stats.median(movie["rating"] for movie in db_data.values())
    best_rated_movie_list, worst_rated_movie_list = get_top_and_flop_movies(db_data)

    print(f"The average rating in the movie database: "
          f"{helper.Bcolors.BOLD}{average_rating: .1f}{helper.Bcolors.ENDC}")
    print(f"The median rating in the movie database: "
          f"{helper.Bcolors.BOLD}{median_rating: .1f}{helper.Bcolors.ENDC}")

    print("The best rated movie/s in the database:")
    for name in best_rated_movie_list:
        print(f"{helper.Bcolors.BOLD}{name}, {db_data[name]['rating']}{helper.Bcolors.ENDC}")
    print("\nThe worst rated movie/s in the database:")
    for name in worst_rated_movie_list:
        print(f"{helper.Bcolors.BOLD}{name}, {db_data[name]['rating']}{helper.Bcolors.ENDC}")
    print()


def rng_movie():
    """
    Prints out the movie information of a randomly chosen movie from the database
    """
    check_for_db_data = movie_table_not_empty()
    if not check_for_db_data[0]:
        print("The database is empty, we cannot show any random movie.")
        print()
        return

    data = check_for_db_data[1]
    rand_movie_title = rand.choice(list(data.keys()))
    print(f"Randomly chosen movie: {helper.Bcolors.BOLD}{rand_movie_title} "
          f"({data[rand_movie_title]['year']}), "
          f"{data[rand_movie_title]['rating']}{helper.Bcolors.ENDC}")
    print()


def fuzzy_movie_search():
    """
    Advanced search with fuzzy matching. Score cutoff is set relative low to higher the
    chances to get a wider overview of possible options. In case even that fails,
    the highest possible score match on search input is printed out as option.
    If search input is exact match with movie title, prints out the movie information.
    """
    search_input = input("Enter part of movie name: ")
    data = db_movie.get_movie_by_title(search_input)
    if data[0]:
        movie_title_db = next(iter(data[1]))
        print(f"{helper.Bcolors.BOLD}{movie_title_db}: {data[1][movie_title_db]}"
              f"{helper.Bcolors.ENDC}")
    else:
        fuzzy_data = db_movie.list_movies()
        all_matches = process.extractBests(search_input, fuzzy_data.keys(), score_cutoff=60)
        print(f"{helper.Bcolors.WARNING}The movie "
              f"{helper.Bcolors.BOLD}{search_input}{helper.Bcolors.ENDC}"
              f"{helper.Bcolors.WARNING} does not exist."
              f" Did you mean: {helper.Bcolors.ENDC}")
        if len(all_matches) > 0:
            for match, _ in all_matches:
                print(f"{helper.Bcolors.BOLD}{match}{helper.Bcolors.ENDC}")
        else:
            fallback_minimum_match = process.extractOne(search_input, fuzzy_data.keys())
            print(f"{helper.Bcolors.BOLD}{fallback_minimum_match[0]}{helper.Bcolors.ENDC}")


def get_movies_sorted_rating():
    """
    Prints out all movies in the database by rating in ascending order
    """
    data = db_movie.list_movies()
    sorted_by_rating = sorted(data.items(), key=lambda m: m[1]["rating"])
    for movie, data in sorted_by_rating:
        print(f"{helper.Bcolors.BOLD}{movie} ({data['year']}), "
              f"{data['rating']}{helper.Bcolors.ENDC}")
    print()


def get_movies_sorted_year():
    """
    Prints out all movies in the database by year of release. Order can be controlled by user input
    """
    data = db_movie.list_movies()
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
        print(f"{helper.Bcolors.BOLD}{movie} ({data['year']}), "
              f"{data['rating']}{helper.Bcolors.ENDC}")
    print()


def get_filtered_movies():
    """
    Function to print out a list for the given filter criteria. User is asked for a minimum rating,
    start and end year. If no input is given for any of those criteria, they are considered
    to not exist.
    """
    db_data = db_movie.list_movies()

    minimum_rating = ask_for_filter_input(
        f"{helper.Bcolors.GREEN}Enter a minimum rating (leave blank for no minimum):"
        f" {helper.Bcolors.ENDC}",
        float,
        f"{helper.Bcolors.FAIL}Please enter an float or leave blank!:"
        f" {helper.Bcolors.ENDC}")
    start_year = ask_for_filter_input(
        f"{helper.Bcolors.GREEN}Enter a minimum year (leave blank for no minimum year): "
        f"{helper.Bcolors.ENDC}",
        int,
        f"{helper.Bcolors.FAIL}Please enter an integer or leave blank!: "
        f"{helper.Bcolors.ENDC}")
    end_year = ask_for_filter_input(
        f"{helper.Bcolors.GREEN}Enter a maximum year (leave blank for no maximum year): "
        f"{helper.Bcolors.ENDC}",
        int,
        f"{helper.Bcolors.FAIL}Please enter an integer or leave blank!: "
        f"{helper.Bcolors.ENDC}")

    for movie, data in db_data.items():
        if minimum_rating is not None and data["rating"] < minimum_rating:
            continue
        if start_year is not None and data["year"] < start_year:
            continue
        if end_year is not None and data["year"] > end_year:
            continue

        print(f"{movie} ({data['year']}): {data['rating']}")
        print()


def ask_for_filter_input(prompt, cast_type, error_msg):
    """
    Helper-Function for the get_filtered_movies function. Works similar to helper.get_input-function;
    since for filters we also need to accept 'None' inputs and in theory don't require
    any limits, this function is specialized for that to ensure code readability.
    :param prompt: Print out to get user input
    :param cast_type: the expected input type we want to get from the user
    :param error_msg: in case casting to cast_type fails, this gets printed out
    :return: the user input converted to cast_type
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
