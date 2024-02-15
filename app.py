from flask import Flask, Response, make_response, render_template, url_for, redirect, request
from server_account_manager import ServerAccountManager
from account_module import Account
from json import dumps as dict_to_json


app: Flask = Flask(__name__)
server_account_manager: ServerAccountManager = ServerAccountManager()


@app.route("/")
def main() -> Response:
    account_info: dict
    account_info, _ = server_account_manager.get_user_account_info()
    logged_in: bool = server_account_manager.is_user_logged_in()
    print(account_info, logged_in)
    if logged_in:
        return render_template("home_page.html", logged_in=logged_in, username=account_info["username"])
    else:
        return render_template("home_page.html")


def handle_post_login() -> Response:
    input_username: str = request.form.get("username", "")
    input_password: str = request.form.get("password", "")

    is_input_valid: bool; username_exists: bool; password_correct: bool
    is_input_valid, username_exists, password_correct = server_account_manager.is_login_valid(input_username, input_password)
    
    
    if not is_input_valid:
        return render_template("login.html", input_not_valid=True)
    elif not username_exists:
        return render_template("login.html", username_does_not_exist=True)
    elif not password_correct:
        return render_template("login.html", incorrect_password=True)
    

    target_account: Account
    target_account, _ = server_account_manager.get_account_by_username(input_username)
    response: Response = make_response(redirect(url_for("main")))
    response.set_cookie("account-info", dict_to_json(target_account.get_info()))
    return response


    


@app.route("/login", methods=["POST", "GET"])
def login() -> Response:
    error: str = ""
    print("/login was accessed")

    if request.method == "POST":
        print("/login POST entered")
        return handle_post_login()    
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
            new_account: Account = server_account_manager.create_account(input_username, input_password)
            response: Response = make_response(redirect(url_for("main")))
            response.set_cookie("account-info", dict_to_json(new_account.get_info()))
            
            return response
    return render_template("sign_up.html", input_not_valid=True)


@app.route("/sign-up", methods=["POST", "GET"])
def sign_up() -> Response:
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


@app.route("/profile/<string:username>", methods=["GET"])
def profile(username: str) -> Response:
    account_info: dict; does_account_exist: bool
    account_info, does_account_exist = server_account_manager.get_account_info_by_username(username)
    logged_in: bool = server_account_manager.is_user_logged_in()
    print(account_info, "line 100")
    if does_account_exist:
        user_account_info: dict
        user_account_info, _ = server_account_manager.get_user_account_info()
        response: Response = make_response(render_template(
            "user_profile.html",
            logged_in = logged_in,
            username = account_info["username"],
            description = account_info["description"],
            profile_picture = account_info["profile_picture"],
            is_user = username == user_account_info["username"]
        ))
        if username == user_account_info["username"]:
            user_account_info_bytes: str = dict_to_json(user_account_info)
            print(user_account_info_bytes, "This is the user's account info that is gonna be saved in the cookie")
            response.set_cookie("account-info", user_account_info_bytes)
        return response
    return render_template("user_profile.html")


def handle_post_modify_profile() -> Response:
    new_image_input: str = request.form.get("new_image_input", "")
    description_input: str = request.form.get("description_input", "")
    username_input: str = request.form.get("username_input", "")
    if server_account_manager.has_account(server_account_manager.get_user_account()):
        server_account_manager.modify_profile(new_image_input, description_input, username_input)
        user_account_info_bytes: bytes = dict_to_json(server_account_manager.get_user_account_info()[0])
        response: Response = make_response(redirect(url_for("profile", username=username_input)))
        response.set_cookie("account-info", user_account_info_bytes)
        return response
    

    user_account_info: dict = server_account_manager.get_user_account_info()[0]
    logged_in: bool = server_account_manager.is_user_logged_in()
    return render_template(
        "user_profile.html",
        logged_in = logged_in,
        username = user_account_info["username"],
        description = user_account_info["description"],
        profile_picture = user_account_info["profile_picture"],
        is_user = True,
    )


@app.route("/modify-profile", methods=["POST", "GET"])
def modify_profile() -> Response:
    if request.method == "POST":
        return handle_post_modify_profile()
    elif request.method == "GET":
        current_account_info: dict = server_account_manager.get_user_account_info()[0]
        print(current_account_info, current_account_info["description"])
        return render_template(
            "modify_user_profile.html",
            username = current_account_info["username"],
            description = current_account_info["description"],
            profile_picture = current_account_info["profile_picture"],
            logged_in = server_account_manager.is_user_logged_in(),
        )
    else:
        return f"I haven't coded the {request.method} method yet."


@app.route("/sign-out")
def sign_out() -> Response:
    response: Response = make_response(redirect(url_for("main")))
    response.set_cookie("account-info", "", expires=0)
    return response

