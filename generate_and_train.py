"""
generate_and_train.py
Run this ONCE to create the dataset and save the trained model.
Usage: python generate_and_train.py
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import pickle
import os

# ── 1. Generate synthetic dataset ──────────────────────────────────────────────
np.random.seed(42)
N = 500

hours_studied   = np.round(np.random.uniform(0, 10, N), 1)
attendance_pct  = np.round(np.random.uniform(30, 100, N), 1)

score = (
    5 * hours_studied
    + 0.4 * attendance_pct
    + np.random.normal(0, 4, N)
)
score = np.clip(np.round(score, 1), 0, 100)

df = pd.DataFrame({
    "hours_studied":   hours_studied,
    "attendance_pct":  attendance_pct,
    "exam_score":      score
})

os.makedirs("model", exist_ok=True)
df.to_csv("model/student_data.csv", index=False)
print(f"✅  Dataset saved  →  model/student_data.csv  ({N} rows)")

# ── 2. Train Linear Regression ─────────────────────────────────────────────────
X = df[["hours_studied", "attendance_pct"]]
y = df["exam_score"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mae    = mean_absolute_error(y_test, y_pred)
r2     = r2_score(y_test, y_pred)

print(f"✅  Model trained   →  MAE: {mae:.2f} pts  |  R²: {r2:.4f}")
print(f"   Coefficients    →  Hours: {model.coef_[0]:.3f}  |  Attendance: {model.coef_[1]:.3f}")
print(f"   Intercept       →  {model.intercept_:.3f}")

# ── 3. Save model ──────────────────────────────────────────────────────────────
with open("model/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅  Model saved     →  model/model.pkl")
print("\n🚀  Run  'python app.py'  to start the web application.")