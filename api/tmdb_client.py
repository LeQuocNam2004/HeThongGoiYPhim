import requests
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('TMDB_API_KEY')

@st.cache_data(ttl=3600)
def fetch_poster(movie_id):
    if not API_KEY or API_KEY == 'your_tmdb_api_key_here':
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except Exception as e:
        print(f"Error fetching poster: {e}")
    return "https://via.placeholder.com/500x750?text=No+Poster+Available"

@st.cache_data(ttl=3600)
def fetch_movie_details(movie_id):
    if not API_KEY or API_KEY == 'your_tmdb_api_key_here':
        return None
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching movie details: {e}")
    return None

@st.cache_data(ttl=3600)
def fetch_trending_movies(page=1):
    if not API_KEY or API_KEY == 'your_tmdb_api_key_here':
        return []
    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={API_KEY}&page={page}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('results', [])
    except Exception as e:
        print(f"Error fetching trending: {e}")
    return []

@st.cache_data(ttl=3600)
def fetch_top_rated_movies(page=1):
    if not API_KEY or API_KEY == 'your_tmdb_api_key_here':
        return []
    url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}&language=en-US&page={page}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('results', [])
    except Exception as e:
        print(f"Error fetching top rated: {e}")
    return []

@st.cache_data(ttl=3600)
def fetch_movie_trailer(movie_id):
    if not API_KEY or API_KEY == 'your_tmdb_api_key_here':
        return None
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json().get('results', [])
            for video in results:
                if video.get('site') == 'YouTube' and video.get('type') == 'Trailer':
                    return f"https://www.youtube.com/watch?v={video.get('key')}"
    except Exception as e:
        print(f"Error fetching trailer: {e}")
    return None

