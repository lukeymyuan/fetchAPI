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
# Testing requirements
input_model = api.model('input',{
    'revenue': fields.Integer,
})

#Movie features
features_model = api.model('features',{
    'director': fields.String,
    'budget': fields.Integer,
    'english':fields.String,
    'runtime': fields.Integer,
    'release_month': fields.Integer,
    'cast1': fields.String,
    'cast2': fields.String,
    'cast3': fields.String,
    'cast4': fields.String,
    'cast5': fields.String,
})

#Parsers for username and password
authenticate_parser = reqparse.RequestParser()
authenticate_parser.add_argument('username', type=str, location='json')
authenticate_parser.add_argument('password', type=str, location='json')

#Parser for a prediction
predict_parser = reqparse.RequestParser()
predict_parser.add_argument('director', type=str, help='Full name of a director', location='json')
predict_parser.add_argument('budget', type=int, required=True, help='Budget in AUD', location='json')  
predict_parser.add_argument('release_month', type=int, required=True, help='Release month (1-12)', location='json')
predict_parser.add_argument('english', type=str, required=True, help='Is the movie in English? True / False', location='json')
predict_parser.add_argument('runtime', required=True, type=int, help='Runtime in minutes', location='json')
predict_parser.add_argument('cast1', type=str, help='Cast member 1', location='json')
predict_parser.add_argument('cast2', type=str, help='Cast member 2', location='json')
predict_parser.add_argument('cast3', type=str, help='Cast member 3', location='json')
predict_parser.add_argument('cast4', type=str, help='Cast member 4', location='json')
predict_parser.add_argument('cast5', type=str, help='Cast member 5', location='json')

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
    @api.response(200, 'Successful determined the revenue')
    @api.response(400, 'One or more of the input parameters is invalid')
    @login_required
    @api.doc(security='apikey')
    @api.expect(features_model)
    def post(self):
        args = predict_parser.parse_args()
        args['english'] = True if args['english'] == 'True' else False
        cast = []
        if args.get('budget') < 0:
            api.abort(400,'Budget has to be greater or equal to 0')
        elif args.get('release_month') < 1 or args.get('release_month') > 12:
            api.abort(400,"Month is not valid, it has to be between 1 - 12")
        elif args.get('runtime') <= 0:
            api.abort(400,"Runtime has to be larger than 0")
        for i in range(1,6):
            key = 'cast' + str(i)
            if args.get(key) is not None and args[key] != 'Option' and args[key] != '':
                cast.append(args[key])
            args.pop(key, None)
        args['actors'] = cast
        revenue = int(predict_revenue(args))
        return {'message':'Successfully determined the revenue based on features', 'revenue':revenue}, 200

@api.route('/movies/<int:revenue>')
class Movies(Resource):
    #Returns a list of movies that are the most similar to the current revenue
    @api.doc(description="Shows a list of movies that have the most similar revenue")
    @api.response(200,'Successfully found movies')
    @api.response(400, 'Invalid input - Revenue greater than zero')
    @login_required
    @api.doc(security='apikey')
    def get(self,revenue):
        if revenue <= 0:
            api.abort(400,'Revenue has to be greater than zero')
        '''
            list of 3 movies in this format
            {'movie': 'name},
            {'revenue': 5000},
            {'poster': link},
        '''
        movieList = db.findMovie(revenue)
        return {'message':"Sucessfully found movies with similar revenue", 'movieList': movieList},200



@api.route('/signup')
class SignUp(Resource):
    # signs up the user
    @api.response(201, 'A new user successfully signed up.')
    @api.response(400, 'Username already exists.')
    @api.doc(description="Signs up for new users.")
    @api.expect(login_model)
    def post(self):
        args = authenticate_parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        #Enters details into the system
        result = db.enterUser(username,password)
        #Succesfully added into the database and if no errors
        if not result:
            return {"message":"A new user successfully signed up."}, 201
        api.abort(400,result)

@api.route('/login')
class Authenticate(Resource):
    @api.response(201, 'Successful login.')
    @api.response(400, 'Incorrect login details.')
    @api.doc(description="Login form for users.")
    @api.expect(login_model)
    def post(self):
        args = authenticate_parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        if db.AuthenticateUser(username,password):
            return  {"message":"Successful login.", "api-key":encryptor.encrypt(username,password)}, 201
        api.abort(400,"Either username doesn't exist or password is wrong.")

if __name__ == '__main__':
    app.run(debug=True)