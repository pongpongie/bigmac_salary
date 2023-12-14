# pandas, matplotlib, seaborn csv 불러오기
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
from IPython.display import set_matplotlib_formats
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib


warnings.filterwarnings(action='ignore')

file_path = "/Users/pongpongi/Desktop/Machine Learining/project/연봉_예측/Salary.csv"

# 데이터 불러오기
data = pd.read_csv(file_path)

# 'Front End Developer'를 'Front end Developer'로 변경
data['Job Title'] = data['Job Title'].replace('Front End Developer', 'Front end Developer')

# 제외할 직종 목록
# exclude_titles = ['Copywriter', 'Data Entry Clerk', 'Director of Human Capital', 
#                   'Support Specialist', 'Technical Recruiter', 'Recruiter']

# # 제외할 직종 제거
# data = data[~data['Job Title'].isin(exclude_titles)]

# # IT 및 소프트웨어 관련 직종 필터링
# it_sw_keywords = ['Software', 'Developer', 'Engineer', 'Data', 'System', 'IT', 'Tech', 'Programmer', 'Web', 'Network']
# it_sw_related_jobs = data[data['Job Title'].str.contains('|'.join(it_sw_keywords), case=False)]

data = data.drop(['Race', 'Senior'], axis=1)

data['Job Title'] = data['Job Title'].replace('Front End Developer', 'Front end Developer')

include_titles = ['Software Engineer', 'Full Stack Engineer', 'Data Scientist',
                  'Software Engineer Manager', 'Data Analyst', 'Project Engineer',
                  'Back end Developer', 'Front end Developer', 'Software Developer',
                  'Web Developer','Director of Data Science']

# 원-핫 인코딩 적용
categorical_columns = ['Job Title', 'Gender', 'Education Level', 'Country', 'Race', 'Senior']
encoder = OneHotEncoder(sparse=False)
encoded_data = encoder.fit_transform(include_titles[categorical_columns])
encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(categorical_columns))
combined_data = pd.concat([include_titles.drop(categorical_columns, axis=1).reset_index(drop=True), encoded_df], axis=1)

# 'Country' 관련 원-핫 인코딩된 열들 찾기
# country_columns = [col for col in combined_data.columns if col.startswith('Country_')]

# # 'Job Title' 관련 원-핫 인코딩된 열들 찾기
# job_title_columns = [col for col in combined_data.columns if col.startswith('Job Title_')]

# # 각 국적별 직종별 종사자 수 계산
# country_job_title_counts = {}
# for country_col in country_columns:
#     country_data = combined_data[combined_data[country_col] == 1]
#     job_counts = country_data[job_title_columns].sum()
#     country_job_title_counts[country_col] = job_counts

# # 각 직업의 표본 수 계산
# job_title_sample_counts = combined_data[job_title_columns].sum(axis=0)

# # 표본 수가 10개 미만인 직업 확인
# low_sample_job_titles = job_title_sample_counts[job_title_sample_counts < 10].index

# # 이러한 직업을 가진 행들 제거
# for job_title_col in low_sample_job_titles:
#     combined_data = combined_data[combined_data[job_title_col] == 0]

# # 각 국가별 직종별 종사자 수 합계
# total_job_title_counts = pd.DataFrame(country_job_title_counts).sum(axis=1)

# # 합계가 0인 직군 제거
# filtered_job_titles = total_job_title_counts[total_job_title_counts > 0]

# # 각 'Job Title' 열에 대한 표본 수 계산
# job_title_sample_counts = combined_data[job_title_columns].sum()

# # 표본 수가 10개 미만인 'Job Title' 열 식별
# low_sample_job_titles = job_title_sample_counts[job_title_sample_counts < 10].index

# # 해당 열에서 값이 1인 행 제거
# for job_title_col in low_sample_job_titles:
#     combined_data = combined_data[combined_data[job_title_col] == 0]

# 훈련 및 테스트 세트 분할
X = combined_data.drop('Salary', axis=1)
y = combined_data['Salary']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 랜덤 포레스트 모델 재훈련 및 평가
rf_model = RandomForestRegressor(random_state=42)
rf_model.fit(X_train, y_train)
y_pred = rf_model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

# Save the model
joblib.dump(rf_model, 'salary_prediction_model.pkl')
