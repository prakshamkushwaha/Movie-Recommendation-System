import streamlit as st
import pickle
import os

st.set_page_config(page_title="Movie Recommender", layout="centered")

st.title("🎬 Movie Recommendation System")
st.write("A Content-Based Recommender System using TF-IDF & Cosine Similarity.")

# Check if pickle files exist in the directory
if not os.path.exists('movies.pkl') or not os.path.exists('similarity.pkl'):
    st.error("Error: `movies.pkl` or `similarity.pkl` not found in this folder!")
    st.info("Make sure both .pkl files are placed in the same directory as app.py.")
    st.stop()

# Load files
with open('movies.pkl', 'rb') as f:
    movies_df = pickle.load(f)

with open('similarity.pkl', 'rb') as f:
    similarity_matrix = pickle.load(f)

def recommend(item_name, top_n=5):
    idx = movies_df[movies_df['title'] == item_name].index[0]
    sim_scores = list(enumerate(similarity_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sim_scores[1:top_n+1]]
    return movies_df[['title', 'genre', 'release_year']].iloc[top_indices]

# Dropdown to select item
selected_movie = st.selectbox(
    "Choose a movie to get recommendations:",
    movies_df['title'].values
)

# Button to trigger recommendation
if st.button("Get Recommendations"):
    results = recommend(selected_movie, top_n=5)
    
    st.subheader(f"Recommendations based on '{selected_movie}':")
    for i, row in results.reset_index().iterrows():
        st.markdown(f"**{i+1}. {row['title']}** — *{row['genre']}* ({row['release_year']})")