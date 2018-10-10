import sqlite3
import pandas as pd





def initiate(pointer,conn):
    createMovie = ''' CREATE TABLE Main(
                        movieID INTEGER PRIMARY KEY NOT NULL,
                        title TEXT,
                        adult TEXT,
                        budget INTEGER  NOT NULL,
                        revenue INTEGER NOT NULL,
                        runTime REAL,
                        country TEXT,
                        releaseMonth INTEGER,
                        releaseYear INTEGER,
                        director TEXT
                        )
                    '''
    createActor = ''' CREATE TABLE actorTable(
                        actor TEXT,
                        movieActor INTEGER,
                        FOREIGN KEY(movieActor) REFERENCES Main(movieID)
                        )
                    '''

    createGenre = ''' CREATE TABLE genreTable(
                        genre TEXT,
                        movieGenre INTEGER,
                        FOREIGN KEY(movieGenre) REFERENCES Main(movieID)
                        )
                    '''

    pointer.execute(createMovie)
    pointer.execute(createActor)
    pointer.execute(createGenre)
    conn.commit()

def rowTrial(pointer,conn):
    df = pd.read_csv("movie-data.csv")

    for index, row in df.iterrows():
        dictrow = row.to_dict()
        # print(dictrow)
        year,month,day = row['release_date'].split("-")
        director = ""
        value = (index,row['title'],row['adult'],row['budget'],
                 row['revenue'],row['runtime'],row['country'], month,year,director)

        pointer.execute('''INSERT INTO Main VALUES (?,?,?,?,?,?,?,?,?,?)''',value)
    conn.commit()

def printer(cursor):
    cursor.execute('''SELECT * FROM Main''')
    user1 = cursor.fetchone()  # retrieve the first row
    print(user1)  # Print the first column retrieved(user's name)
    # all_rows = cursor.fetchall()
    # for row in all_rows:
    #     # row[0] returns the first column in the query (name), row[1] returns email column.
    #     print('{0} : {1}, {2}'.format(row[0], row[1], row[2]))

if __name__ == '__main__':
    file_name = "movie-data.db"
    conn = sqlite3.connect(file_name)
    pointer = conn.cursor()
    # initiate(pointer,conn)
    rowTrial(pointer,conn)
    printer(pointer)
