import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
import joblib

# Load dataset
df = pd.read_csv('final_dataset.csv')

# Handle missing values
df.fillna(method='ffill', inplace=True)

# Encode categorical variables (gender)
encoder = OneHotEncoder(sparse_output=False)
encoded_gender = encoder.fit_transform(df[['Gender']])

# One-hot encode BMICase column
encoded_bmicase = pd.get_dummies(df['BMIcase'])

# Normalize numerical features (weight, BMI, height, age)
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df[['Weight', 'BMI', 'Height', 'Age']])

# Combine features into a single DataFrame
features = pd.concat([pd.DataFrame(encoded_gender), pd.DataFrame(scaled_features), encoded_bmicase], axis=1)
features.columns = features.columns.astype(str)  # Convert feature names to strings
labels = df['Exercise Recommendation Plan']

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Hyperparameter tuning for KNN using GridSearchCV
param_grid = {'n_neighbors': [3, 5, 7, 9, 11]}
grid_search = GridSearchCV(KNeighborsClassifier(), param_grid, cv=5, scoring='accuracy')

try:
    grid_search.fit(X_train, y_train)
    best_knn = grid_search.best_estimator_
    best_knn.fit(X_train, y_train)
except Exception as e:
    print(f"Error during grid search fitting: {e}")
    best_knn = None  # Define best_knn as None in case of error

# Save the best KNN model if it's defined
if best_knn is not None:
    joblib.dump(best_knn, 'best_knn_model.pkl')
