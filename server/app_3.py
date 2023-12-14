from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)

model = joblib.load('salary_prediction_model_4.pkl')
encoder = joblib.load('encoder.pkl')

job_title_mapping = {
    0: 'Back end Developer', 1: 'Data Analyst', 2: 'Data Scientist',
    3: 'Front end Developer', 4: 'Full Stack Engineer', 5: 'Project Engineer',
    6: 'Software Developer', 7: 'Software Engineer', 8: 'Software Engineer Manager',
    9: 'Web Developer'
}
country_mapping = {
    0: 'Australia', 1: 'China', 2: 'Canada', 3: 'UK', 4: 'USA'
}
gender_mapping = {0: 'Female', 1: 'Male'}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    job_title = job_title_mapping[int(data['jobTitle'])]
    country = country_mapping[int(data['companyNation'])]
    gender = gender_mapping[int(data['gender'])]

    input_data_for_encoding = pd.DataFrame([[job_title, country, gender]], 
                                           columns=['Job Title', 'Country', 'Gender'])

    encoded_input_data = encoder.transform(input_data_for_encoding)

    try:
        encoded_df = pd.DataFrame(encoded_input_data.toarray(), columns=encoder.get_feature_names_out())
    except ValueError as e:
        print("Error in DataFrame creation:", e)
        print("Columns expected:", encoder.get_feature_names_out())
        return jsonify({"error": str(e)})

    final_input_df = pd.DataFrame({
        'Age': [int(data['age'])],
        'Education Level': [int(data['educationLevel'])],
        'Years of Experience': [int(data['yearsExperience'])]
    })

    final_input_df = pd.concat([final_input_df, encoded_df], axis=1)

    expected_feature_names = model.feature_names_in_ 
    final_input_df = final_input_df.reindex(columns=expected_feature_names, fill_value=0)

    predicted_salary = model.predict(final_input_df)[0]

    return jsonify({"predictedSalary": predicted_salary})

@app.route('/predictSalaryByExperience', methods=['POST'])
def predict_salary_by_experience():
    data = request.json
    job_title = job_title_mapping[int(data['jobTitle'])]
    country = country_mapping[int(data['companyNation'])]
    gender = gender_mapping[int(data['gender'])]

    # 나머지 사용자 입력은 고정하고, 오직 경력 연수만 변화시킵니다.
    base_input_data = {
        'Age': int(data['age']),
        'Education Level': int(data['educationLevel']),
        # 다른 필요한 입력 값들도 포함시킵니다.
    }

    # 1년부터 10년까지의 경력 연수에 대한 예측을 수행합니다.
    salary_predictions = {}
    for years_of_experience in range(0, 11):
        input_data_for_encoding = pd.DataFrame([[job_title, country, gender]], 
                                               columns=['Job Title', 'Country', 'Gender'])

        encoded_input_data = encoder.transform(input_data_for_encoding)
        # toarray() 함수를 사용하여 인코딩된 데이터를 배열로 변환
        encoded_df = pd.DataFrame(encoded_input_data.toarray(), columns=encoder.get_feature_names_out())

        final_input_df = pd.DataFrame(base_input_data, index=[0]) # 인덱스를 명시적으로 지정
        final_input_df['Years of Experience'] = [years_of_experience]
        final_input_df = pd.concat([final_input_df, encoded_df], axis=1)

        # 모델의 입력 순서에 맞게 컬럼을 재정렬합니다.
        final_input_df = final_input_df.reindex(columns=model.feature_names_in_, fill_value=0)

        # 연봉 예측 수행
        predicted_salary = model.predict(final_input_df)[0]
        salary_predictions[years_of_experience] = predicted_salary

    return jsonify(salary_predictions)

    
if __name__ == '__main__':
    app.run(debug=True)
