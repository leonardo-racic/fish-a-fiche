from flask import Flask, render_template, request, url_for, redirect
from account_module import Account
from server_account_manager import ServerAccountManager



app: Flask = Flask(__name__)
server_account_manager: ServerAccountManager = ServerAccountManager()







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

        is_input_valid: bool; username_exists: bool; password_correct: bool
        is_input_valid, username_exists, password_correct = server_account_manager.is_login_valid(input_username, input_password)
        
        
        if not is_input_valid:
            return render_template("login.html", input_not_valid=True)
        elif not username_exists:
            return render_template("login.html", username_does_not_exist=True)
        elif not password_correct:
            return render_template("login.html", password_incorrect=True)

        return redirect(url_for("main"))


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
        input_username: str = request.form.get("username", "")
        input_password: str = request.form.get("password", "")

        if server_account_manager.is_sign_up_input_valid(input_username, input_password):
            if server_account_manager.has_account_username(input_username):
                return render_template("sign_up.html", username_already_exists=True)
            else:
                server_account_manager.set_account(input_username, input_password)
                return redirect(url_for("main"))
        else:
            return render_template("sign_up.html", input_not_valid=True)


    elif request.method == "GET":
        return render_template("sign_up.html")
    
    else:
        error = f"I haven't coded the {request.method} method yet."
        

    return error