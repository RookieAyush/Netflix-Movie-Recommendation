import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import requests

# Load and preprocess dataset
df = pd.read_csv('netflix_titles.csv')
df['description'] = df['description'].fillna('')
df['listed_in'] = df['listed_in'].fillna('')
df['text'] = df['description'] + ' ' + df['listed_in']

# TF-IDF vectorization
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['text'])

# Model training
nn_model = NearestNeighbors(n_neighbors=6, metric='cosine')
nn_model.fit(tfidf_matrix)

# Recommender function
def recommend(query):
    query = query.lower()

    # Match exact title
    matches = df[df['title'].str.lower() == query]

    if not matches.empty:
        idx = matches.index[0]
        distances, indices = nn_model.kneighbors(tfidf_matrix[idx], n_neighbors=6)
        return df.iloc[indices[0][1:]][['title', 'listed_in', 'description']]

    # Match genre keyword
    genre_matches = df[df['listed_in'].str.lower().str.contains(query)]

    if not genre_matches.empty:
        return genre_matches[['title', 'listed_in', 'description']].sample(n=15, random_state=42)

    return []

# Poster fetch function
OMDB_API_KEY = "8df3a7d2"  # Replace with your actual API key

def fetch_poster(title):
    title = title.split(":")[0].strip()
    title = title.replace("&", "and")
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data.get('Response') == 'True' and data.get("Poster") != "N/A":
        return data.get('Poster')
    else:
        return "https://via.placeholder.com/160x240.png?text=No+Image"
