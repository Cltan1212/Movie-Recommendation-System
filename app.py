# https://streamlit.io/
# https://docs.streamlit.io/library/api-reference
import streamlit as st
import pickle
import pandas as pd
import requests

# main function (modified from the jupyter notebook)
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index] 
    # sorted with the most 5 similar movies -> first will be the most similar
    movies_list = sorted(list(enumerate(distances)), reverse=True, key = lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title) # i[0] is the id
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# fetch the movie picture
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=9724fb5b3e5855eb27dfda9b225347fc&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

# load the movies from a Pickle file
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))  # Load the list of movies from a Pickle file
movies = pd.DataFrame(movies_dict)

# load the similarity matrix from a Pickle file
similarity = pickle.load(open('similarity.pkl', 'rb'))

# frond-end here:
# title of the page
st.title("Movie Recommender System")

# selected box that shows 5000 movies
selected_movie_name = st.selectbox('Movie', (movies['title'].values))

# button for recommendation
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    
    # Sort the names alphabetically
    sorted_names, sorted_posters = zip(*sorted(zip(names, posters)))

    # Create 5 columns dynamically
    cols = st.columns(5)

    # Iterate over the columns and display the name and poster of each movie
    for i in range(5):
        with cols[i]:
            st.text(sorted_names[i])
            st.image(sorted_posters[i])
