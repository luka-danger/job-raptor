from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Create Flask web app
app = Flask(__name__)

# Load the dataset from the CSV file
data = pd.read_csv('data/fake_job_postings.csv')

# Clean the dataset: Remove rows with missing title, function, or description
data = data.dropna(subset=['title', 'description'])

# Separate real and fake job postings
fake_jobs = data[data['fraudulent'] == 1]  # Fake job postings (fraudulent == 1)
real_jobs = data[data['fraudulent'] == 0]  # Real job postings (fraudulent == 0)

# Load the trained model pipeline
model = joblib.load('model/decision_tree_model_pipeline.pkl')

'''
Function: Generate random job posting

Description: This function loads a random job posting and predicts if
it is real or fake. It uses a sample split of 75% real job postings and
25% fake job postings to display the functionality of the model. After 
splitting the sample job postings, it combines into one set of sample
posts and then randomly selects one to predict via the trained model. 
The response (title, description, and prediciton) are returned
in JSON format. 

Example: 
A GET request to the '/random_job' endpoint will return a JSON response containing:
- A job title ('Administrative Assistant')
- A description ('This is a fake job posting example')
- The model's prediction: 'Fake' or 'Real' depending on the trained model's classification

Request:
GET /random_job

Response (Example):
{
    "job": {
        "description": "This is a fake job posting example"
        "title": "Administrative Assistant",
    },
    "prediction": "Fake"
}
'''
# Load a random job posting and predict if it is real or fake
@app.route('/random_job', methods=['GET', 'POST'])
def random_job():
    try:
        # Include a ratio of 75/25 real to fake job postings
        num_fake = int(len(real_jobs) * 0.25) 
        num_real = len(real_jobs) - num_fake    

        # Sample data set of real and fake jobs
        sampled_fake_jobs = fake_jobs.sample(n=num_fake, replace=True) 
        sampled_real_jobs = real_jobs.sample(n=num_real, replace=True)  

        # Combine the sampled jobs
        combined_jobs = pd.concat([sampled_fake_jobs, sampled_real_jobs])

        # Randomly select one job from the combined set
        random_job = combined_jobs.sample(n=1).iloc[0]

        # Extract the title, function, and description for prediction
        job_title = random_job['title']  
        description = random_job['description']

        # Prepare the data in the same format as the training data
        input_data = pd.DataFrame([{
            'title': job_title,
            'description': description
        }])

        # Use the trained model to make a prediction
        prediction = model.predict(input_data)

        # Return the job title, description, and prediction as JSON
        return jsonify({
            'job': {
                'title': job_title,  
                'description': description
            },
            'prediction': 'Fake' if prediction[0] == 1 else 'Real'
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)

# Use for Testing API
# curl http://ipaddress:Port/random_job