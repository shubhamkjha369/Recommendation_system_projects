import os
import pickle
import streamlit as st
import requests
import urllib.parse
from typing import List, Tuple, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Movie Matcher",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enable requests caching optionally to optimize API latency if the package is installed
try:
    import requests_cache
    requests_cache.install_cache('movie_cache', expire_after=86400)  # Cache responses for 24 hours
except ImportError:
    pass

# API Key Resolution (Environment fallback + Session State dynamic configuration)
if "omdb_api_key" not in st.session_state:
    st.session_state["omdb_api_key"] = os.getenv("OMDB_API_KEY", "")

# Load unified, auto-adapting CSS styles
try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Sidebar Settings
st.sidebar.markdown("## ⚙️ Configuration")
api_key_input = st.sidebar.text_input(
    "🔑 OMDb API Key (optional)",
    value=st.session_state["omdb_api_key"],
    type="password",
    help="To display movie posters, ratings, and plots, enter your OMDb API key. Get a FREE key at https://www.omdbapi.com/apikey.aspx"
)

if api_key_input != st.session_state["omdb_api_key"]:
    st.session_state["omdb_api_key"] = api_key_input
    st.rerun()

# Blending Strategy selection (Strict Match uses vector product, Broad Match uses vector average)
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ Algorithm Settings")
blend_strategy = st.sidebar.radio(
    "🔄 Blending Strategy",
    ["Strict Match (Fuzzy AND)", "Broad Match (Fuzzy OR)"],
    index=0,
    help="Strict Match ensures recommendations are highly similar to ALL selected movies (using a geometric product). Broad Match averages similarities across all selections (Fuzzy OR)."
)

# Genre Filtering options in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Genre Filters")
excluded_genres = st.sidebar.multiselect(
    "Exclude Genres",
    ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Sport", "Thriller", "War", "Western"],
    default=[],
    help="Exclude any recommended movies containing these genres."
)

required_genres = st.sidebar.multiselect(
    "Require Genres",
    ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Sport", "Thriller", "War", "Western"],
    default=[],
    help="Only show recommended movies that contain at least one of these genres."
)

# Extract and clean key (handling raw keys, copy-paste spacing, or full OMDb URLs)
raw_key = st.session_state["omdb_api_key"].strip()
VERIFYKEY = raw_key

if "apikey=" in raw_key:
    try:
        from urllib.parse import urlparse, parse_qs
        parsed_url = urlparse(raw_key)
        queries = parse_qs(parsed_url.query)
        if "apikey" in queries:
            VERIFYKEY = queries["apikey"][0].strip()
    except Exception:
        pass


def get_placeholder_svg(title: str) -> str:
    """
    Generates a high-end vector SVG placeholder card with smooth linear gradients
    calculated based on the title's character hash. This ensures a varied, gorgeous
    visual aesthetic when movie posters are missing or no API key is supplied.
    """
    # Stylized curated gradients
    gradients = [
        ("#FF512F", "#DD2476"),  # Sunset Fire
        ("#1A2980", "#26D0CE"),  # Neon Ocean
        ("#61045F", "#AA076B"),  # Purple Glow
        ("#02AAB0", "#00CDAC"),  # Emerald Teal
        ("#FF8C00", "#E52D27"),  # Cyber Orange
        ("#7000FF", "#FF007F"),  # Retro Purple
        ("#11998E", "#38EF7D"),  # Aurora Green
        ("#8A2387", "#E94057"),  # Royal Amethyst
    ]
    
    idx = sum(ord(c) for c in title) % len(gradients)
    color1, color2 = gradients[idx]
    
    # Auto-wrap long titles to fit cleanly within card dimensions
    words = title.split()
    lines = []
    current_line = []
    for word in words:
        if len(" ".join(current_line + [word])) <= 14:
            current_line.append(word)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
        
    lines = lines[:3]  # Cap at 3 lines
    text_y_start = 220 - (len(lines) - 1) * 15
    
    text_svg = ""
    for i, line in enumerate(lines):
        y = text_y_start + i * 30
        # Escape special XML chars to prevent image render breakages
        line_escaped = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        text_svg += f'<text x="150" y="{y}" fill="#ffffff" font-family="system-ui, -apple-system, sans-serif" font-size="20" font-weight="800" text-anchor="middle" letter-spacing="0.5">{line_escaped}</text>'

    svg_content = f"""
    <svg width="300" height="450" viewBox="0 0 300 450" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="grad-{idx}" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:{color1};stop-opacity:1" />
          <stop offset="100%" style="stop-color:{color2};stop-opacity:1" />
        </linearGradient>
        <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
          <feDropShadow dx="0" dy="8" stdDeviation="8" flood-opacity="0.3"/>
        </filter>
      </defs>
      <rect width="280" height="430" x="10" y="10" rx="24" fill="url(#grad-{idx})" filter="url(#shadow)" />
      
      <!-- Film Icon -->
      <g transform="translate(118, 90)" fill="#ffffff" opacity="0.25">
        <path d="M57.2,16H6.8C3,16,0,19,0,22.8v18.4C0,45,3,48,6.8,48h50.4c3.8,0,6.8-3,6.8-6.8V22.8C64,19,61,16,57.2,16z M16,40H8v-8h8V40z M16,28H8v-8h8V28z M36,40h-8v-8h8V40z M36,28h-8v-8h8V28z M56,40h-8v-8h8V40z M56,28h-8v-8h8V28z"/>
      </g>
      
      <!-- Wrapped Movie Title -->
      {text_svg}
      
      <!-- Premium Design Accents -->
      <rect x="120" y="380" width="60" height="4" rx="2" fill="#ffffff" opacity="0.3" />
      <text x="150" y="410" fill="#ffffff" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="600" text-anchor="middle" letter-spacing="2" opacity="0.5">PREMIUM MATCH</text>
    </svg>
    """
    encoded = urllib.parse.quote(svg_content.strip())
    return f"data:image/svg+xml;utf8,{encoded}"


