def remove_space(word):
    l= []
    for i in word:
        l.append(i.replace(" ",""))
    return l

from nltk.stem import PorterStemmer
ps  = PorterStemmer()
def stems(text):
    l = []
    for i in text.split():
        l.append(ps.stem(i))
    return " ".join(l)

def partial_match(movie_genres,selected_genres):
    #selected_genres = ["Action","Comedy"]
    return len(set(movie_genres) & set(selected_genres))

def exact_match(movie_genres,selected_genres):
    #selected_genres = ["Action","Comedy"]
    return set(movie_genres) == set(selected_genres)