import json
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from .model import model  # Assuming 'model' is your trained model instance

# Define global variables for OneHotEncoder and StandardScaler
encoder = OneHotEncoder(sparse_output=False)
scaler = StandardScaler()

# Predefined feature names based on training data
expected_columns = ['Gender_Female', 'Gender_Male', 'Weight', 'BMI', 'Height', 'Age', 
                    'BMIcase_underweight', 'BMIcase_normal', 'BMIcase_overweight', 'BMIcase_obese']

@csrf_exempt
def index(request):
    return render(request, 'predictor/index.html')

@csrf_exempt
def predict(request):
    global encoder, scaler

    if request.method == 'POST':
        try:
            data = request.POST.dict()
            # Convert string numeric values to the appropriate type
            data = {key: int(value) if value.isdigit() else value for key, value in data.items()}
            
            print("request.body", data)  # Use print() for debugging

            gender = data.get('Gender')
            weight = data.get('Weight')
            bmi = data.get('BMI')
            height = data.get('Height')
            age = data.get('Age')
            bmicase = data.get('BMIcase')

            # Fit the encoder on your training data before using it for transformation
            if not hasattr(encoder, 'categories_'):
                # Assuming you have a dataset called 'train_data' containing all the possible categories for 'Gender'
                train_data = [['Male'], ['Female']]  # Replace with your actual training data
                encoder.fit(train_data)

            # Fit the scaler on your training data before using it for transformation
            if not hasattr(scaler, 'mean_'):
                # Assuming you have a dataset called 'train_features' containing your training features
                train_features = [[50, 20, 150, 30]]  # Replace with your actual training features
                scaler.fit(train_features)

            # Preprocess the input data using the fitted encoder and scaler
            encoded_gender = encoder.transform([[gender]])
            scaled_features = scaler.transform([[weight, bmi, height, age]])

            # Dummy encode BMIcase
            bmicase_dummies = pd.get_dummies([bmicase], prefix='BMIcase')
            dummy_columns = bmicase_dummies.columns.tolist()

            # Combine features into a DataFrame
            features = pd.concat([pd.DataFrame(encoded_gender), pd.DataFrame(scaled_features)], axis=1)
            features = pd.concat([features, bmicase_dummies], axis=1)

            # Add missing columns with default value 0
            for col in expected_columns:
                if col not in features:
                    features[col] = 0

            # Ensure the feature DataFrame has the correct order of columns
            features = features[expected_columns]

            print("Feature names:", features.columns.tolist())

            # Make a prediction
            prediction = model.predict(features)
            return JsonResponse({'prediction': int(prediction[0])})
        
        except Exception as e:
            print("Error during prediction:", str(e))
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
