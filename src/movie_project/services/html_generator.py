# in case no poster url for movie in db
NA_PIC_SOURCE = ("https://upload.wikimedia.org/wikipedia/commons"
                 "/1/14/No_Image_Available.jpg?_=20200913095930")

def generate_html_from_template(template, title, movies):
    """generating HTML from template with movie data from database"""
    movie_items = []

    for name, data in movies.items():
        movie_html = f"""
            <li>
                <div class="movie">
                    <a href="https://www.imdb.com/title/{data.get('imdb_id')}" target="_blank">
                        <img class="movie-poster" 
                            src="{data.get('poster_url') or NA_PIC_SOURCE}" 
                            title="{data.get('user_notes')}" 
                            alt="{name}">
                    </a>
                    <div class="movie-title">{name}</div>
                    <div class="movie-year">{data['year']}</div>
                    <div class="movie-rating">
                        Internet Movie Database Rating: {data.get('rating') or 'N/A'}</div>
                </div>
            </li>
            """
        movie_items.append(movie_html.strip())

    movie_grid_html = "\n".join(movie_items)

    result = template.replace("__TEMPLATE_TITLE__", title)
    result = result.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html)

    return result
