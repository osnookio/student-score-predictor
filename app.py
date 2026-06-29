from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    hours = float(request.form["hours"])
    attendance = float(request.form["attendance"])

    prediction = model.predict([[hours, attendance]])

    return render_template(
        "index.html",
        prediction=round(prediction[0], 2)
    )

if __name__ == "__main__":
    app.run(debug=True)