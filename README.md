# fetchAPI
For the frontend:
1. Download Nodejs from https://nodejs.org/en/download/
2. install all packages for enviroment `npm i`
3. Execute `node index.js`
(Option) install nodemon to monitor the changes in client `nodemon index.js` or `nodemon . `
If it shows `nodemon: not found`, then `sudo npm install -g nodemon`



For the backend:
    - API is initiated by running the 'api-backend.py' file
   
  Prerequisites:
  Install pipenv: https://github.com/pypa/pipenv

## instructions
1. Run command to set up modules: `pipenv install`
2. Launch the pipenv shell: `pipenv shell`
2. Train the prediction model: `python ml/train.py ml/movies_v1.csv`
3. Start the API using command: `python api-backend.py`

## Integrating Machine learning (for backend)
```python
from ml.prediction import predict_revenue
# To run prediction:
predict_revenue(movie_info) # movie_info is a dictionary
# predict_revenue returns a number for the predicted revenue
```
