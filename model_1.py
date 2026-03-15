import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.convert import remove_space,stems

movies = pd.read_csv("imdb_top_1000.csv")

movies = movies.rename(columns = {"IMDB_Rating":"imdb"})

movies["Star1"] = movies["Star1"].apply(lambda x: x.split(","))
movies["Star2"] = movies["Star2"].apply(lambda x: x.split(","))
movies["Star3"] = movies["Star3"].apply(lambda x: x.split(","))
movies["Star4"] = movies["Star4"].apply(lambda x: x.split(","))

movies = movies.rename(columns = {"Series_Title":"title"})
movies = movies.rename(columns = {"Released_Year":"year"})
movies = movies.rename(columns = {"Genre":"genre"})
movies["cast"] = movies["Star1"]+ movies["Star2"] + movies["Star3"] + movies["Star4"]

movies['Overview'] = movies['Overview'].apply(lambda x: x.split())

movies = movies[["title","Overview","genre","Director","cast"]]

movies['genre'] = movies['genre'].apply(lambda x: x.split(","))

movies['Director'] = movies['Director'].apply(lambda x: x.split(','))

movies["Director"] = movies["Director"].apply(remove_space)
movies["cast"] = movies["cast"].apply(remove_space)

details_movies = movies

movies["tags"] = movies["Overview"] + movies["genre"] + movies["Director"] + movies["cast"]

movies = movies[['title','tags']]

movies['tags'] = movies['tags'].apply(lambda x: " ".join(x))

movies['tags'] = movies['tags'].apply(lambda x: x.lower())

movies['tags'] = movies['tags'].apply(stems)

cv = CountVectorizer(max_features=5000, stop_words='english')

vector = cv.fit_transform(movies['tags']).toarray()

similarity = cosine_similarity(vector)

