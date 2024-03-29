import sqlite3
import re
from makeDatabase import *
import os
#TODO fix so that if the file doesnt exist, to create the file
file_name = "datahouse.db"
posterPrefix = "https://image.tmdb.org/t/p/w342"

class Database(object):
    def __init__(self):
        self.initiate()
        self.conn = sqlite3.connect(file_name)
        self.pointer =self.conn.cursor()


    def restartPointer(self):
        self.conn = sqlite3.connect(file_name)
        self.pointer = self.conn.cursor()

    def save(self):
        self.conn.commit()
        self.conn.close()

    def initiate(self):
        if not os.path.exists(file_name):
            createDatabase()

    def enterUser(self,username,password):
        #Flask creates a new thread, therefore, need to recreate cursor object
        self.restartPointer()
        if username and password:
            #Regex to see if the password is using valid characters
            found = re.match(r'^(\w|\+|\*|\?|\^|\$|\.|\[|\]|\{|\}|\(|\)|\/)+$', password, re.M | re.I)
            # Test to see if username already exists
            self.pointer.execute('''SELECT * FROM User WHERE email= (?)''', (username,))
            result = self.pointer.fetchone()

            if len(password) < 6:
                error = "Password length is too short, needs to be at least 6 characters."
            elif not found:
                error="Password using invalid characters."
            elif result:
                error="Username already exists."
            else:
                #if it is all valid, adds the username and password to the database
                self.pointer.execute('''INSERT INTO User VALUES (?,?)''',(username,password))
                print("successfully added ")
                self.save()
                error=None
        else:
            error = "Username or password is not valid."

        return error

    def AuthenticateUser(self,username,password):
        #Flask creates a new thread, therefore, need to recreate cursor object
        self.restartPointer()
        self.pointer.execute('''SELECT password FROM User WHERE email= (?)''', (username,))
        result= self.pointer.fetchone()
        self.conn.close()
        if result:
            passFind = result[0]
            if passFind == password:
                return True
        return False

    def findMovie(self,revenue):
        self.restartPointer()
        command = '''
                    SELECT title,revenue,posterPath, abs(revenue-(?))*100/(?)*100 AS diff FROM
                    Main
                    ORDER BY diff
                    ASC LIMIT 3
             '''
        self.pointer.execute(command,(revenue,revenue,))
        result = self.pointer.fetchall()
        movieList = list()
        for movie in result:
            movieElement = {
                'movie': movie[0],
                'revenue': movie[1],
                'poster': posterPrefix+movie[2],
            }
            movieList.append(movieElement)
        return movieList




    def printer(self):
        #Flask creates a new thread, therefore, need to recreate cursor object
        self.restartPointer()
        self.pointer.execute('''SELECT * FROM User''')
        result = self.pointer.fetchall()  # retrieve the first row
        print(result)  # Print the first column retrieved(user's name)
        self.conn.close()


if __name__ == '__main__':
    db = Database()
    db.findMovie(900000)