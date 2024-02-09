from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/")
def main():
    return render_template("website.html")


@app.route("/login", methods=["POST"])
def login():
    data = request.data
    print(data)