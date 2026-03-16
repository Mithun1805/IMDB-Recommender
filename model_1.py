import pandas as pd
from src.convert import remove_space,stems
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
movies = pd.read_csv("imdb_top_1000.csv")

movies = movies.rename(columns={
    "Series_Title":"title",
    "IMDB_Rating":"imdb",
    "Released_Year":"year",
    "Genre":"genre"
})

# copy for movie details
details_movies = movies.copy()

# create cast column
details_movies["cast"] = (
    details_movies["Star1"] + ", " +
    details_movies["Star2"] + ", " +
    details_movies["Star3"] + ", " +
    details_movies["Star4"]
)

# popularity data
popularity_data = movies[['title','imdb','No_of_Votes']].copy()

# cast preparation
movies["Star1"] = movies["Star1"].apply(lambda x: x.split(","))
movies["Star2"] = movies["Star2"].apply(lambda x: x.split(","))
movies["Star3"] = movies["Star3"].apply(lambda x: x.split(","))
movies["Star4"] = movies["Star4"].apply(lambda x: x.split(","))

movies["cast"] = movies["Star1"] + movies["Star2"] + movies["Star3"] + movies["Star4"]

movies['Overview'] = movies['Overview'].apply(lambda x: x.split())
movies['genre'] = movies['genre'].apply(lambda x: x.split(","))
movies['Director'] = movies['Director'].apply(lambda x: x.split(","))

movies["Director"] = movies["Director"].apply(remove_space)
movies["cast"] = movies["cast"].apply(remove_space)

movies = movies[["title","Overview","genre","Director","cast"]]

movies["tags"] = movies["Overview"] + movies["genre"] + movies["Director"] + movies["cast"]

movies = movies[['title','tags']]

movies['tags'] = movies['tags'].apply(lambda x: " ".join(x))
movies['tags'] = movies['tags'].apply(lambda x: x.lower())
movies['tags'] = movies['tags'].apply(stems)

cv = CountVectorizer(max_features=5000, stop_words='english')
vector = cv.fit_transform(movies['tags']).toarray()

similarity = cosine_similarity(vector)

# popularity score
C = popularity_data['imdb'].mean()
m = popularity_data['No_of_Votes'].quantile(0.90)

def weighted_rating(x, m=m, C=C):
    v = x['No_of_Votes']
    R = x['imdb']
    return (v/(v+m) * R) + (m/(v+m) * C)

popularity_data['popularity'] = popularity_data.apply(weighted_rating, axis=1)