def fetch_movie_details(movie_title: str) -> Dict[str, Any]:
    """
    Fetch comprehensive movie information (poster, rating, genres, plots, casts) from OMDb API.
    """
    default_data = {
        "poster": get_placeholder_svg(movie_title),
        "rating": "N/A",
        "year": "N/A",
        "genre": "N/A",
        "plot": "Detailed plot description is currently unavailable.",
        "director": "N/A",
        "cast": "N/A",
        "imdb_id": ""
    }
    
    if not VERIFYKEY:
        return default_data
        
    url = f"https://www.omdbapi.com/?t={urllib.parse.quote(movie_title)}&apikey={VERIFYKEY}"
    try:
        response = requests.get(url).json()
        if response.get("Response") == "True":
            poster_url = response.get("Poster")
            if not poster_url or poster_url == "N/A":
                poster_url = get_placeholder_svg(movie_title)
                
            return {
                "poster": poster_url,
                "rating": response.get("imdbRating", "N/A"),
                "year": response.get("Year", "N/A"),
                "genre": response.get("Genre", "N/A"),
                "plot": response.get("Plot", "Detailed plot description is currently unavailable."),
                "director": response.get("Director", "N/A"),
                "cast": response.get("Actors", "N/A"),
                "imdb_id": response.get("imdbID", "")
            }
        else:
            error_msg = response.get("Error", "Unknown OMDb error")
            st.sidebar.warning(f"OMDb ({movie_title}): {error_msg}")
    except Exception as e:
        st.sidebar.error(f"OMDb API Error: {str(e)}")
        
    return default_data


def recommend(movies_input: List[str], movies_df, similarity_matrix, top_n: int = 5, blend_strategy: str = "Strict Match (Fuzzy AND)", excluded_genres: List[str] = [], required_genres: List[str] = []) -> List[Dict[str, Any]]:
    """
    Calculate similarity scores for single or multiple blended input movies.
    Filters out inputs and extracts complete live details, applying genre exclusions and requirements.
    """
    try:
        indices = []
        for movie in movies_input:
            match = movies_df[movies_df['title'] == movie].index
            if len(match) > 0:
                indices.append(match[0])
                
        if not indices:
            return []
            
        # Mathematical Vector Blending (combines cosine similarities)
        if len(indices) == 1:
            sim_scores = similarity_matrix[indices[0]]
        else:
            import numpy as np
            if blend_strategy.startswith("Strict"):
                # Strict: element-wise product of similarity vectors (Geometric Product)
                sim_scores = np.prod([similarity_matrix[idx] for idx in indices], axis=0)
            else:
                # Broad: arithmetic mean across vectors
                sim_scores = np.mean([similarity_matrix[idx] for idx in indices], axis=0)
            
        # Rank similarity distances
        distances = sorted(list(enumerate(sim_scores)), reverse=True, key=lambda x: x[1])
        
        results = []
        checked_count = 0
        for item in distances:
            idx = item[0]
            movie_title = movies_df.iloc[idx].title
            
            # Prevent recommending any of the active input movies
            if movie_title in movies_input:
                continue
                
            checked_count += 1
            if checked_count > 40:  # Prevent excessive network queries
                break
                
            # Fetch details to check genres
            details = fetch_movie_details(movie_title)
            
            # Genre post-filtering (case-insensitive checks)
            movie_genres = [g.strip().lower() for g in details["genre"].split(",")]
            
            # 1. Exclude Filter
            if any(ex.lower() in movie_genres for ex in excluded_genres):
                continue
                
            # 2. Require Filter
            if required_genres and not any(req.lower() in movie_genres for req in required_genres):
                continue
                
            details["title"] = movie_title
            results.append(details)
            if len(results) >= top_n:
                break
                
        return results
        
    except Exception as e:
        st.error(f"Error compiling recommendations: {e}")
        return []


