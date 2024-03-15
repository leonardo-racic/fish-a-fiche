from flask import Response, render_template, make_response, redirect, url_for, request
from .account_module import Account
from .server_account_manager import ServerAccountManager, get_hash
from json import dumps as dict_to_json




# Login
def handle_login(server_account_manager: ServerAccountManager) -> Response:
    error: str = ""
    if request.method == "POST":
        return handle_post_login(server_account_manager)    
    elif request.method == "GET":
        return render_template("login.html")
    else:
        error = f"I haven't coded login {request.method} code yet"

    return error


def handle_post_login(server_account_manager: ServerAccountManager) -> Response:
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
    

    target_account: Account = server_account_manager.get_account_by_username(input_username)
    response: Response = make_response(redirect(url_for("main")))
    response.set_cookie("account-token", target_account.get_id())
    return response



# Sign-up
def handle_sign_up(server_account_manager: ServerAccountManager) -> Response:
    error: str = ""
    if request.method == "POST":
        input_username: str = request.form.get("username", "")
        input_password: str = request.form.get("password", "")
        return handle_post_sign_up(server_account_manager, input_username, input_password)
    elif request.method == "GET":
        return render_template("sign_up.html")
    else:
        error = f"I haven't coded the {request.method} method yet."
        

    return error 


def handle_post_sign_up(server_account_manager: ServerAccountManager, input_username: str, input_password: str) -> Response:
    if server_account_manager.is_sign_up_input_valid(input_username, input_password):
        if server_account_manager.has_account_username(input_username):
            return render_template("sign_up.html", username_already_exists=True)
        else:
            new_account: Account = server_account_manager.create_account(input_username, input_password)
            response: Response = make_response(redirect(url_for("main")))
            response.set_cookie("account-token", new_account.get_id())
            return response
    return render_template("sign_up.html", input_not_valid=True)




# Sign-out
def handle_sign_out() -> Response:
    response: Response = make_response(redirect(url_for("main")))
    response.delete_cookie("account-token")
    return response




# Modify profile
def handle_modify_profile(server_account_manager: ServerAccountManager) -> Response:
    if request.method == "POST":
        return handle_post_modify_profile(server_account_manager)
    elif request.method == "GET":
        current_account_info: dict = server_account_manager.get_user_account_info()
        return render_template(
            "modify_user_profile.html",
            username=current_account_info["username"],
            description=current_account_info["description"],
            profile_picture=current_account_info["profile_picture"],
            logged_in=server_account_manager.is_user_logged_in(),
        )
    else:
        return f"I haven't coded the {request.method} method yet."


def handle_post_modify_profile(server_account_manager: ServerAccountManager) -> Response:
    new_image_input: str = request.form.get("new_image_input", "")
    description_input: str = request.form.get("description_input", "")
    username_input: str = request.form.get("username_input", "")
    if server_account_manager.has_account(server_account_manager.get_user_account()):
        server_account_manager.modify_profile(new_image_input, description_input, username_input)    
    return redirect("/")




# Display profile
def handle_profile(server_account_manager: ServerAccountManager, hashed_token: str) -> Response:
    account_info: dict = server_account_manager.get_account_info_from_hashed_token(hashed_token)
    does_account_exist: bool = account_info is not None
    logged_in: bool = server_account_manager.is_user_logged_in()
    if does_account_exist:
        user_account_info: dict = server_account_manager.get_user_account_info()
        response: Response = make_response(render_template(
            "user_profile.html",
            logged_in=logged_in,
            username=account_info["username"],
            description=account_info["description"],
            profile_picture=account_info["profile_picture"],
            is_user=bool(account_info["id"] == user_account_info["id"]),
            cheat_sheet=server_account_manager.get_account_cheat_sheet_info(account_info["id"])
        ))
        return response
    return "That account does not exist"