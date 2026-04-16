import matplotlib.pyplot as plt
from src.movie_project.db import movie_storage_sql as db_sql
from src.movie_project.services import html_generator
from pathlib import Path
import src.movie_project.services.helper as helper

BASE_DIR = Path(__file__).resolve().parents[3]
TEMPLATE_PATH = BASE_DIR / "_template" / "index_template.html"
OUTPUT_PATH = BASE_DIR / "_static" / "index.html"

def draw_rating_histogram_to_file():
    """
    Function to print a simple histogram of movie rating and number of movies
    in the database in a .png-file.
    """
    data = db_sql.list_movies()
    file_name_input = input(f"{helper.Bcolors.GREEN}Enter a file name to "
                            f"put the histogram: {helper.Bcolors.ENDC}")
    rating_list = [m["rating"] for m in data.values()]
    plt.hist(rating_list)
    plt.title("Histogram of movie ratings")
    plt.xlabel("Rating")
    plt.ylabel("Number of movies")
    plt.savefig(file_name_input + '.png')
    print(f"created file {helper.Bcolors.BOLD}{file_name_input}.png{helper.Bcolors.ENDC}")
    print()


def generate_website():
    movie_data = db_sql.list_movies()
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as fr:
        template = fr.read()
        html_output = html_generator.generate_html_from_template(template, "Masterschool's Movie App", movie_data)
        with open(OUTPUT_PATH, "w") as fw:
            fw.write(html_output)
        print("Website generated!")

