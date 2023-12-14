import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

file_path = "/Users/pongpongi/Desktop/Machine Learining/project/연봉_예측/Salary.csv"

# CSV 파일에서 데이터를 불러옵니다.
data = pd.read_csv(file_path)

# '인종'과 'senior'여부는 연구에서 중요하지 않으므로 'Race'와 'Senior' 열을 삭제합니다.
data = data.drop(['Race', 'Senior'], axis=1)
data = data[data['Years of Experience'] < 20] # 경력 연수가 20년 이상인 데이터는 제거합니다.
data = data[data['Age'] < 45] # 나이가 45세 이상인 데이터는 제거합니다.

# 관심있는 직업만 필터링합니다.
job_titles = ['Software Engineer', 'Full Stack Engineer', 'Data Scientist',
              'Software Engineer Manager', 'Data Analyst', 'Project Engineer',
              'Back end Developer', 'Front end Developer', 'Software Developer',
              'Web Developer', 'Director of Data Science']
data = data[data['Job Title'].isin(job_titles)]


encoder = OneHotEncoder() # 'Job Title', 'Country', 'Gender' 열에 대해 원-핫 인코딩을 수행합니다.
encoded_data = encoder.fit_transform(data[['Job Title', 'Country', 'Gender']]) 
encoded_df = pd.DataFrame(encoded_data.toarray(), columns=encoder.get_feature_names_out()) # 인코딩된 열을 데이터 프레임으로 변환합니다.

# 인코딩된 열을 나머지 데이터와 결합합니다.
data.reset_index(drop=True, inplace=True)
data = pd.concat([data.drop(['Job Title', 'Country', 'Gender'], axis=1), encoded_df], axis=1)

# 랜덤 포레스트에 사용할 데이터를 준비합니다.
X = data.drop('Salary', axis=1)
y = data['Salary']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 랜덤 포레스트 회귀 모델을 훈련합니다.
rf_model = RandomForestRegressor(random_state=42)
rf_model.fit(X_train, y_train)

# 모델을 사용하여 예측하고 평가합니다.
y_pred = rf_model.predict(X_test)
rmse = mean_squared_error(y_test, y_pred, squared=False)
r2 = r2_score(y_test, y_pred)

# 모델과 인코더를 파일로 저장합니다.
joblib.dump(rf_model, 'salary_prediction_model_4.pkl')
joblib.dump(encoder, 'encoder.pkl')
