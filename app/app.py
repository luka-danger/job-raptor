from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Create Flask web app
app = Flask(__name__)

# Load Trained Decision Tree model
model = joblib.load('model/decision_tree_model_pipeline.pkl')


@app.route('/predict', methods=['POST'])
# Get data from POST request
def predict():
    data = request.get_json()

    if 'function' not in data or 'description' not in data:
        return jsonify({'error': 'Missing required fields: "function" and "description"'}), 400
    
    # Prepare input data
    input_data = pd.DataFrame([{
        'function': data['function'],
        'description': data['description']
    }])

    # Use model to make prediction on job post (ex: real or fake)
    prediction = model.predict(input_data)

    return jsonify({'prediction': 'Fake' if prediction[0] == 1 else 'Real'})

if __name__ == '__main__':
    app.run(debug=True)