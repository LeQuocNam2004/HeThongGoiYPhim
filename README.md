# Movie Recommendation System

A modern, Netflix-style movie recommendation system built with Python, Streamlit, and Machine Learning (Content-Based Filtering).

## Features
- **Content-Based Filtering**: Uses `CountVectorizer` and Cosine Similarity to recommend similar movies based on genres, overview, keywords, cast, and crew.
- **Modern UI**: Netflix-style dark theme with responsive movie cards, custom CSS, and animations.
- **TMDb Integration**: Fetches real-time movie posters and details via the TMDb API.
- **Multi-page Architecture**: Home, Trending, Top Rated, and Analytics pages.
- **Data Visualization**: Interactive charts using Plotly.

## Installation

1. Clone the repository and navigate into the folder.
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the environment variables:
   - Copy `.env.example` to `.env`
   - Add your TMDb API Key to `.env`: `TMDB_API_KEY=your_key_here`
4. Prepare data:
   - Put `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` in the `data/` folder.
   - Run the data preprocessing script to generate the models:
     ```bash
     python src/data_preprocessing.py
     ```
5. Run the application:
   ```bash
   streamlit run app.py
   ```

## Docker
To run using Docker:
```bash
docker build -t movie-recommender .
docker run -p 8501:8501 --env-file .env movie-recommender
```
