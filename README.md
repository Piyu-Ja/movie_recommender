https://movierecommender-pwtzxas67w3nk9u8xmkdse.streamlit.app/

# Movie Recommender System

Experience a new way to discover movies with this intelligent, interactive Movie Recommender System.  
Try the live app: https://movierecommender-pwtzxas67w3nk9u8xmkdse.streamlit.app/

---

## Project Overview

This project is a robust, end-to-end movie recommendation platform that combines advanced data processing, natural language matching, and cloud-based machine learning models. Built with Python, Streamlit, and scikit-learn, it offers a seamless and visually engaging experience for users to explore and find movies tailored to their tastes.

Unlike basic recommenders, this system leverages both cosine and Euclidean similarity metrics, fuzzy text matching, and real-time poster fetching to deliver highly relevant and visually rich suggestions. All models and data are managed via Hugging Face, ensuring reliability and easy updates.

---

## What Makes This Project Unique?

- **Hybrid Similarity Ranking**: Uses both cosine and Euclidean similarity for multi-stage, high-precision recommendations.
- **Fuzzy Search & Matching**: Accepts any user input—movie titles, keywords, or even vague phrases—and intelligently resolves it to the closest movie using exact, substring, and fuzzy matching.
- **Cloud-Native Model Management**: All model files are stored and loaded directly from Hugging Face, ensuring the app is always up-to-date and easy to deploy anywhere.
- **Interactive Exploration**: Users can recursively explore recommendations, creating a personalized discovery journey.
- **Visual Appeal**: Movie posters are fetched live from TMDB, making the interface engaging and easy to use.
- **No Local Setup Hassles**: No need to manage local files or Google Drive links; everything is handled in the cloud.

---

## Features

- **Flexible, Intelligent Search**: Enter any text and the app finds the closest movie match, even with typos or partial names.
- **Multi-Stage Recommendation Engine**: 
  - First, finds the top 25 similar movies using cosine similarity.
  - Then, re-ranks these using Euclidean similarity to present the top 5 most relevant suggestions.
- **Rich Visuals**: Each recommendation includes a movie poster, fetched in real-time.
- **Recursive Recommendations**: Click on any recommended movie to get a new set of suggestions based on that movie.
- **Robust Error Handling**: Handles missing posters, network issues, and invalid inputs gracefully.
- **Session Memory**: Remembers your navigation and choices for a smooth, uninterrupted experience.

---

## How It Works

### Data & Model Preparation

- **Data Sources**: Uses the TMDB 5000 movies and credits datasets.
- **Data Processing**: 
  - Merges movie and credit data.
  - Extracts and cleans genres, keywords, cast, and crew (director).
  - Combines all relevant text into a single "tags" field for each movie.
- **Feature Engineering**: 
  - Uses `CountVectorizer` to create a bag-of-words representation of each movie.
  - Computes cosine similarity and Euclidean similarity matrices for all movies.
- **Model Storage**: 
  - All processed data and similarity matrices are saved as pickle files and uploaded to Hugging Face for cloud access.

### App Architecture

- **Model Loading**: On startup, the app downloads the latest model files from Hugging Face using `huggingface_hub`.
- **User Input**: Users enter any text; the app resolves it to the best-matching movie using a combination of exact, substring, and fuzzy matching.
- **Recommendation Logic**: 
  - Finds the top 25 similar movies (cosine similarity).
  - Re-ranks these using Euclidean similarity to select the top 5.
- **Display**: Shows recommendations with titles and posters. Users can click to explore further recommendations.
- **Poster Fetching**: Uses the TMDB API to fetch high-quality posters for each movie.

---

## Technologies Used

- **Python**: Core programming language.
- **Streamlit**: For building the interactive web interface.
- **pandas**: Data manipulation and analysis.
- **scikit-learn**: Feature extraction and similarity computation.
- **huggingface_hub**: Cloud storage and retrieval of model files.
- **requests**: For API calls to TMDB.
- **difflib**: For fuzzy string matching.
- **TMDB API**: For fetching movie posters.

---

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Install required packages:
  ```
  pip install streamlit pandas requests huggingface_hub scikit-learn
  ```

### Running the App Locally

1. Clone this repository.
2. Ensure you have an internet connection (for model and poster downloads).
3. Run the app:
   ```
   streamlit run app.py
   ```
4. Open the provided local URL in your browser.

*No need to download any data or models manually—the app handles everything automatically via Hugging Face.*

---

## Example Workflow

1. **Enter a Movie or Any Text**: Type "Inception", "space adventure", or even "Nolan".
2. **Get Recommendations**: The app finds the closest movie and shows 5 highly relevant suggestions with posters.
3. **Explore Further**: Click "Get similar movies" on any recommendation to dive deeper into related films.
4. **Repeat**: Continue exploring as long as you like.

---

## Best Features

- **Always Up-to-Date**: Models are managed in the cloud, so improvements and updates are instantly available.
- **No Setup Hassles**: Zero local file management—just run and use.
- **Highly Relevant Suggestions**: Multi-stage similarity ensures recommendations are both broad and precise.
- **Engaging Visuals**: Posters make browsing fun and intuitive.
- **User-Centric Design**: Built for exploration, not just static lists.

---

## Credits

- **Movie data and posters**: TMDB
- **Model hosting**: Hugging Face
- **Development**: Inspired by modern recommender system research and practical deployment needs.

---

## License

This project is open source under the MIT License.

---

Discover your next favorite movie—start exploring now!
