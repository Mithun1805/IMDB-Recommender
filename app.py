
import streamlit as st
from model_1 import movies, similarity, details_movies
from filter import all_genres, recommend_movies, movies_1


st.header("🎬 Movie Recommender System")

# ---------------- SESSION STATE ----------------

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = ""

if "selected_genres" not in st.session_state:
    st.session_state.selected_genres = []

if "recommended_movies" not in st.session_state:
    st.session_state.recommended_movies = []


# ---------------- RECOMMENDATION FUNCTION ----------------

def recommend(movie):

    index = movies[movies['title'] == movie].index[0]

    distance = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommend_list = []

    for i in distance[1:6]:
        recommend_list.append(movies.iloc[i[0]].title)

    return recommend_list


# ---------------- SHOW MOVIE DETAILS PAGE ----------------

def movie_details_page(movie):

    movie_data = details_movies[details_movies['title'] == movie]
    movies_data = movies_1[movies_1['title'] == movie]

    if movie_data.empty:
        st.warning("Details not available for this movie.")
        return

    movie_data = movie_data.iloc[0]
    movies_data = movies_data.iloc[0]

    st.title(movie)

    # 🎬 Poster
    st.image(movies_data['Poster_Link'], width=300)

    st.write("🎬 **Overview**")
    st.write(movies_data['Overview'])

    st.write("🎭 **Cast**")

    cast = movie_data['cast']

    if isinstance(cast, list):
        for actor in cast[:5]:
            st.markdown(f"• {actor}")
    else:
        st.write(cast)

    st.write("🎥 **Director**")

    director = movie_data['Director']

    if isinstance(director, list):
        st.write(", ".join(director))
    else:
        st.write(director)

    if st.button("⬅ Back to Recommendations"):
        st.session_state.page = "recommendations"
        st.rerun()


# ---------------- HOME PAGE ----------------

if st.session_state.page == "home":

    movies_list = [""] + list(movies['title'].values)

    select_movie = st.selectbox(
        "Type or select a Movie (optional)",
        movies_list
    )

    st.subheader("Select Genres")

    cols = st.columns(4)

    for i, genre in enumerate(all_genres):

        if genre in st.session_state.selected_genres:
            label = f"✅ {genre}"
        else:
            label = genre

        if cols[i % 4].button(label, key=f"genre_{genre}"):

            if genre in st.session_state.selected_genres:
                st.session_state.selected_genres.remove(genre)
            else:
                st.session_state.selected_genres.append(genre)

    selected_genres = st.session_state.selected_genres

    if st.button("Show Recommendation"):

        if selected_genres:
            st.session_state.recommended_movies = recommend_movies(selected_genres)

        elif select_movie != "":
            st.session_state.recommended_movies = recommend(select_movie)

        else:
            st.warning("Please select a movie or genres.")
            st.stop()

        st.session_state.page = "recommendations"
        st.rerun()


# ---------------- RECOMMENDATION PAGE ----------------

elif st.session_state.page == "recommendations":

    st.subheader("Recommended Movies")

    recommended_movies = st.session_state.recommended_movies

    cols = st.columns(5)

    for i, movie in enumerate(recommended_movies):

        movie_data = movies_1[movies_1['title'] == movie].iloc[0]

        with cols[i]:
            st.image(movie_data['Poster_Link'])
            if st.button(movie, key=f"movie_{i}"):
                st.session_state.selected_movie = movie
                st.session_state.page = "details"
                st.rerun()

    if st.button("🔄 Start Over"):
        st.session_state.selected_genres = []
        st.session_state.page = "home"
        st.rerun()


# ---------------- DETAILS PAGE ----------------

elif st.session_state.page == "details":

    movie_details_page(st.session_state.selected_movie)


