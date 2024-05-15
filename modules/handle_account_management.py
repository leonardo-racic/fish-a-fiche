from __future__ import annotations
from flask import Response, make_response, redirect, url_for, flash, abort, request
from singletons import render_html, get_form_data, get_cookie, get_form_file
from modules.account_module import Account
from modules.server_account_manager import ServerAccountManager
from modules.handle_upload import handle_profile_picture_upload
from environment_variable import reports_path
from terminal_log import inform, warn
from werkzeug.datastructures import FileStorage
import json


# Login
def handle_login(server_account_manager: ServerAccountManager) -> Response:
    if request.method == "POST":
        return handle_post_login(server_account_manager)    
    elif request.method == "GET":
        return render_html(
            "login.html",
            server_account_manager,
        )
    else:
        return make_response("Method not supported")


def handle_post_login(server_account_manager: ServerAccountManager) -> Response:
    form_data: dict = get_form_data()
    input_username: str = form_data.get("username", "")
    input_password: str = form_data.get("password", "")

    is_input_valid: bool; username_exists: bool; password_correct: bool
    is_input_valid, username_exists, password_correct = server_account_manager.is_login_valid(input_username, input_password)
    
    
    if not is_input_valid:
        flash('Invalid input', 'warning')
        warn(f'{request.remote_addr} entered invalid inputs : {input_username}, {input_password}')
        return render_html(
            "login.html",
            server_account_manager,
        )
    elif not username_exists:
        flash('Username does not exist', 'warning')
        warn(f'{request.remote_addr} has tried to log in as {input_username} with {input_password} but it does not exist')
        return render_html(
            "login.html",
            server_account_manager,
        )
    elif not password_correct:
        flash('Incorrect password', 'warning')
        warn(f'{request.remote_addr} has tried to log in as {input_username} but input the wrong password {input_password}')
        return render_html(
            "login.html",
            server_account_manager,
        )
    

    target_account: Account | None = server_account_manager.get_account_by_username(input_username)
    if isinstance(target_account, Account):
        response: Response = make_response(redirect(url_for("main")))
        response.set_cookie("account-token", target_account.get_id())
        inform(f'{request.remote_addr} has logged in as {input_username}')
        return response
    else:
        return make_response("/")



# Sign-up
def handle_sign_up(server_account_manager: ServerAccountManager) -> Response:
    if request.method == "POST":
        form_data: dict = get_form_data()
        input_username: str = form_data.get("username", "")
        input_password: str = form_data.get("password", "")
        return handle_post_sign_up(server_account_manager, input_username, input_password)
    elif request.method == "GET":
        return render_html(
            "sign_up.html",
            server_account_manager,
        )
    else:
        return make_response("Method not supported")


def handle_post_sign_up(server_account_manager: ServerAccountManager, input_username: str, input_password: str) -> Response:
    if server_account_manager.is_sign_up_input_valid(input_username, input_password):
        if server_account_manager.has_account_username(input_username):
            flash('Username is already used', 'warning')
            return render_html(
                "sign_up.html",
                server_account_manager,
            )
        else:
            flash('Account has been created', 'success')
            new_account: Account = server_account_manager.create_account(input_username, input_password)
            response: Response = make_response(redirect(url_for("main")))
            response.set_cookie("account-token", new_account.get_id())
            inform(f"user({new_account.get_id()}) has been signed in")
            return response
    warn(f'{request.remote_addr} gave invalid input {input_username}, {input_password}')
    flash('Invalid input', 'warning')
    return render_html(
        "sign_up.html",
        server_account_manager,
    )


# Sign-out
def handle_sign_out() -> Response:
    flash('Successfully signed out', 'info')
    response: Response = make_response(redirect(url_for("main")))
    inform(f"{request.remote_addr}:{get_cookie('account-token')} has delogged")
    response.delete_cookie("account-token")
    return response


