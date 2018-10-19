'''

'''

import pandas as pd
import os
import sqlite3

filename = os.path.join("ml", "movies_v1.csv")
DATABASE = "datahouse.db"


def printer(cursor):
    cursor.execute('''SELECT * FROM User''')
    user1 = cursor.fetchone()  # retrieve the first row
    print(user1)  # Print the first column retrieved(user's name)

def createDatabase():
    conn = sqlite3.connect(DATABASE)
    pointer = conn.cursor()
    df1 = pd.read_csv(filename)
    createMovie = ''' CREATE TABLE Main(
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
    UserTable = ''' CREATE TABLE User(
                        email TEXT PRIMARY KEY NOT NULL,
                        password TEXT
                        )
                    '''
    pointer.execute(createMovie)
    pointer.execute(UserTable)
    conn.commit()
    for index, row in df1.iterrows():
        insertValue = (index,row['title'],row['budget'],row['genres'],
                       row['original_language'],row['english'],
                       row['production_companies'],row['production_countries'],
                       row['release_year'],row['release_month'], row['revenue'],
                       row['runtime'],row['poster_path'])

        pointer.execute('''INSERT INTO Main VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', insertValue)
    conn.commit()
    printer(pointer)
    print("Successfully created database")
    conn.close()
