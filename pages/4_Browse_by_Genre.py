import streamlit as st
import pandas as pd
import os
from api.tmdb_client import fetch_poster

st.set_page_config(page_title="Browse by Genre", page_icon="🎭", layout="wide")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("assets/style.css")

st.title("🎭 Browse by Genre")
st.markdown("Find the best movies by category.")

@st.cache_data
def load_data():
    path = 'models/movies_clean.pkl'
    if os.path.exists(path):
        return pd.read_pickle(path)
    return None

df = load_data()

if df is not None:
    # Extract unique genres
    all_genres = set()
    for genres_str in df['genres_display']:
        if isinstance(genres_str, str):
            genres_list = [g.strip() for g in genres_str.split(',') if g.strip()]
            all_genres.update(genres_list)
    
    genres_list = sorted(list(all_genres))
    
    selected_genre = st.selectbox("Select a Genre:", genres_list)
    
    if selected_genre:
        st.subheader(f"Top Movies in {selected_genre}")
        # Filter dataframe
        filtered_df = df[df['genres_display'].str.contains(selected_genre, na=False, case=False)]
        
        # Sort by popularity
        top_movies = filtered_df.sort_values(by='popularity', ascending=False).head(20)
        
        cols = st.columns(5)
        for idx, row in top_movies.reset_index().iterrows():
            col = cols[idx % 5]
            with col:
                st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                poster = fetch_poster(row['id'])
                st.image(poster, use_container_width=True)
                st.markdown(f'<div class="movie-title">{row["title"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="star-rating">⭐ {row["vote_average"]:.1f}/10</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("Data not found. Please run preprocessing scripts first.")
