import numpy as np
import os
import pandas as pd
from sklearn.externals import joblib
from ml.cast_crew import get_director_revenue, get_actor_list_revenue

FEATURES = ['budget', 'release_month', 'english', 'runtime']
GENERATED = ['director_revenue', 'actor_revenue']
MODEL_PATH = 'model.pk1'

model = joblib.load(MODEL_PATH)

def encode_month(month):
    '''Get one-hot encoding for month value'''
    months = pd.DataFrame(columns=['month_{}'.format(i) for i in range(1,12+1)])
    months.loc[0] = 0
    months['month_{}'.format(month)][0] = 1
    return months    

def predict_revenue(movie: dict):
    '''Predict the revenue of a movie given its features'''
    data = dict(movie)
    director = data.pop('director', 'Other_')
    actors = data.pop('actors', [])
    actors_str = '#'.join([a.replace('#', '') for a in actors])
    data['director_revenue'] = get_director_revenue(director)
    data['actor_revenue'] = get_actor_list_revenue(actors_str)
    movie_df = pd.DataFrame([data], columns=GENERATED + FEATURES)
    if movie_df.isnull().values.any():
        raise Exception('Missing fields: movie info should have {}'.format(FEATURES))

    month_encoding = encode_month(movie['release_month'])
    movie_df = movie_df.drop(columns=['release_month'])
    movie_df = pd.concat([movie_df, month_encoding], axis=1)

    pred = model.predict(movie_df)
    return pred[0]

if __name__ == '__main__':
    # test predict
    r = predict_revenue({
        'director': 'Edgar Wright',
        'actors': ['Ansel Elgort', 'Lily James', 'Kevin Spacey', 'Jamie Foxx',
            'Jon Hamm'],
        'budget': 34000000,
        'release_month': 6,
        'english': True,
        'runtime': 113
    })
    print(r)
