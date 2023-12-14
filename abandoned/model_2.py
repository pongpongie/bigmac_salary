# pandas, matplotlib, seaborn csv 불러오기
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from IPython.display import set_matplotlib_formats
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

warnings.filterwarnings(action='ignore')
plt.rc('font', family='AppleGothic')
plt.rc('axes', unicode_minus=False)

# 데이터 불러오기
data =  pd.read_csv('/Users/pongpongi/Desktop/Machine Learining/project/연봉_예측/Salary.csv')
data = data.drop(['Race', 'Senior'], axis=1)

data['Job Title'] = data['Job Title'].replace('Front End Developer', 'Front end Developer')

include_titles = ['Software Engineer', 'Full Stack Engineer', 'Data Scientist',
                  'Software Engineer Manager', 'Data Analyst', 'Project Engineer',
                  'Back end Developer', 'Front end Developer', 'Software Developer',
                  'Web Developer','Director of Data Science']

data = data[data['Job Title'].isin(include_titles)]

numerical_columns = data.select_dtypes(include=['float64', 'int64']).columns
categorical_columns = ['Job Title', 'Gender', 'Education Level', 'Country']

le = LabelEncoder()
data['Age'] = data['Age'].astype(int)
data['Gender'] = le.fit_transform(data['Gender'])
data['Country'] = le.fit_transform(data['Country'])
data['Education Level'] = le.fit_transform(data['Education Level'])
data['Job Title'] = le.fit_transform(data['Job Title'])
data['Years of Experience'] = data['Years of Experience'].astype(int)
data['Country'] = le.fit_transform(data['Country'])

# 훈련 및 테스트 세트 분할
X = data.drop(['Salary'],axis =1)
y = data['Salary']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train RandomForestRegressor model
rf_model = RandomForestRegressor(random_state=42)
rf_model.fit(X_train, y_train)

# Save the model
joblib.dump(rf_model, 'salary_prediction_model_2.pkl')
