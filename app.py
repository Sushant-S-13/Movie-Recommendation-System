import streamlit as st
import pickle
import requests


def fetch_poster(movie_title):
    api_key = "6dd7970c"
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if data.get("Response") == "True":
        return data.get("Poster")  # Returns poster URL
    else:
        return "https://via.placeholder.com/300x450.png?text=Poster+Not+Available"  # Placeholder image


def fetch_trailer(movie_title):
    search_query = f"{movie_title} trailer"
    youtube_url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
    return youtube_url


def fetch_description(movie_title):
    api_key = "6dd7970c"
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if data.get("Response") == "True":
        return data.get("Plot")  # Returns the movie description
    else:
        return "Description not available"


movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

st.markdown(
    """
    <style>
    .hero {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #6C63FF, #8E44AD);
        color: white;
        border-radius: 8px;
    }
    .movie-card {
        width: 320px;
        padding: 10px;
        text-align: center;
        border-radius: 8px;
        box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
    }
    .movie-card img {
        width: 100%;
        border-radius: 8px;
    }
    .movie-description {
        font-size: 21px;
        font-family: 'Arial';
        color: #FFF;
        margin-top: 10px;
    }
    .movie-card button {
        background-color: #6C63FF;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        width: 100%;
        margin-top: 10px;
    }
    </style>
    <div class="hero">
        <h1>🎬 Movie Recommender System</h1>
        <p>Designed By SUSHANT</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.header("Find the perfect movie recommendations tailored to your taste!")

import streamlit.components.v1 as components

imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

imageUrls = [
    fetch_poster("The Godfather"),
    fetch_poster("Avengers: Infinity War"),
    fetch_poster("The Dark Knight"),
    fetch_poster("Pulp Fiction"),
    fetch_poster("Spider-Man: Homecoming"),
    fetch_poster("Harry Potter and the Philosopher's Stone"),
    fetch_poster("The Lord of the Rings: The Fellowship of the Ring"),
    fetch_poster("The Shawshank Redemption"),
    fetch_poster("Inception"),
    fetch_poster("Titanic"),
    fetch_poster("Forrest Gump"),
    fetch_poster("The Lion King"),
    fetch_poster("Frozen")
]

imageCarouselComponent(imageUrls=imageUrls, height=400)

selectvalue = st.selectbox("Select movie from dropdown", movies_list)


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    recommend_trailer = []
    recommend_description = []
    for i in distance[1:6]:
        movie_title = movies.iloc[i[0]].title
        recommend_movie.append(movie_title)
        recommend_poster.append(fetch_poster(movie_title))
        recommend_trailer.append(fetch_trailer(movie_title))
        recommend_description.append(fetch_description(movie_title))
    return recommend_movie, recommend_poster, recommend_trailer, recommend_description


if st.button("Recommend"):
    movie_name, movie_poster, movie_trailer, movie_description = recommend(selectvalue)

    # Create columns for the recommended movies
    columns = st.columns(5)  # 5 columns for 5 recommended movies

    for i, (name, poster, trailer, description) in enumerate(
            zip(movie_name, movie_poster, movie_trailer, movie_description)):
        with columns[i]:
            st.markdown(
                f"""
                <div class="movie-card">
                    <img src="{poster}" alt="{name}">
                    <h3>{name}</h3>
                    <a href="{trailer}" target="_blank">
                        <button>Watch Trailer</button>
                    </a>
                    <p class="movie-description">{description}</p>
                    
                </div>
                """,
                unsafe_allow_html=True,
            )
