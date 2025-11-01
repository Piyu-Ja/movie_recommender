import streamlit as st
import pickle
import pandas as pd
import requests
import time
import difflib
import random
import gdown
import os

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=b98659973d144fa7fcc6dfad33c1661f&language=en-US"
    for attempt in range(3):
        try:
            data = requests.get(url,timeout=10)
            data.raise_for_status()
            data = data.json()
            poster_path = data.get('poster_path')
            if not poster_path:
                return "https://via.placeholder.com/500x750?text=No+Image"
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        except requests.exceptions.RequestException as e:
            print(f"⚠ Attempt {attempt + 1}: Error fetching poster for {movie_id} → {e}")
            time.sleep(1)
    return "https://via.placeholder.com/500x750?text=Connection+Error"


st.title('Movie Recommender System')

# Download model files from Google Drive using gdown
model_dir = "model"
os.makedirs(model_dir, exist_ok=True)

# Replace these IDs with your actual Google Drive file IDs
drive_ids = {
    "movie_list": "1oXYw7-yUZhbVdUhUhz2GlnYUgb-ypwcr",
    "similarity_cosine": "1Tb92OEnzQnEkgU8187xmgIdwAU7LfZ9O",
    "similarity_euclid": "1IYg5Qa0nJ8aFx5mdb9ASaGG0y2ko522F"
}

local_paths = {
    "movie_list": os.path.join(model_dir, "movie_list.pkl"),
    "similarity_cosine": os.path.join(model_dir, "similarity_cosine.pkl"),
    "similarity_euclid": os.path.join(model_dir, "similarity_euclid.pkl")
}

for key in drive_ids:
    if not os.path.exists(local_paths[key]):
        gdown.download(
            f"https://drive.google.com/uc?id={drive_ids[key]}",
            local_paths[key],
            quiet=False
        )

movies = pd.DataFrame(pickle.load(open(local_paths["movie_list"], 'rb')))
similarity_cosine = pickle.load(open(local_paths["similarity_cosine"], 'rb'))
similarity_euclid = pickle.load(open(local_paths["similarity_euclid"], 'rb'))


movie_list = movies['title'].values.tolist()

# keep radio for compatibility, but internal flow always uses cosine->euclid
metric = st.radio("Ranking metric (primary -> re-rank)", ("cosine_then_euclid",), index=0, format_func=lambda x: "cosine → euclid (top25→top5)")

# 1) Replace selectbox with free text input + Search button
search_text = st.text_input("Enter any text (will be resolved to a movie):", value="")
if "current_root_movie" not in st.session_state:
    st.session_state["current_root_movie"] = None

def resolve_input_to_movie(text):
    # Exact match (case-insensitive)
    if not text or str(text).strip() == "":
        return random.choice(movie_list)
    text = text.strip()
    lower_map = {t.lower(): t for t in movie_list}
    if text.lower() in lower_map:
        return lower_map[text.lower()]
    # substring matches
    substr_matches = [t for t in movie_list if text.lower() in t.lower()]
    if substr_matches:
        return substr_matches[0]
    # use difflib closest match
    matches = difflib.get_close_matches(text, movie_list, n=1, cutoff=0.35)
    if matches:
        return matches[0]
    # fallback random
    return random.choice(movie_list)

# Helper functions (unchanged logic mostly)
def get_ordered_candidates_indices(movie_title, top_k_cosine=25):
    movie_index = movies[movies['title'] == movie_title].index[0]
    sims = list(enumerate(similarity_cosine[movie_index]))
    sims_sorted = sorted(sims, reverse=True, key=lambda x: x[1])
    candidate_pairs = sims_sorted[1: top_k_cosine + 1]
    candidate_indices = [idx for idx, _ in candidate_pairs]
    if similarity_euclid is not None:
        candidate_indices = sorted(candidate_indices, reverse=True, key=lambda idx: similarity_euclid[movie_index][idx])
    return candidate_indices

def ids_and_posters_from_indices(indices):
    titles = [movies.iloc[idx].title for idx in indices]
    ids = [int(movies.iloc[idx].movie_id) for idx in indices]
    posters = [fetch_poster(mid) for mid in ids]
    return titles, posters, ids

