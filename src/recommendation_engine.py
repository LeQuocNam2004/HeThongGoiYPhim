import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

def create_similarity_matrix(df_path, output_path):
    print(f"Loading preprocessed data from {df_path}")
    movies = pd.read_pickle(df_path)
    
    print("Initializing CountVectorizer")
    # Using max_features to limit the dimensions and avoid memory issues on large datasets
    cv = CountVectorizer(max_features=5000, stop_words='english')
    
    print("Computing vectors")
    vectors = cv.fit_transform(movies['tags']).toarray()
    
    print("Computing cosine similarity")
    similarity = cosine_similarity(vectors)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"Saving similarity matrix to {output_path}")
    with open(output_path, 'wb') as f:
        pickle.dump(similarity, f)
        
    print("Done!")

if __name__ == "__main__":
    input_file = 'd:/IT_D/Python/movie-recommendation-system/models/movies_clean.pkl'
    output_file = 'd:/IT_D/Python/movie-recommendation-system/models/similarity.pkl'
    
    if os.path.exists(input_file):
        create_similarity_matrix(input_file, output_file)
    else:
        print(f"Input file {input_file} not found. Please run data_preprocessing.py first.")
