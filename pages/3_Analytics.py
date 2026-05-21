import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("assets/style.css")

st.title("📊 Dataset Analytics")
st.markdown("Insights into the movie dataset.")

@st.cache_data
def load_data():
    path = 'models/movies_clean.pkl'
    if os.path.exists(path):
        return pd.read_pickle(path)
    return None

df = load_data()

if df is not None:
    st.markdown("### Top 10 Movies by Popularity")
    top_popular = df.sort_values(by='popularity', ascending=False).head(10)
    fig = px.bar(top_popular, x='popularity', y='title', orientation='h', color='popularity',
                 color_continuous_scale='Reds', title="Most Popular Movies")
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Top 10 Movies by Vote Average")
    top_rated = df[df['vote_average'] > 0].sort_values(by='vote_average', ascending=False).head(10)
    fig2 = px.bar(top_rated, x='vote_average', y='title', orientation='h', color='vote_average',
                 color_continuous_scale='Reds', title="Highest Rated Movies")
    fig2.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.error("Data not found. Please run preprocessing scripts first.")
