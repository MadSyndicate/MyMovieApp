# 🎬 Movie CLI Project

A Python-based CLI tool to manage a movie collection enriched with data from the OMDb API.

---

## ✨ Features

* ➕ Add movies via OMDb API (includes:

  * Publication year
  * IMDb rating
  * Poster URL (if available)
    )
* ❌ Remove movies from the database
* 🔍 Search movies:

  * Case-insensitive exact match
  * Fuzzy matching suggestions if no exact match is found
* 📊 Generate statistics about stored movies
* 📈 Create a plot (number of movies vs. rating)
* 🌐 Generate a static website displaying all movies (with posters if available)

---

## 📁 Project Structure

```
MovieProjectPart3/
│
├── src/movie_project/
│   ├── api/
│   ├── db/
│   ├── services/
│   └── main.py
│
├── static/
│   └── styles.css
├── templates/
│   └── index_template.html
├── data/
│   └── movies.db
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd MovieProjectPart3
```
---

### 2. Create and activate virtual environment (recommended)

```bash
python -m venv .venv
```

#### On Windows:

```bash
.venv\Scripts\activate
```

#### On macOS/Linux:

```bash
source .venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables (OMDb API)

This project uses the OMDb API.

Set your API key as an environment variable in a .env file. Use the .env.example.
You can register for your personal API key [under this URL](https://www.omdbapi.com/apikey.aspx).

---

## 🗄️ Database Setup

To initialize the database structure:

```bash
python -m src.movie_project.db.setup
```

This will:

* Create the SQLite database (if it does not exist)
* Initialize all required tables

---

## ✅ Sanity Check

To verify that all database operations (CRUD) are working:

```bash
python -m src.movie_project.db.sanity_checks
```

---

## 🚀 Running the CLI

```bash
python -m src.movie_project.main
```

---

## 🧪 Example CLI Operations

Depending on your implementation, the CLI may support:

* Add movie
* Remove movie
* Search movie
* Show statistics
* Generate plot
* Generate website

---

## 🌐 Generate Static Website

The tool can generate a static HTML page showing:

* Movie title
* Year
* IMDb rating
* Poster (if available)

Output will be written to the `static/` directory.

---

## 📈 Plot Generation

Creates a visualization of:

```
Number of Movies vs IMDb Rating
```

Useful for analyzing your collection.

---

## 🧠 Notes

* Movie search uses **fuzzy string matching** if no exact match is found
* Database is stored in:

  ```
  data/movies.db
  ```
* Poster URLs are optional and depend on OMDb availability

---

## 📄 License

MIT License (or your preferred license)
