'''
Uses pandas to remove the revenue and budget that is 0
and to combine the dataset with directors
'''

import pandas as pd

filename = "the-movies-dataset/movies_metadata.csv"
file_cast = "the-movies-dataset/credits.csv"
output = "movie-data.csv"

def cleanse(df):
    columns_keep = ['adult',
                        'original_title',
                       'genres',
                       'budget',
                       'runtime',
                       'production_countries',
                       'release_date',
                       'revenue',
                        'cast',
                        'crew',
                       ]
    # keep necessary columns
    newdf = df[columns_keep]
    newdf.rename(index=str, columns={"original_title": "title", "production_countries": "country"},inplace=True)
    newdf = newdf.query('budget != "0"')
    newdf = newdf.query('revenue > 0')
    return newdf
if __name__ == '__main__':
    df1 = pd.read_csv(filename)
    df2 = pd.read_csv(file_cast)
    df = df1.merge(df2,left_index=True,right_index=True)
    df = cleanse(df)
    df.to_csv(output)
