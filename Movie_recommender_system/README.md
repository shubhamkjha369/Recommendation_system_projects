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

check out this project running directly on hugigng face: https://huggingface.co/spaces/shubhammjha/movie-recommender-system

📝 Problem Statement:

With the overwhelming number of movies released every year, finding a movie that matches a user’s taste can be difficult and time-consuming. Users often struggle to discover new movies similar to the ones they already like.
The goal of this project is to build an intelligent movie recommendation system that:
Suggests movies based on user preferences or previously liked movies.
Helps users discover hidden gems and relevant content without manually searching through thousands of titles.
Provides recommendations quickly through an interactive web interface.
This system leverages data preprocessing, similarity metrics, and machine learning algorithms to deliver personalized movie suggestions, making the movie-watching experience more enjoyable and efficient.

🎬 Movie Recommendation System

A Movie Recommendation System built using Python and Streamlit that suggests movies based on user preferences and similarity metrics. This project scrapes movie data, processes it, and recommends movies similar to the ones you like.

🛠 Features

Personalized Recommendations: Suggests movies based on user input or favorite movies.

Web Scraping: Uses BeautifulSoup4 and requests to fetch movie data.

Data Processing: Utilizes pandas and numpy for handling and transforming data.

Similarity Computation: Employs scikit-learn for building recommendation models.

Caching: requests_cache improves scraping performance by storing responses.

Environment Configuration: Supports .env files for API keys or configuration.

Web App: Streamlit interface for easy movie selection and viewing recommendations.

📦 Installation

1. Clone the repository:
   git clone https://github.com/shubhammjha/Data-Science.git
   cd projects/movie-recommender-system
2. Create a virtual environment (optional but recommended):
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
3. Install dependencies:
   pip install -r requirements.txt
4. Add your configuration (if any) in a .env file
   # Example
   API_KEY=your_api_key_here

🚀 Usage

Run the Streamlit app:
streamlit run app.py

Enter your favorite movie or preferences.

Get a list of recommended movies instantly.

Explore additional details for each movie (if implemented).

🗂 Project Structure
movie-recommendation-system/
│

├─model

├─app.py

├─dark.css

├─light.css

├─movie_cache.sqlite

├─qodana.yaml

├─requirements.txt

├─Dockerfile

└─README.md

🧰 Dependencies

streamlit – Web app framework

pandas – Data manipulation

numpy – Numerical computations

scikit-learn – Machine learning & similarity metrics

joblib – Model persistence

requests – HTTP requests

beautifulsoup4 – Web scraping

lxml – Parsing HTML/XML

requests_cache – Caching HTTP requests

dotenv – Environment variable management

📈 How It Works

Load movie dataset (or scrape from a source).

Preprocess movie features (genres, keywords, ratings, etc.).

Compute similarity scores using machine learning models.

Take user input and recommend top N similar movies.

Display recommendations in a Streamlit app.

📄 License

This project is open-source and available under the MIT License. See LICENSE
 for details.

🙌 Contribution

Contributions, issues, and feature requests are welcome!

Fork the repository

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some feature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

⭐ Acknowledgements

Inspired by popular movie recommendation systems

Python libraries: Streamlit, Scikit-learn, Pandas, NumPy

Web scraping using BeautifulSoup4 and requests
