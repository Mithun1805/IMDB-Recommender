import pandas as pd
from src.convert import partial_match, exact_match
from model_1 import details_movies

movies = pd.read_csv("imdb_top_1000.csv")

movies.rename(columns={"Series_Title": "title"}, inplace=True)

movies_1 = movies

movies["genres_list"] = movies["Genre"].apply(
    lambda x: [g.strip() for g in x.split(",")]
)

all_genres = sorted(
    {g.strip() for genres in movies["Genre"] for g in genres.split(",")}
)

def recommend_movies(selected_genres, top_n=5):

    movies["exact_match"] = movies["genres_list"].apply(
        lambda x: exact_match(x, selected_genres)
    )

    movies["partial_score"] = movies["genres_list"].apply(
        lambda x: partial_match(x, selected_genres)
    )

    filtered_movies = movies[movies["partial_score"] > 0]

    filtered_movies = filtered_movies.sort_values(
        by=["exact_match", "partial_score"],
        ascending=False
    )

    recommended = filtered_movies.head(top_n)

    return recommended["title"].tolist()
