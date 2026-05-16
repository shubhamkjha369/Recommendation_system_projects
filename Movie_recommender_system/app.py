import os
import pickle
import streamlit as st
import requests
import requests_cache
from typing import List, Tuple
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Movie Matcher",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enable caching to avoid exceeding API limits
requests_cache.install_cache('movie_cache', expire_after=86400)  # Cache for 24 hours

# OMDb API Key from environment variable
VERIFYKEY = os.getenv("OMDB_API_KEY")

# Check if API key is available
if not VERIFYKEY:
    st.error("OMDb API Key not found. Please set OMDB_API_KEY in your .env file.")

# Custom CSS for enhanced styling with dark mode support
def local_css():
    st.markdown("""
    <style>
    /* Base styles with dark mode support */
    :root {
        --bg-primary: #f4f4f7;
        --bg-secondary: #ffffff;
        --text-primary: #2c3e50;
        --text-secondary: #34495e;
        --accent-color: #3498db;
        --hover-color: #2980b9;
    }

    [data-theme="dark"] {
        --bg-primary: #121212;
        --bg-secondary: #1e1e1e;
        --text-primary: #e0e0e0;
        --text-secondary: #b0b0b0;
        --accent-color: #4ecdc4;
        --hover-color: #45b7aa;
    }

    /* Global Styles */
    .stApp {
        background-color: var(--bg-primary);
        color: var(--text-primary);
        font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    }

    /* Header Styles */
    h1, h2, h3 {
        color: var(--text-primary);
        font-weight: 700;
    }

    /* Recommendation Card Styles */
    .recommendation-card {
        background-color: var(--bg-secondary);
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 15px;
        margin: 10px 0;
        transition: all 0.3s ease;
        border: 1px solid transparent;
    }

    .recommendation-card:hover {
        transform: scale(1.03);
        border-color: var(--accent-color);
    }

    /* Sidebar Styles */
    .css-1aumxhk {
        background-color: var(--bg-secondary);
    }

    /* Button Styles */
    .stButton > button {
        background-color: var(--accent-color) !important;
        color: white !important;
        border: none;
        transition: background-color 0.3s ease;
    }

    .stButton > button:hover {
        background-color: var(--hover-color) !important;
    }

    /* Selectbox Styles */
    .stSelectbox > div > div {
        background-color: var(--bg-secondary);
        color: var(--text-primary);
    }

    /* Image Styles */
    .recommendation-image {
        border-radius: 8px;
        object-fit: cover;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Responsive Adjustments */
    @media (max-width: 768px) {
        .recommendation-card {
            margin: 5px 0;
            padding: 10px;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def fetch_poster(movie_title: str) -> str:
    """
    Fetch movie poster from OMDb API with improved error handling.

    Args:
        movie_title (str): Title of the movie

    Returns:
        str: URL of the movie poster
    """
    # Only attempt to fetch poster if API key is available
    if not VERIFYKEY:
        return "https://via.placeholder.com/500x750?text=No+Poster"

    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={VERIFYKEY}"

    try:
        response = requests.get(url).json()
        if response.get("Response") == "True":
            return response.get("Poster", "https://via.placeholder.com/500x750?text=No+Poster")
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except Exception as e:
        st.error(f"Error fetching poster for {movie_title}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Poster"


def recommend(movie: str, movies, similarity) -> Tuple[List[str], List[str]]:
    """
    Recommend top 5 similar movies with robust error handling.

    Args:
        movie (str): Base movie to find recommendations for
        movies (pd.DataFrame): DataFrame of movies
        similarity (np.ndarray): Similarity matrix

    Returns:
        Tuple of recommended movie names and their poster URLs
    """
    try:
        # Find the index of the selected movie
        movie_indices = movies[movies['title'] == movie].index

        if len(movie_indices) == 0:
            st.warning(f"Movie '{movie}' not found in the database.")
            return [], []

        index = movie_indices[0]

        # Get similarity distances and sort
        distances = sorted(list(enumerate(similarity[index])),
                           reverse=True,
                           key=lambda x: x[1])

        recommended_movie_names = []
        recommended_movie_posters = []

        # Fetch top 5 recommendations (excluding the original movie)
        for i in distances[1:6]:
            movie_title = movies.iloc[i[0]].title
            recommended_movie_names.append(movie_title)
            recommended_movie_posters.append(fetch_poster(movie_title))

        return recommended_movie_names, recommended_movie_posters

    except Exception as e:
        st.error(f"Error in recommendation process: {e}")
        return [], []


def main():
    """
    Main Streamlit application function with improved UI and dark mode
    """
    # Apply custom CSS
    local_css()

    # Dark mode toggle in sidebar
    st.sidebar.header("🌓 Theme")
    dark_mode = st.sidebar.toggle("Dark Mode", value=False)

    # Apply dark mode if selected
    css_file = "dark.css" if dark_mode else "light.css"
    try:
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"CSS file '{css_file}' not found.")

    # Title and description
    st.markdown("""
    # 🎬 Movie Matcher
    #### Discover Your Next Favorite Film
    """)

    # Sidebar information
    with st.sidebar:
        st.header("🔍 How It Works")
        st.markdown("""
        - Select a movie you enjoyed
        - Click 'Find Recommendations'
        - Discover similar cinematic gems!

        💡 Smart recommendations based on movie similarities.
        """)

    # Load movie dataset and similarity matrix
    try:
        movies = pickle.load(open('model/movie_list.pkl', 'rb'))
        similarity = pickle.load(open('model/similarity.pkl', 'rb'))
    except FileNotFoundError:
        st.error(
            "Movie database files not found. Please ensure 'model/movie_list.pkl' and 'model/similarity.pkl' exist.")
        return
    except Exception as e:
        st.error(f"Error loading movie database: {e}")
        return

    # Movie selection with improved styling
    st.markdown("### 🎥 Choose Your Movie")
    movie_list = sorted(movies['title'].values)
    selected_movie = st.selectbox(
        "Select a movie that you loved",
        movie_list,
        index=None,
        placeholder="Browse and select a movie..."
    )

    # Recommendation button with enhanced interaction
    if st.button('🔮 Find Recommendations', type='primary'):
        if selected_movie:
            with st.spinner('Curating your perfect movie recommendations...'):
                recommended_movie_names, recommended_movie_posters = recommend(selected_movie, movies, similarity)

            # Display the base selected movie section
            st.subheader(f"Recommendations inspired by {selected_movie}")

            # Display recommended movies in a more interactive grid
            if recommended_movie_names:
                cols = st.columns(5)
                for idx, (name, poster) in enumerate(zip(recommended_movie_names, recommended_movie_posters)):
                    with cols[idx]:
                        with st.container(border=True):
                            st.image(poster, use_container_width=True,
                                     output_format='PNG',
                                     caption=name)
            else:
                st.info("No recommendations found. Try another movie!")
        else:
            st.warning("Please select a movie to get recommendations!")


if __name__ == "__main__":
    main()