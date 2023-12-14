from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load your trained model and encoder
# Update these paths to the actual paths where your model and encoder are saved
rf_model = joblib.load('salary_prediction_model_3.pkl')
encoder = joblib.load('encoder.pkl')

@app.route('/predict', methods=['POST'])
def predict_salary():
    # Get data from POST request
    data = request.get_json()

    # Convert the data to DataFrame
    input_df = pd.DataFrame([data])

    # Preprocess the data
    # One-hot encoding for 'Job Title', 'Country', and 'Gender'
    categorical_data = encoder.transform(input_df[['Job Title', 'Country', 'Gender']])
    encoded_df = pd.DataFrame(categorical_data.toarray(), columns=encoder.get_feature_names_out())

    # Combine the numeric data with the encoded categorical data
    numeric_data = input_df.drop(['Job Title', 'Country', 'Gender'], axis=1)
    final_input = pd.concat([numeric_data, encoded_df], axis=1)

    # Predict the salary
    predicted_salary = rf_model.predict(final_input)

    # Return the prediction
    return jsonify({'predicted_salary': predicted_salary[0]})

if __name__ == '__main__':
    app.run(debug=True)
