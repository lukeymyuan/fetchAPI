# fetchAPI

## Summary
A ML webapp that predicts the revenue(box office) based on the features of the movie and shows similar movies

## Getting Started
### Frontend
```sh
npm install
node index.js
```
Frontend should now be running on <http://127.0.0.1:8081>

### Backend:
Prerequisites:
Install pipenv: https://github.com/pypa/pipenv

1. Run command to set up modules: `pipenv install`
2. Launch the pipenv shell: `pipenv shell`
2. Train the prediction model: `python ml/train.py ml/movies_v1.csv`
3. Start the API using command: `python api-backend.py`

Backend should now be running on <http://127.0.0.1:5000>

## Integrating Machine learning (for backend)
```python
from ml.prediction import predict_revenue
# To run prediction:
predict_revenue(movie_info) # movie_info is a dictionary
# predict_revenue returns a number for the predicted revenue
```
