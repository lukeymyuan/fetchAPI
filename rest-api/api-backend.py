from flask import Flask, request
from flask_restplus import Resource, Api, fields, reqparse
from database import *
from authentication import *
from itsdangerous import JSONWebSignatureSerializer, SignatureExpired, BadSignature
from functools import wraps
from ml.prediction import predict_revenue

#TODO Edit endpints so that they are valid
#TODO make sure that the status code are the codes that we want
#TODO possibly store the tokens into another key, look at standard api to ensure those are the correct end points

#Sets up api token and where it should be
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'API-KEY'
    }
}


app = Flask(__name__)
#Creates the app for flask
api = Api(app,
          authorizations=authorizations)
#initiates database
db = Database()

#Creates the JSONWebSerializer
private_key = "Highway is so far away"
encryptor = Encryptor(private_key)

# The following is a model for a user
login_model = api.model('login', {
    'username': fields.String,
    'password': fields.String,
})

#Parsers for username and password
authenticate_parser = reqparse.RequestParser()
authenticate_parser.add_argument('username', type=str)
authenticate_parser.add_argument('password', type=str)

#Parser for a prediction
predict_parser = reqparse.RequestParser()
predict_parser.add_argument('budget', type=int, required=True, help='Budget in AUD')  
predict_parser.add_argument('release_month', type=int, required=True, help='Release month (1-12)')
predict_parser.add_argument('english', type=str, required=True, help='Is the movie in English? True / False')
predict_parser.add_argument('runtime', required=True, type=int, help='Runtime in minutes')

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('API-KEY')
        if not auth:  # no header set
            api.abort(401,"No access since you are not logged in")
        try:
            payload = encryptor.decrypt(auth)
        except SignatureExpired:
            api.abort(401,"Token expired, please login again")
        except BadSignature:
            api.abort(401,"Invalid Token")

        user = payload.get("username")
        password = payload.get("password")

        if not db.AuthenticateUser(user,password):
            api.abort(401,"Username/Password is incorrect")
        return f(*args, **kwargs)

    return decorated

@api.route('/predict')
class Revenue(Resource):
    #Uses machine learning to find the revenue of the movie
    @api.doc(description="Predicts the revenue of a movie based on its features")
    @api.response(200, 'Successful')
    @login_required
    @api.doc(security='apikey')
    def get(self):
        args = predict_parser.parse_args()
        args['english'] = True if args['english'] == 'True' else False
        revenue = int(predict_revenue(args))
        return {'revenue':revenue}, 200

@api.route('/signup')
class SignUp(Resource):
    # signs up the user
    @api.response(201, 'New user added to a db')
    @api.doc(description="Signs up the user so they can log in")
    @api.expect(login_model)
    def post(self):
        args = authenticate_parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        #Enters details into the system
        result = db.enterUser(username,password)
        #Succesfully added into the database and if no errors
        if not result:
            return {True:"Succesfully added into database"},201
        else:
            return {False:result},400

@api.route('/login')
class Authenticate(Resource):
    @api.response(200, 'Successful')
    @api.response(400, 'Incorrect login details')
    @api.doc(description="Login form for users")
    @api.expect(login_model)
    def get(self):
        args = authenticate_parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        if db.AuthenticateUser(username,password):
            return  {"success": True, "api-key": encryptor.encrypt(username,password)},200
        else:
            return {"success" : False, "error": "Either username doesn't exist or password is wrong"},400


if __name__ == '__main__':
    app.run(debug=True)