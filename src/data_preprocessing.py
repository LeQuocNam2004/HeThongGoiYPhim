import pandas as pd
import json
import ast
import os

def load_data(movies_path, credits_path):
    movies = pd.read_csv(movies_path)
    credits = pd.read_csv(credits_path)
    # Merge datasets on title
    movies = movies.merge(credits, on='title')
    return movies

def extract_names(text):
    try:
        L = []
        for i in ast.literal_eval(text):
            L.append(i['name'])
        return L
    except (ValueError, SyntaxError):
        return []

def extract_top_3_cast(text):
    try:
        L = []
        counter = 0
        for i in ast.literal_eval(text):
            if counter < 3:
                L.append(i['name'])
                counter += 1
            else:
                break
        return L
    except (ValueError, SyntaxError):
        return []

def fetch_director(text):
    try:
        L = []
        for i in ast.literal_eval(text):
            if i['job'] == 'Director':
                L.append(i['name'])
                break
        return L
    except (ValueError, SyntaxError):
        return []

def preprocess_data(movies):
    # Select important columns
    # id, title, overview, genres, keywords, cast, crew, vote_average
    movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew', 'vote_average', 'release_date', 'popularity']]
    movies.rename(columns={'movie_id': 'id'}, inplace=True)
    
    # Drop rows with missing values
    movies.dropna(subset=['overview'], inplace=True)

    # Convert stringified JSON to lists
    movies['genres'] = movies['genres'].apply(extract_names)
    movies['keywords'] = movies['keywords'].apply(extract_names)
    movies['cast'] = movies['cast'].apply(extract_top_3_cast)
    movies['crew'] = movies['crew'].apply(fetch_director)
    
    # Convert overview string to list
    movies['overview'] = movies['overview'].apply(lambda x: x.split() if isinstance(x, str) else [])

    # Remove spaces from names to create unique tags
    movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

    # Create the tags column
    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

    # New dataframe with necessary columns
    new_df = movies[['id', 'title', 'tags', 'genres', 'vote_average', 'release_date', 'popularity']].copy()
    
    # Join tags back to a single string and lowercase
    new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
    new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())
    
    # Format genres for display purposes
    new_df['genres_display'] = movies['genres'].apply(lambda x: ", ".join([i for i in x]))
    new_df['overview'] = movies['overview'].apply(lambda x: " ".join(x))
    
    return new_df

def save_preprocessed_data(df, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_pickle(output_path)
    print(f"Preprocessed data saved to {output_path}")

if __name__ == "__main__":
    movies_file = 'd:/IT_D/Python/movie-recommendation-system/data/tmdb_5000_movies.csv'
    credits_file = 'd:/IT_D/Python/movie-recommendation-system/data/tmdb_5000_credits.csv'
    output_file = 'd:/IT_D/Python/movie-recommendation-system/models/movies_clean.pkl'
    
    if os.path.exists(movies_file) and os.path.exists(credits_file):
        print("Loading data...")
        movies_raw = load_data(movies_file, credits_file)
        print("Preprocessing data...")
        movies_clean = preprocess_data(movies_raw)
        print("Saving data...")
        save_preprocessed_data(movies_clean, output_file)
    else:
        print("Dataset files not found. Please ensure they are in the data/ folder.")
