import streamlit as st
from api.tmdb_client import fetch_trending_movies, fetch_poster

st.set_page_config(page_title="Trending Movies", page_icon="🔥", layout="wide")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("assets/style.css")

st.title("🔥 Trending This Week")
st.markdown("Discover the most popular movies right now.")

movies = fetch_trending_movies(page=1)

if movies:
    cols = st.columns(5)
    for idx, movie in enumerate(movies[:20]): # Show top 20
        col = cols[idx % 5]
        with col:
            st.markdown('<div class="movie-card">', unsafe_allow_html=True)
            poster = f"https://image.tmdb.org/t/p/w500/{movie.get('poster_path')}" if movie.get('poster_path') else "https://via.placeholder.com/500x750?text=No+Poster+Available"
            st.image(poster, use_container_width=True)
            st.markdown(f'<div class="movie-title">{movie.get("title", "Unknown")}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="movie-genres">Rating: {movie.get("vote_average", 0):.1f}/10</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Please set your TMDb API key in `.env` to view trending movies.")
