import streamlit as st

st.set_page_config(page_title="My Watchlist", page_icon="❤️", layout="wide")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("assets/style.css")

st.title("❤️ My Watchlist")
st.markdown("Movies you want to watch later.")

if 'watchlist' not in st.session_state:
    st.session_state['watchlist'] = []

if not st.session_state['watchlist']:
    st.info("Your watchlist is empty! Go to the Home page and add some movies.")
else:
    if st.button("Clear Watchlist"):
        st.session_state['watchlist'] = []
        st.rerun()

    cols = st.columns(5)
    for idx, movie in enumerate(st.session_state['watchlist']):
        col = cols[idx % 5]
        with col:
            st.markdown('<div class="movie-card">', unsafe_allow_html=True)
            st.image(movie.get('poster', 'https://via.placeholder.com/500x750'), use_container_width=True)
            st.markdown(f'<div class="movie-title">{movie.get("title", "Unknown")}</div>', unsafe_allow_html=True)
            if movie.get('genres'):
                st.markdown(f'<div class="movie-genres">{movie["genres"]}</div>', unsafe_allow_html=True)
            
            # Remove button
            if st.button("❌ Remove", key=f"remove_{movie['id']}_{idx}", use_container_width=True):
                st.session_state['watchlist'] = [m for m in st.session_state['watchlist'] if m['id'] != movie['id']]
                st.rerun()
                
            st.markdown('</div>', unsafe_allow_html=True)
