import pandas as pd
from sklearn.linear_model import LinearRegression
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

data = pd.read_csv(os.path.join(BASE_DIR, "student_scores.csv"))

X = data[["Hours", "Attendance"]]
y = data["Score"]

model = LinearRegression()
model.fit(X, y)