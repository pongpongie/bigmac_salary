from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load the trained model
model = joblib.load('salary_prediction_model_2.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract data from request
    user_input = request.json

    # Create a DataFrame with the correct structure
    input_df = pd.DataFrame({
        'Age': [user_input['age']],
        'Gender': [user_input['gender']],
        'Education Level': [user_input['educationLevel']], 
        'Job Title': [user_input['jobTitle']],
        'Years of Experience': [user_input['yearsExperience']],
        'Country': [user_input['companyNation']],
    })

    # Use the model to make a prediction
    predicted_salary = model.predict(input_df)[0]

    return jsonify({"predictedSalary": predicted_salary})

if __name__ == '__main__':
    app.run(debug=True)
