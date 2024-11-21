from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import joblib
import pandas as pd

app = Flask(__name__)
# Enable Cross-origin Requests
CORS(app)

client = MongoClient('mongodb://localhost:27017')
database = client['job_postings_db']
collection = database['postings']

# Load the trained model pipeline
model = joblib.load('model/decision_tree_model_pipeline.pkl')

# Retrieve jobs from MongoDB
@app.route('/api/random-posting', methods=['GET'])
def get_random_posting():
    # Fetch all job postings from database collection
    all_jobs = pd.DataFrame(list(collection.find()))

    # Prepare input data for model
    input_data = all_jobs[['title', 'description']]

    # Use Decision Tree to make predictions on all jobs in collection
    prediction = model.predict(input_data)

    # Add predictions to the DataFrame as new collection 
    all_jobs['prediction'] = prediction

    #Separate real and fake job postings based on model
    real_jobs = all_jobs[all_jobs['prediction'] == 0]
    fake_jobs = all_jobs[all_jobs['prediction'] == 1]

    # Create a 75/25 split of real to fake job postings
    num_fake = int(len(real_jobs) * 0.25)
    num_real = len(real_jobs) - num_fake

    # Make sample data set of real and fake job postings 
    sampled_fake_jobs = fake_jobs.sample(n=num_fake, replace=True)
    sampled_real_jobs = real_jobs.sample(n=num_real, replace=True)

    # Combine both sample sets
    combined_jobs = pd.concat([sampled_fake_jobs, sampled_real_jobs])

    #Randomly select one job from the combined set
    random_posting = combined_jobs.sample(n=1).iloc[0]

    # Extract posting data
    posting_data = {
        'title': random_posting.get('title'),
        'company': random_posting.get('company'),
        'location': random_posting.get('location'),
        'description': random_posting.get('description'),
    }

    # Return job posting data and prediction as JSON
    return jsonify({
        'posting': posting_data,
        'prediction': 'Real' if random_posting['prediction'] == 0 else 'Fake'
    })


if __name__ == '__main__':
    app.run(debug=True, port=5001)