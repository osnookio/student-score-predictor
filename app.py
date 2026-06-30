"""
app.py  –  Student Score Predictor (Flask backend)
Run:  python app.py
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import pickle, os, json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "student_score_secret_2024"

MODEL_PATH = os.path.join("model", "model.pkl")
USERS_PATH = os.path.join("model", "users.json")

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model not found. Run 'python generate_and_train.py' first.")
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

def load_users():
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH) as f:
        return json.load(f)

def save_users(users):
    os.makedirs("model", exist_ok=True)
    with open(USERS_PATH, "w") as f:
        json.dump(users, f, indent=2)

@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("predict_page"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not name or not email or not password:
            flash("All fields are required.", "error")
            return render_template("signup.html")
        users = load_users()
        if email in users:
            flash("Email already registered. Please log in.", "error")
            return render_template("signup.html")
        users[email] = {"name": name, "password": generate_password_hash(password)}
        save_users(users)
        flash("Account created! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        users = load_users()
        user  = users.get(email)
        if user and check_password_hash(user["password"], password):
            session["user"] = email
            session["name"] = user["name"]
            return redirect(url_for("predict_page"))
        flash("Invalid email or password.", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/predict", methods=["GET"])
def predict_page():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("predict.html", name=session.get("name", ""))

@app.route("/api/predict", methods=["POST"])
def api_predict():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    try:
        hours      = float(data["hours"])
        attendance = float(data["attendance"])
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "Invalid input"}), 400
    if not (0 <= hours <= 24):
        return jsonify({"error": "Hours must be between 0 and 24."}), 400
    if not (0 <= attendance <= 100):
        return jsonify({"error": "Attendance must be between 0 and 100."}), 400
    model = load_model()
    score = model.predict([[hours, attendance]])[0]
    score = round(float(max(0, min(100, score))), 1)
    if score >= 90:
        grade, msg = "A+", "Outstanding performance!"
    elif score >= 80:
        grade, msg = "A", "Excellent work!"
    elif score >= 70:
        grade, msg = "B", "Good performance."
    elif score >= 60:
        grade, msg = "C", "Average — there's room to improve."
    elif score >= 50:
        grade, msg = "D", "Below average — consider studying more."
    else:
        grade, msg = "F", "At risk — significant improvement needed."
    return jsonify({"score": score, "grade": grade, "message": msg})

if __name__ == "__main__":
    app.run(debug=True, port=5000)