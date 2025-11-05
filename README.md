https://movierecommender-pwtzxas67w3nk9u8xmkdse.streamlit.app/

# Movie Recommender System

This is a simple movie recommender system made as a college project. You can try the deployed app here:  
https://movierecommender-pwtzxas67w3nk9u8xmkdse.streamlit.app/

## What is this?

It's a web app where you can type in any movie name or even just some text, and it will suggest movies that are similar. You can keep clicking on any recommended movie to get more suggestions based on that one. The app shows movie posters and tries to make the experience interactive and fun.

## How does it work?

- The app uses some pre-trained models (stored on Hugging Face) to figure out which movies are similar to each other.
- When you search, it tries to match your input to a movie in its database, even if you make a typo.
- It uses two different ways (cosine and Euclidean similarity) to rank and re-rank the recommendations.
- Posters are fetched live from the TMDB API.


## Files and Data

- The app automatically downloads all the data it needs from Hugging Face, so you don't need to worry about any files.
- No Google Drive or local files are needed.

## Credits

- Movie data and posters: TMDB
- Model hosting: Hugging Face

---

This project was made for learning and demonstration purposes.
