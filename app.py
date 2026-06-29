from flask import Flask, render_template, request
import pandas as pd
from sklearn.linear_model import LinearRegression
import os

app = Flask(__name__)

# Load dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data = pd.read_csv(os.path.join(BASE_DIR, "student_scores.csv"))

# Train model
X = data[["Hours", "Attendance"]]
y = data["Score"]

model = LinearRegression()
model.fit(X, y)


# -----------------------
# Routes
# -----------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        hours = float(request.form["hours"])
        attendance = float(request.form["attendance"])

        prediction = model.predict([[hours, attendance]])[0]

        prediction = round(prediction, 2)

        return render_template(
            "index.html",
            prediction_text=f"Predicted Score: {prediction}"
        )

    except Exception:
        return render_template(
            "index.html",
            prediction_text="Invalid Input!"
        )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)