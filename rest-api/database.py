import sqlite3
import re
#TODO fix so that if the file doesnt exist, to create the file
file_name = "Users.db"
class Database(object):
    def __init__(self):
        self.conn = sqlite3.connect(file_name)
        self.pointer =self.conn.cursor()
        self.initiate()

    def restartPointer(self):
        self.conn = sqlite3.connect(file_name)
        self.pointer = self.conn.cursor()

    def initiate(self):
        UserTable = ''' CREATE TABLE IF NOT EXISTS User(
                            email TEXT PRIMARY KEY NOT NULL,
                            password TEXT
                            )
                        '''

        self.pointer.execute(UserTable)
        self.conn.commit()



    def enterUser(self,username,password):
        #Flask creates a new thread, therefore, need to recreate cursor object
        self.restartPointer()
        if username and password:
            #Regex to see if the password is using valid characters
            found = re.match(r'^(\w|\+|\*|\?|\^|\$|\.|\[|\]|\{|\}|\(|\)|\/)+$', password, re.M | re.I)
            # Test to see if username already exists
            self.pointer.execute('''SELECT * FROM User WHERE email= (?)''', (username,))
            result = self.pointer.fetchone()

            if len(password) < 7:
                error = "Password length is too short, needs to be more than 6 characters"
            elif not found:
                error="Password using invalid characters"
            elif result:
                error="Username already exists"
            else:
                #if it is all valid, adds the username and password to the database
                self.pointer.execute('''INSERT INTO User VALUES (?,?)''',(username,password))
                print("successfully added ")
                self.conn.commit()
                error=None
        else:
            error = "Username or password is not valid"

        return error

    def AuthenticateUser(self,username,password):
        #Flask creates a new thread, therefore, need to recreate cursor object
        self.restartPointer()
        self.pointer.execute('''SELECT password FROM User WHERE email= (?)''', (username,))
        result= self.pointer.fetchone()
        if result:
            passFind = result[0]
            if passFind == password:
                return True
        return False

    def printer(self):
        #Flask creates a new thread, therefore, need to recreate cursor object
        self.restartPointer()
        self.pointer.execute('''SELECT * FROM User''')
        result = self.pointer.fetchall()  # retrieve the first row
        print(result)  # Print the first column retrieved(user's name)


if __name__ == '__main__':
    db = Database()
    db.enterUser("phb136", "potato1")
    db.enterUser("kenrokzz", "potato1")
    db.enterUser("phb136", "potato1")
    db.enterUser("phb136adasd", "potato1")
    db.printer()