def main():
    # Brand Title Header with beautiful neon gradient
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0 1.5rem 0;">
        <h1 style="font-size: 3.8rem; margin-bottom: 0.1rem; font-weight: 800; background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🎬 MOVIE MATCHER</h1>
        <p style="font-size: 1.1rem; font-weight: 600; opacity: 0.65; letter-spacing: 2px;">CURATE YOUR PERFECT CINEMATIC JOURNEY</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Explanatory Sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🔍 How It Works")
        st.markdown("""
        Using **Natural Language Processing (NLP)**, tags like keywords, genres, casts, and plots are modeled into multi-dimensional vectors. 
        
        We calculate **Cosine Similarity** to locate items closest to your preferences.
        
        ### 🧪 Advanced features
        - **Movie Blend**: Blends vectors from multiple movies to synthesize suggestions satisfying all inputs!
        - **Live Overlays**: Displays ratings, release years, plot points, and verified IMDb entries.
        
        ---
        💻 [GitHub Repository](https://github.com/shubhamkjha369/Recommendation_system_projects/tree/main/Movie_recommender_system)
        🚀 [Streamlit Web App](https://movie-recommendation-system-skjha369.streamlit.app/)
        """)

    # Load databases (using robust script-relative path resolution to prevent folder mismatch errors on Streamlit Sharing)
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        movies_path = os.path.join(base_dir, 'model', 'movie_list.pkl')
        similarity_path = os.path.join(base_dir, 'model', 'similarity.pkl')
        
        movies = pickle.load(open(movies_path, 'rb'))
        similarity = pickle.load(open(similarity_path, 'rb'))
    except FileNotFoundError:
        st.error("Movie database matrices are missing. Please verify that 'model/movie_list.pkl' and 'model/similarity.pkl' exist in the model directory.")
        return
    except Exception as e:
        st.error(f"Failed to load similarity model: {e}")
        return

    # Select Recommendation Mode
    mode = st.radio(
        "Recommendation Mode",
        ["Single Movie Focus", "Multi-Movie Blend"],
        horizontal=True,
        label_visibility="collapsed",
        help="Single Mode focuses recommendations on one movie. Multi-Movie Blend averages similarities from multiple movies to find perfect recommendations matching all selections."
    )
    
    movie_list = sorted(movies['title'].values)
    
    # Dynamic form inputs depending on selected mode
    st.markdown("### 🎥 Input Selection")
    if mode == "Single Movie Focus":
        selected_movie = st.selectbox(
            "Select a movie you loved:",
            movie_list,
            index=None,
            placeholder="Type or select a movie title..."
        )
        selected_movies = [selected_movie] if selected_movie else []
    else:
        selected_movies = st.multiselect(
            "Select two or more movies to blend:",
            movie_list,
            placeholder="Search and select multiple movies..."
        )

    # Configuration filters
    top_n = st.slider("Number of recommendations:", min_value=3, max_value=10, value=5)
    
    # Recommendation curation button
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    if st.button('🔮 Curate Recommendations', type='primary'):
        if selected_movies:
            with st.spinner('Synthesizing vectors and curating selections...'):
                recommendations = recommend(selected_movies, movies, similarity, top_n, blend_strategy, excluded_genres, required_genres)
                
            if recommendations:
                st.markdown("---")
                if len(selected_movies) == 1:
                    st.subheader(f"✨ Curated Recommendations inspired by: {selected_movies[0]}")
                else:
                    st.subheader(f"✨ {len(recommendations)} Blended Suggestions inspired by your {len(selected_movies)} selections:")
                
                # Visual columns grid layout
                cols = st.columns(len(recommendations))
                for idx, item in enumerate(recommendations):
                    with cols[idx]:
                        with st.container():
                            # Render movie poster image
                            st.image(item["poster"], use_container_width=True)
                            
                            # Render movie titles & meta parameters
                            st.markdown(f"#### **{item['title']}**")
                            
                            # Horizontal badges layout
                            badge_row = ""
                            if item["rating"] != "N/A":
                                badge_row += f"<span class='movie-badge movie-badge-accent'>⭐ {item['rating']}</span>"
                            if item["year"] != "N/A":
                                badge_row += f"<span class='movie-badge'>{item['year']}</span>"
                            if badge_row:
                                st.markdown(f"<div>{badge_row}</div>", unsafe_allow_html=True)
                            
                            # Genre Badges
                            if item["genre"] != "N/A":
                                genres = item["genre"].split(",")
                                genre_html = "<div>"
                                for g in genres[:2]:
                                    genre_html += f"<span class='movie-badge'>{g.strip()}</span> "
                                genre_html += "</div>"
                                st.markdown(genre_html, unsafe_allow_html=True)
                            
                            # Detailed overlay accordion
                            with st.expander("📝 Details"):
                                st.markdown(f"**Director:** {item['director']}")
                                st.markdown(f"**Cast:** {item['cast']}")
                                st.markdown(f"**Plot:** {item['plot']}")
                                if item["imdb_id"]:
                                    st.markdown(f"🔗 [View on IMDb](https://www.imdb.com/title/{item['imdb_id']}/)")
            else:
                st.info("No recommendations generated. Try selecting a different title!")
        else:
            st.warning("Please choose one or more movies to generate recommendations!")


if __name__ == "__main__":
    main()