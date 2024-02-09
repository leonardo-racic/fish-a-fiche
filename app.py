from flask import Flask, render_template, request


app: Flask = Flask(__name__)


def is_login_valid(username: str, password: str) -> bool:
    if username == "" or password == "":
        return False
    return True


@app.route("/")
def main() -> None:
    return render_template("login.html")


@app.route("/login", methods=["POST", "GET"])
def login() -> str:
    error: str = ""
    print("/login was accessed")
    if request.method == "POST":
        print("/login POST entered")
        input_username = request.form.get("username", "")
        input_password = request.form.get("password", "")
        if is_login_valid(input_username, input_password):
            return "<p>Logged in.</p>"
        else:
            error = "The password and/or the username is invalid."
            print(error)
    else:
        error = "I haven't coded the get method yet."

    return error