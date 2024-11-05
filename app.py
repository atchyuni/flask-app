from flask import Flask, render_template, request
import requests
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
    if " minus " in input:
        parts = input.split()
        total = int(parts[2]) - int(parts[4].replace("?", ""))
        return str(total)
    if " multiplied by " in input:
        parts = input.split()
        total = int(parts[2]) * int(parts[5].replace("?", ""))
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


@app.route("/github")
def get_githubname():
    return render_template("github_index.html")


def get_commit_info(repo_name):
    url = f"https://api.github.com/repos/{repo_name}/commits"
    commit_response = requests.get(url)

    if commit_response.status_code == 200:
        commits = commit_response.json()

        hash = commits[0]["sha"]
        date = commits[0]["commit"]["author"]["date"]
        author = commits[0]["commit"]["author"]["name"]
        message = commits[0]["commit"]["message"]

    return hash, date, author, message


def get_user_info(username):
    user_response = requests.get(f"https://api.github.com/users/{username}")

    if user_response.status_code == 200:
        user_info = user_response.json()

        bio = user_info["bio"]
        num_public_repos = user_info["public_repos"]
        account_created = user_info["created_at"]
        num_followers = user_info["followers"]
        num_following = user_info["following"]

    return bio, num_public_repos, account_created, num_followers, num_following


@app.route("/github_submit", methods=["POST"])
def github_submit():
    input_githubname = request.form.get("githubname")
    url = f"https://api.github.com/users/{input_githubname}/repos"
    response = requests.get(url)
    
    bio, num_public_repos, account_created, num_followers, num_following = \
        get_user_info(input_githubname)
    user_info = {
        "bio": bio,
        "num_public_repos": num_public_repos,
        "account_created": account_created,
        "num_followers": num_followers,
        "num_following": num_following
    }

    repos_list = []

    if response.status_code == 200:
        repos = response.json()
        # data returned is a list of ‘repository’ entities
        for repo in repos:
            # repos_list.append(repo["full_name"])
            hash, date, author, message = get_commit_info(repo["full_name"])
            repo_info = {
                "name": repo["full_name"],
                "date": date,
                "hash": hash,
                "author": author,
                "message": message,
                "repo_created": repo["created_at"]
            }
            repos_list.append(repo_info)

    return render_template(
        "github_submit.html", name=input_githubname,
        repos=repos_list, user=user_info
    )
