from flask import Flask, render_template, request, url_for, redirect
from server_account_manager import ServerAccountManager



app: Flask = Flask(__name__)
server_account_manager: ServerAccountManager = ServerAccountManager()


def is_login_valid(username: str, password: str) -> bool:
    if username == "" or password == "":
        return False
    return True


@app.route("/")
def main() -> None:
    return render_template("home_page.html")


@app.route("/login", methods=["POST", "GET"])
def login() -> str:
    error: str = ""
    print("/login was accessed")


    if request.method == "POST":
        print("/login POST entered")
        input_username: str = request.form.get("username", "")
        input_password: str = request.form.get("password", "")
        if is_login_valid(input_username, input_password):
            return redirect(url_for('main'))
        else:
            error = "The password and/or the username is invalid."
            print(error)


    elif request.method == "GET":
        return render_template("login.html")
    

    else:
        error = f"I haven't coded login {request.method} code yet"

    return error


@app.route("/sign-up", methods=["POST", "GET"])
def sign_up() -> str:
    error: str = ""
    print("/sign-up was accessed")
    if request.method == "POST":
        print("/sign-up POST entered")
        input_username = request.form.get("username", "")
        input_password = request.form.get("password", "")


        if is_login_valid(input_username, input_password):
            server_account_manager.set_account(input_username, input_password)
            return redirect(url_for("main"))
        else:
            error = "The password and/or the username is invalid."
            print(error)


    elif request.method == "GET":
        return render_template("sign_up.html")
    
    else:
        error = "I haven't coded the get method yet."
        

    return error