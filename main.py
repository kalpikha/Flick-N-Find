import pandas as pd
import streamlit as st
import requests
import pickle
import bz2file as bz2

def decompress_pickle(file):

    data = bz2.BZ2File(file, 'rb')
    data = pickle.load(data)
    return data

movies_dict = decompress_pickle('models/movies_dict.pbz2')
movies_df = pd.DataFrame(movies_dict)

similarity = decompress_pickle('models/similarity.pbz2')

st.title('Flick N Find')
option = st.selectbox(
    'Select your movie',
    movies_df['title'].values)

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=5eff1cc96866d62e856adb3550188b65&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend_movies(movie):
    index = movies_df[movies_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    movie_posters = []
    for i in distances[1:5]:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended_movies.append(movies_df.iloc[i[0]].title)
        movie_posters.append(fetch_poster(movie_id))
    return recommended_movies, movie_posters


if st.button('Get Recommendations'):
    # st.write('Here are your top recommendations !!')
    movie_names, movie_posters = recommend_movies(option)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.caption(movie_names[0])
        st.image(movie_posters[0])
    with col2:
        st.caption(movie_names[1])
        st.image(movie_posters[1])

    with col3:
        st.caption(movie_names[2])
        st.image(movie_posters[2])
    with col4:
        st.caption(movie_names[3])
        st.image(movie_posters[3])

