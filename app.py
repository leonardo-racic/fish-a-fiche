from flask import Flask, Response, make_response, render_template, url_for, redirect, request
from account_module import Account
from server_account_manager import ServerAccountManager
from json import loads as json_to_dict, dumps as dict_to_json



app: Flask = Flask(__name__)
server_account_manager: ServerAccountManager = ServerAccountManager()


def get_account_info() -> dict:
    return json_to_dict(request.cookies.get("account-info", "{}"))


def is_logged_in(account_info: dict) -> bool:
    return account_info != {}


@app.route("/")
def main() -> None:
    account_info: dict = get_account_info()
    logged_in: bool = is_logged_in(account_info)
    if logged_in:
        return render_template("home_page.html", logged_in=logged_in, username=account_info["username"])
    else:
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


def handle_sign_up(input_username: str, input_password: str) -> Response:
    if server_account_manager.is_sign_up_input_valid(input_username, input_password):
        if server_account_manager.has_account_username(input_username):
            return render_template("sign_up.html", username_already_exists=True)
        else:
            account_info: dict = {
                "username": input_username,
                "profile_picture": "",
                "description": "..."
            }
            response: Response = make_response(redirect(url_for("main")))
            response.set_cookie("account-info", dict_to_json(account_info))
            return response
    return render_template("sign_up.html", input_not_valid=True)


@app.route("/sign-up", methods=["POST", "GET"])
def sign_up() -> str:
    error: str = ""
    print("/sign-up was accessed")

    if request.method == "POST":
        print("/sign-up POST entered")
        input_username: str = request.form.get("username", "")
        input_password: str = request.form.get("password", "")
        return handle_sign_up(input_username, input_password)


    elif request.method == "GET":
        return render_template("sign_up.html")
    

    else:
        error = f"I haven't coded the {request.method} method yet."
        

    return error


@app.route("/profile", methods=["GET"])
def profile() -> str:
    account_info: dict = get_account_info()
    logged_in: bool = is_logged_in(account_info)
    if logged_in:
        print(account_info)
        return render_template(
            "user_profile.html",
            logged_in = logged_in,
            username = account_info["username"],
            description = account_info["description"],
            profile_picture = account_info["profile_picture"],
        )
    return render_template("profile.html")