def ensure_candidates_for_movie(movie_title, top_k_cosine=25):
    key = f"cands_{movie_title.replace(' ','__')}"
    page_key = f"page_{movie_title.replace(' ','__')}"
    last_shown_key = f"last_shown_{movie_title.replace(' ','__')}"
    no_more_key = f"no_more_{movie_title.replace(' ','__')}"
    if key not in st.session_state:
        st.session_state[key] = get_ordered_candidates_indices(movie_title, top_k_cosine=top_k_cosine)
        st.session_state[page_key] = 0
        st.session_state[last_shown_key] = None
        st.session_state[no_more_key] = False

def get_page_for_movie(movie_title, page, page_size=5):
    key = f"cands_{movie_title.replace(' ','__')}"
    ordered_indices = st.session_state.get(key, [])
    start = page * page_size
    end = start + page_size
    page_indices = ordered_indices[start:end]
    titles, posters, ids = ids_and_posters_from_indices(page_indices)
    return titles, posters, ids, len(ordered_indices)

def get_next_unique_page(movie_title, page_size=5):
    key = f"cands_{movie_title.replace(' ','__')}"
    page_key = f"page_{movie_title.replace(' ','__')}"
    last_shown_key = f"last_shown_{movie_title.replace(' ','__')}"
    no_more_key = f"no_more_{movie_title.replace(' ','__')}"
    ensure_candidates_for_movie(movie_title, top_k_cosine=25)
    ordered = st.session_state.get(key, [])
    total = len(ordered)
    max_pages = (total + page_size - 1) // page_size
    current_page = st.session_state.get(page_key, 0)
    last_shown = st.session_state.get(last_shown_key, None)

    # Try next pages until a new set is found
    for p in range(current_page + 1, max_pages):
        start = p * page_size
        end = start + page_size
        indices = ordered[start:end]
        _, _, ids = ids_and_posters_from_indices(indices)
        if last_shown is not None and ids == last_shown:
            continue
        # Found a new page
        st.session_state[page_key] = p
        st.session_state[last_shown_key] = ids
        st.session_state[no_more_key] = False
        st.session_state["current_root_movie"] = movie_title
        return True
    # If no new page found
    st.session_state[no_more_key] = True
    return False

def primary_recommend(selected_movie, top_k_cosine=25, top_n=5, page=0):
    ordered_indices = get_ordered_candidates_indices(selected_movie, top_k_cosine=top_k_cosine)
    start = page * top_n
    top_indices = ordered_indices[start:start + top_n]
    titles, posters, ids = ids_and_posters_from_indices(top_indices)
    key_candidates = f"cands_{selected_movie.replace(' ','__')}"
    last_shown_key = f"last_shown_{selected_movie.replace(' ','__')}"
    if key_candidates not in st.session_state:
        st.session_state[key_candidates] = ordered_indices
    # Track last shown ids for duplicate avoidance
    st.session_state[last_shown_key] = ids
    return titles, posters, ids

def show_recommendations_for(root_movie):
    page_key = f"page_{root_movie.replace(' ','__')}"
    no_more_key = f"no_more_{root_movie.replace(' ','__')}"
    page = st.session_state.get(page_key, 0)
    primary_titles, primary_posters, primary_ids = primary_recommend(root_movie, top_k_cosine=25, top_n=5, page=page)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(primary_titles[idx])
            st.image(primary_posters[idx])
            rec_title = primary_titles[idx]
            rec_id = primary_ids[idx]
            if st.button("Get similar movies", key=f"get_sim_{rec_id}"):
                ok = get_next_unique_page(rec_title, page_size=5)
                if not ok:
                    st.warning("No more movies in database for this movie.")

    # Show "No more movies" if all pages exhausted
    if st.session_state.get(no_more_key, False):
        st.write("No more movies in database for this movie.")

# Search button handler: resolve text -> movie and set as current root
if st.button("Search"):
    resolved = resolve_input_to_movie(search_text)
    st.session_state["current_root_movie"] = resolved
    ensure_candidates_for_movie(resolved, top_k_cosine=25)
    st.session_state[f"no_more_{resolved.replace(' ','__')}"] = False
    st.session_state[f"last_shown_{resolved.replace(' ','__')}"] = None
    st.session_state[f"page_{resolved.replace(' ','__')}"] = 0

# If current_root_movie set, show recommendations for it, otherwise prompt
if st.session_state.get("current_root_movie"):
    show_recommendations_for(st.session_state["current_root_movie"])
else:
    st.write("Enter a text and press Search (or click a movie's 'Get similar movies').")
