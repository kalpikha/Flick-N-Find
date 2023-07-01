import pandas as pd
import streamlit as st
import requests
import pickle
import bz2file as bz2

st.set_page_config(
    page_title="Flick N Find",
    page_icon="🎬"
)

def decompress_pickle(file):

    data = bz2.BZ2File(file, 'rb')
    data = pickle.load(data)
    return data

movies_dict = decompress_pickle('models/movies_dict.pbz2')
movies_df = pd.DataFrame(movies_dict)

similarity = decompress_pickle('models/similarity.pbz2')

st.title('Flick N Find 🎬')

option = st.selectbox(
    'Select your movie',
    movies_df['title'].values)

def fetch_poster_ratings(movie_id):
    api_key = st.secrets['API_KEY']
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(movie_id, api_key))
    data = response.json()
    ratings = round(data['vote_average'],1)
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path'], ratings

def recommend_movies(movie):
    index = movies_df[movies_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    movie_posters = []
    movie_ratings = []
    for i in distances[1:5]:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended_movies.append(movies_df.iloc[i[0]].title)
        p, r = fetch_poster_ratings(movie_id)
        movie_posters.append(p)
        movie_ratings.append(r)

    return recommended_movies, movie_posters, movie_ratings


if st.button('Get Recommendations'):
    # st.write('Here are your top recommendations !!')
    movie_names, movie_posters, movies_ratings = recommend_movies(option)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text(movie_names[0])
        st.image(movie_posters[0])
        st.caption('{} :star: '.format(movies_ratings[0]))
    with col2:
        st.text(movie_names[1])
        st.image(movie_posters[1])
        st.caption('{} :star: '.format(movies_ratings[1]))

    with col3:
        st.text(movie_names[2])
        st.image(movie_posters[2])
        st.caption('{} :star: '.format(movies_ratings[2]))
    with col4:
        st.text(movie_names[3])
        st.image(movie_posters[3])
        st.caption('{} :star: '.format(movies_ratings[3]))