# Modify profile
def handle_modify_profile(server_account_manager: ServerAccountManager) -> Response:
    if request.method == "POST":
        return handle_post_modify_profile(server_account_manager)
    elif request.method == "GET":
        current_account_info: dict = server_account_manager.get_user_account_info()
        if current_account_info == {}:
            flash("You are not logged in", "danger")
            abort(404)
        return render_html(
            "modify_user_profile.html",
            server_account_manager,
            username=current_account_info["username"],
            description=current_account_info["description"],
            cheat_sheet=current_account_info["cheat_sheet"],
        )
    else:
        return make_response("Method not supported")


def handle_post_modify_profile(server_account_manager: ServerAccountManager) -> Response:
    new_image_input: FileStorage | None = get_form_file("new_image_input")
    form_data: dict[str, str] = get_form_data()
    description_input: str = form_data.get("description_input", "")
    username_input: str = form_data.get("username_input", "")
    remove_pfp: str = form_data.get("remove_pfp", "")
    if server_account_manager.has_account(server_account_manager.get_user_account()):
        image_path: str = handle_profile_picture_upload(new_image_input, server_account_manager)
        server_account_manager.modify_profile(image_path, description_input, username_input, bool(remove_pfp))
        inform(f"{request.remote_addr}:{get_cookie('account-token')} modified {username_input}, with {image_path}, {description_input}")
        if image_path:
            flash('Account has been successfully modified', 'success')
    else:
        warn(f'{request.remote_addr}:{server_account_manager.get_user_account()} tried to modify non existant account')
        flash('Account does not exist', 'warning') 
        return make_response(abort(404))
    return make_response(
        redirect(f"/profile/{server_account_manager.get_user_account_hashed_token()}")
    )




# Display profile
def handle_profile(server_account_manager: ServerAccountManager, hashed_token: str) -> Response:
    if request.method == "GET":
        account_info: dict | None = server_account_manager.get_account_info_from_hashed_token(hashed_token)
        does_account_exist: bool = account_info is not None
        if does_account_exist:
            user_account_info: dict = server_account_manager.get_user_account_info()
            if user_account_info == {}:
                is_user = False
            else:
                is_user = bool(account_info["id"] == user_account_info["id"])
            response: Response = make_response(render_html(
                "user_profile.html",
                server_account_manager,
                username=account_info["username"],
                current_hashed_token=hashed_token,
                description=account_info["description"],
                is_user=is_user,
                cheat_sheet=server_account_manager.get_account_cheat_sheet_info(account_info["id"]),
                profile_picture=server_account_manager.get_pfp_path_from_hashed_token(hashed_token)
            ))
            return response
        flash('Account does not exist', 'warning')
        return make_response(abort(404))

    
    elif request.method == "POST":
        form_data: dict = get_form_data()
        input_type: str = form_data["input_type"]
        account: Account | None
        if input_type == "delete_account_input":
            account = server_account_manager.get_account_from_hashed_token(hashed_token)
            if account is None:
                flash("Account does not exist", "warning")
                abort(404)
            else:
                server_account_manager.delete_account(account)
                inform(f"user({account.get_id()}) has been deleted")
            return make_response(redirect("/profile"))
        

        elif input_type == "report_input":
            with open(reports_path) as f:
                reports_dict: dict = json.loads(f.read())
            reports: dict = reports_dict["reports"]
            hashed_account_id: str = form_data["hashed_account_id"]
            account = server_account_manager.get_account_from_hashed_token(hashed_account_id)
            if isinstance(account, Account):
                if account.get_id() not in reports["accounts"]:
                    reports["accounts"].append(account.get_id())
                    with open(reports_path, "w") as f:
                        f.write(json.dumps(reports_dict, indent=4))
                    flash("Sucessfully reported!", "success")
                    inform(f"user({account.get_id()}) has been reported")
                else:
                    flash("It has already been reported", "warning")
                    warn(f"user({account.get_id()}) has been reported once again")
            return make_response(redirect(f"/profile/{hashed_account_id}"))
    
        return make_response(redirect("/profile"))
    else:
        return make_response("Method not supported")