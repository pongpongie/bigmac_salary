from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load the trained model
model = joblib.load('salary_prediction_model.pkl')

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/predict', methods=['POST'])
def predict():
    # Extract data from request
    user_input = request.json

    # Initialize DataFrame with zeros for all features
    feature_names = ['Age', 'Years of Experience', 'Job Title_Back end Developer',
       'Job Title_Chief Data Officer', 'Job Title_Chief Technology Officer',
       'Job Title_Data Analyst', 'Job Title_Data Engineer',
       'Job Title_Data Scientist', 'Job Title_Developer',
       'Job Title_Digital Content Producer',
       'Job Title_Digital Marketing Manager',
       'Job Title_Digital Marketing Specialist',
       'Job Title_Director of Data Science',
       'Job Title_Director of Engineering', 'Job Title_Engineer',
       'Job Title_Front end Developer', 'Job Title_Full Stack Engineer',
       'Job Title_IT Consultant', 'Job Title_IT Manager',
       'Job Title_IT Project Manager', 'Job Title_IT Support',
       'Job Title_IT Support Specialist', 'Job Title_Network Engineer',
       'Job Title_Principal Engineer', 'Job Title_Project Engineer',
       'Job Title_Quality Assurance Analyst', 'Job Title_Software Architect',
       'Job Title_Software Developer', 'Job Title_Software Engineer',
       'Job Title_Software Engineer Manager', 'Job Title_Software Manager',
       'Job Title_Software Project Manager',
       'Job Title_Technical Support Specialist', 'Job Title_Technical Writer',
       'Job Title_Web Designer', 'Job Title_Web Developer', 'Gender_Female',
       'Gender_Male', 'Education Level_0', 'Education Level_1',
       'Education Level_2', 'Education Level_3', 'Country_Australia',
       'Country_Canada', 'Country_China', 'Country_UK', 'Country_USA',
       'Race_African American', 'Race_Asian', 'Race_Australian', 'Race_Black',
       'Race_Chinese', 'Race_Hispanic', 'Race_Korean', 'Race_Mixed',
       'Race_Welsh', 'Race_White', 'Senior_0', 'Senior_1']
    
    input_df = pd.DataFrame(columns=feature_names, data=[{name: 0 for name in feature_names}])

    # Assign numerical features directly
    input_df['Age'] = user_input['age']
    input_df['Years of Experience'] = user_input['yearsExperience']

    # One-hot encoding for categorical features
    input_df[f'Job Title_{user_input["jobTitle"]}'] = 1
    input_df[f'Gender_{user_input["gender"]}'] = 1
    input_df[f'Education Level_{user_input["educationLevel"]}'] = 1
    input_df[f'Country_{user_input["companyNation"]}'] = 1
    input_df[f'Race_{user_input["race"]}'] = 1

    # Use the model to make a prediction
    predicted_salary = model.predict(input_df)[0]

    return jsonify({"predictedSalary": predicted_salary})

if __name__ == '__main__':
    app.run(debug=True)
