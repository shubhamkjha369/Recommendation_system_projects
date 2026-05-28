---
title: Movie Recommender System
emoji: 📈
colorFrom: green
colorTo: green
sdk: streamlit
sdk_version: 1.44.1
app_file: app.py
pinned: false
---

<div align="center">

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/shubhamkjha369/Recommendation_system_projects/tree/main/Movie_recommender_system)
[![Streamlit App](https://img.shields.io/badge/Streamlit-Web%20App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://movie-recommendation-system-skjha369.streamlit.app/)

</div>

📝 Problem Statement:

With the overwhelming number of movies released every year, finding a movie that matches a user’s taste can be difficult and time-consuming. Users often struggle to discover new movies similar to the ones they already like.
The goal of this project is to build an intelligent movie recommendation system that:
- Suggests movies based on user preferences or previously liked movies.
- Helps users discover hidden gems and relevant content without manually searching through thousands of titles.
- Provides recommendations quickly through an interactive web interface.

This system leverages data preprocessing, similarity metrics, and content-based filtering algorithms to deliver personalized movie suggestions, making the movie-watching experience more enjoyable and efficient.

🎬 Movie Recommendation System

A Movie Recommendation System built using Python and Streamlit that suggests movies based on user preferences and similarity metrics. The system uses precomputed content similarity matrices generated using natural language processing (NLP) to recommend movies similar to the ones you select.

🛠 Features

- **Personalized Recommendations**: Suggests movies based on user input or favorite movies.
- **Advanced Blended Search**: Select and blend multiple movies to get recommendation results matching all your selections.
- **Interactive Details**: Shows movie posters, IMDb ratings, year of release, genres, director, cast, and detailed plot descriptions from OMDb API.
- **Beautiful Custom SVG Placeholders**: Automatically generates gorgeous custom linear gradient SVG posters based on the movie's title hash if the OMDb poster is unavailable.
- **Robust Caching**: Automatically caches OMDb API queries to minimize external network requests.
- **Responsive Theme Switching**: Built-in support for responsive modern cinematic dark and clean light modes.

📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/shubhamkjha369/Recommendation_system_projects.git
   cd Movie_recommender_system
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Add your OMDb configuration in a `.env` file (optional):
   ```env
   OMDB_API_KEY=your_api_key_here
   ```

🚀 Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

1. Enter your favorite movie or select one from the dropdown.
2. Toggle "Multi-Movie Blend" to combine recommendations of multiple movies.
3. Click "🔮 Find Recommendations" to discover similar cinematic gems instantly!
4. Expand any movie container to view details (rating, plot, cast, and more).

🗂 Project Structure

```text
Movie_recommender_system/
│
├── model/
│   ├── movie_list.pkl    # Preprocessed movie DataFrame containing movie_id, title, and tags
│   └── similarity.pkl    # Precomputed cosine similarity matrix (184 MB)
│
├── app.py                # Main Streamlit web application
├── dark.css              # Custom styling for modern cinematic dark mode
├── light.css             # Custom styling for clean light mode
├── requirements.txt      # Project requirements
├── Dockerfile            # Containerization instructions
└── README.md             # Project documentation
```

🧰 Active Dependencies

- **streamlit** – Interactive web app framework
- **pandas** – Data manipulation & pickle dataframe extraction
- **numpy** – Similarity matrix processing
- **scikit-learn** – Utilized offline for TF-IDF vectorization and cosine similarity
- **requests** – Live OMDb API poster and details fetching
- **requests_cache** – Offline caching of API requests (stores in local sqlite database)
- **python-dotenv** – local environment configuration loading

📄 License

This project is open-source and available under the MIT License. See LICENSE for details.

🙌 Contribution

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

⭐ Acknowledgements

- Inspired by popular movie recommendation systems.
- Python libraries: Streamlit, Scikit-learn, Pandas, NumPy.
- API provider: OMDb API for high-quality movie metadata and poster rendering.
