# predictor/model.py
import joblib
import os

# Load the model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'best_knn_model.pkl')
model = joblib.load(MODEL_PATH)
