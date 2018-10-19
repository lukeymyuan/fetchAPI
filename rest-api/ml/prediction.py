import numpy as np
import pandas as pd
from sklearn.externals import joblib

FEATURES = ['budget', 'release_month', 'english', 'runtime']

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
    movie_df = pd.DataFrame([movie], columns=FEATURES)
    if movie_df.isnull().values.any():
        raise Exception('Missing fields: movie info should have {}'.format(FEATURES))

    month_encoding = encode_month(movie['release_month'])
    movie_df = movie_df.drop(columns=['release_month'])
    movie_df = pd.concat([movie_df, month_encoding], axis=1)

    # print(movie_df)

    pred = model.predict(movie_df)
    return pred[0]

if __name__ == '__main__':
    # test predict
    r = predict_revenue({
        'budget': 600000000,
        'release_month': 12,
        'english': True,
        'runtime': 180
    })
    print(r)
