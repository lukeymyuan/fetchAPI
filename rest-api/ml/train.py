'''Trains the revenue prediction model from the movies dataset'''
import sys
import pandas as pd
from sklearn import linear_model
from sklearn.externals import joblib

FEATURES = ['budget', 'release_month', 'english', 'runtime']
MODEL_PATH = 'model.pk1'

def encode_month(release_month):
    '''Transform month column/Series into a one-hot encoding'''
    month_one_hot = pd.get_dummies(release_month)
    month_one_hot.columns = ['month_{}'.format(i) for i in month_one_hot.columns]
    return month_one_hot


def extract_features(df):
    '''Extract independent variables for training'''
    df = df[FEATURES]
    month_encoding = encode_month(df['release_month'])
    df = df.drop(columns=['release_month'])
    df = pd.concat([df, month_encoding], axis=1)
    return df


if __name__ == '__main__':
    movie_df = pd.read_csv(sys.argv[1])
    
    X = extract_features(movie_df)
    y = movie_df['revenue']

    model = linear_model.LinearRegression()
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    print('Model saved in {}'.format(MODEL_PATH))
