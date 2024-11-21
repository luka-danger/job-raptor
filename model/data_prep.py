# %%
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# Load the dataset
data = pd.read_csv("data/fake_job_postings.csv")

# Inspect column names and structure
print(data.columns)
print(data.head())

# %%
# Preprocess dataset: drop rows with missing 'title', 'function' or 'description' values
data = data.dropna(subset=['title', 'description'])

# Features and target variable
X = data[['title', 'description']]
y = data['fraudulent']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define preprocessing for different columns
preprocessor = ColumnTransformer(
    transformers=[
        ('title', TfidfVectorizer(), 'title'),
        ('description', TfidfVectorizer(), 'description')  
    ])

# Create pipeline that transforms data and fits DecisionTreeClassifier with class weight
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),  
    ('classifier', DecisionTreeClassifier(class_weight='balanced'))  
])

# Train the model
pipeline.fit(X_train, y_train)

# Evaluate the model
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))

# Save trained model to file
joblib.dump(pipeline, 'decision_tree_model_pipeline.pkl')


# %%
# Load the trained model pipeline
model = joblib.load('decision_tree_model_pipeline.pkl')

# Example prediction
example = pd.DataFrame([{'title': 'Administrative Assistant', 'description': 'This is a fake job posting example'}])

# Predict using the loaded model
prediction = model.predict(example)
print("Prediction (fake job):", "Fake" if prediction[0] == 1 else "Real")



