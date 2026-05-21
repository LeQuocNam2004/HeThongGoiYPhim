import streamlit as st
import pandas as pd
import pickle
import os
from api.tmdb_client import fetch_poster, fetch_movie_details, fetch_movie_trailer

# Set page config
st.set_page_config(
    page_title="Movieflix - Recommendation System",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State for Watchlist
if 'watchlist' not in st.session_state:
    st.session_state['watchlist'] = []

# Load CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("assets/style.css")

# Load models
@st.cache_resource
def load_models():
    movies_path = 'models/movies_clean.pkl'
    sim_path = 'models/similarity.pkl'
    if os.path.exists(movies_path) and os.path.exists(sim_path):
        movies = pd.read_pickle(movies_path)
        with open(sim_path, 'rb') as f:
            similarity = pickle.load(f)
        return movies, similarity
    return None, None

movies, similarity = load_models()

def recommend(movie_title):
    try:
        movie_index = movies[movies['title'] == movie_title].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_movies = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].id
            poster = fetch_poster(movie_id)
            details = fetch_movie_details(movie_id)
            trailer = fetch_movie_trailer(movie_id)
            title = movies.iloc[i[0]].title
            confidence = i[1] * 100
            
            recommended_movies.append({
                'title': title,
                'poster': poster,
                'genres': movies.iloc[i[0]].get('genres_display', ''),
                'confidence': confidence,
                'id': movie_id,
                'details': details,
                'trailer': trailer
            })
        return recommended_movies
    except IndexError:
        return []

def add_to_watchlist(movie):
    if not any(m['id'] == movie['id'] for m in st.session_state['watchlist']):
        st.session_state['watchlist'].append(movie)
        st.toast(f"Added {movie['title']} to Watchlist! ❤️")
    else:
        st.toast(f"{movie['title']} is already in Watchlist! ℹ️")

st.title("🎥 Welcome to Movieflix")
st.markdown("Discover your next favorite movie using our AI-powered recommendation engine.")

if movies is not None:
    # Search autocomplete
    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list,
        index=None,
        placeholder="Search for a movie..."
    )

    if st.button("🔍 Recommend", use_container_width=True):
        if selected_movie:
            with st.spinner("Finding similar movies..."):
                recommendations = recommend(selected_movie)
                
                if recommendations:
                    st.subheader(f"Because you watched **{selected_movie}**:")
                    cols = st.columns(5)
                    
                    for idx, col in enumerate(cols):
                        with col:
                            rec = recommendations[idx]
                            
                            # Movie Card
                            st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                            st.image(rec['poster'], use_container_width=True)
                            st.markdown(f'<div class="movie-title" title="{rec["title"]}">{rec["title"]}</div>', unsafe_allow_html=True)
                            if rec['genres']:
                                st.markdown(f'<div class="movie-genres">{rec["genres"]}</div>', unsafe_allow_html=True)
                            
                            if rec['details'] and 'vote_average' in rec['details']:
                                rating = rec['details']['vote_average']
                                st.markdown(f'<div class="star-rating">⭐ {rating:.1f}/10</div>', unsafe_allow_html=True)
                            
                            st.progress(int(rec['confidence']), text=f"Match: {rec['confidence']:.1f}%")
                            
                            if st.button(f"❤️ Add", key=f"wl_{rec['id']}_{idx}", use_container_width=True):
                                add_to_watchlist(rec)
                                
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Expander for more details
                            with st.expander("More Details & Trailer"):
                                if rec['details']:
                                    st.write(rec['details'].get('overview', 'No overview available.'))
                                if rec['trailer']:
                                    st.video(rec['trailer'])
                                else:
                                    st.write("No trailer available on YouTube.")
                else:
                    st.warning("Could not find recommendations for this movie.")
else:
    st.error("Model files not found. Please run the preprocessing scripts first.")
