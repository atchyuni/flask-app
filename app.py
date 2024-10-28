from flask import Flask, render_template, request
app = Flask(__name__)


def process_query(input):
    if input == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    if input == "What is your name?":
        return "ajc24"
    if " plus " in input:
        parts = input.split()
        total = int(parts[2]) + int(parts[4].replace("?", ""))
        return str(total)
    if "Which of the following numbers is the largest: " in input:
        parts = input.split()
        num1 = int(parts[8].replace(",", ""))
        num2 = int(parts[9].replace(",", ""))
        num3 = int(parts[10].replace("?", ""))
        return str(max(num1, num2, num3))
    return "Unknown"


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    return render_template("hello.html", name=input_name, age=input_age)


@app.route("/query", methods=["GET"])
def query():
    q = request.args.get("q")
    return process_query(q)
