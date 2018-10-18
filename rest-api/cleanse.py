'''
Uses pandas to remove the revenue and budget that is 0
and to combine the dataset with directors
'''

import pandas as pd
import os
import sqlite3

filename = os.path.join("ml", "movies_v1.csv")
DATABASE = "datahouse.db"

conn = sqlite3.connect(DATABASE)
pointer = conn.cursor()

def printer(cursor):
    cursor.execute('''SELECT * FROM Main''')
    user1 = cursor.fetchone()  # retrieve the first row
    print(user1)  # Print the first column retrieved(user's name)

if __name__ == '__main__':
    df1 = pd.read_csv(filename)
    createMovie = ''' CREATE TABLE IF NOT EXISTS Main(
                        movieID INTEGER PRIMARY KEY NOT NULL,
                        title TEXT,
                        budget INTEGER  NOT NULL,
                        genres TEXT,
                        originLanguage TEXT,
                        english TEXT,
                        company TEXT,
                        country TEXT,
                        releaseYear INTEGER,
                        releaseMonth INTEGER,
                        revenue INTEGER,
                        runtime INTEGER,
                        posterPath TEXT
                        )
                    '''
    pointer.execute(createMovie)
    for index, row in df1.iterrows():
        insertValue = (index,row['title'],row['budget'],row['genres'],
                       row['original_language'],row['english'],
                       row['production_companies'],row['production_countries'],
                       row['release_year'],row['release_month'], row['revenue'],
                       row['runtime'],row['poster_path'])

        pointer.execute('''INSERT INTO Main VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', insertValue)
    conn.commit()
    printer(pointer)
    conn.close()
