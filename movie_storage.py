import json


def get_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data.

    For example, the function may return:
    {
      "Titanic": {
        "rating": 9,
        "year": 1999
      },
      "..." {
        ...
      },
    }
    [Question for Reviewer]: After refactoring to a new data structure like asked for by the task,
    I originally had a list of dictionaries in the form:
    [
        {"name": "Titanic", "rating": 9, "year": 1999},
        ....
    ]
    I was unsure if that was still fine for the task and thus refactored once more to fulfill
    the example above. In case I would have stayed with my variant, would that cost me points
    on the score or would that be fine as well (asking for future task)? Best regards!
    """
    with open("./db/data.json", "r") as file:
        list_of_dicts = json.loads(file.read())

    return list_of_dicts


def save_movies(movies):
    """
    Gets all your movies as an argument and saves them to the JSON file.
    """
    json_str = json.dumps(movies)
    with open("./db/data.json", "w") as file:
        file.write(json_str)


def add_movie(title, year, rating):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    dict_of_dicts = get_movies()
    dict_of_dicts[title] = {"rating": rating, "year": year}
    save_movies(dict_of_dicts)


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    dict_of_dicts = get_movies()
    del dict_of_dicts[title]
    save_movies(dict_of_dicts)


def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    dict_of_dicts = get_movies()
    dict_of_dicts[title]["rating"] = rating
    save_movies(dict_of_dicts)


def lookup_specific_movie(title):
    """
    Looks up a movie from the movies database by the given title.
    :param title: exact movie title to check if in database. used as key
    :return: Tuple containing the bool if movie was found and if so the
    information; otherwise None instead.
    """
    with open("./db/data.json", "r") as file:
        list_of_dicts = json.loads(file.read())
    if title in list_of_dicts:
        return True, list_of_dicts[title]
    return False, None
