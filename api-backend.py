from flask import Flask, request
from flask_restplus import Resource, Api, fields, reqparse
from database import *


app = Flask(__name__)
api = Api(app)
db = Database()

# The following is a model for a user
User_model = api.model('User', {
    'username': fields.String,
    'password': fields.String,
})

@api.route('/predict')
@api.doc(description="Predicts the revenue of a movie based on its features")
@api.response(200, 'Successful')
class Revenue(Resource):
    #Uses machine learning to find the revenue of the movie
    def post(self):
        return {'Revenue': 90000000},200



@api.route('/signup')
@api.doc(description="Signs up the user so they can log in")
class Login(Resource):
    # signs up the user
    @api.expect(User_model)
    def post(self):
        #Flask creates a new thread, therefore, need to recreate cursor object
        db.restartPointer()
        content = request.json
        username = content.get("username")
        password = content.get("password")
        #Enters details into the system
        result = db.enterUser(username,password)
        #Succesfully added into the database and if no errors
        if not result:
            return {True:"Succesfully added into database"},200
        else:
            return {False:result},200



if __name__ == '__main__':
    app.run(debug=True)