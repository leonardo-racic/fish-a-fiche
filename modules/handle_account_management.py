from flask import Response, make_response, redirect, url_for, flash, abort, request
from singletons import render_html, get_form_data
from .account_module import Account
from .server_account_manager import ServerAccountManager
from .cheat_sheet_manager import CheatSheetManager
from terminal_log import inform, warn, debug


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
        #error = f"I haven't coded login {request.method} code yet"
        warn(f'{request.remote_addr} used invalid method')
        flash('Invalid method', 'warning')
    return redirect('/login')


def handle_post_login(server_account_manager: ServerAccountManager) -> Response:
    input_username: str = request.form.get("username", "")
    input_password: str = request.form.get("password", "")

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
    
    target_account: Account = server_account_manager.get_account_by_username(input_username)
    response: Response = make_response(redirect(url_for("main")))
    response.set_cookie("account-token", target_account.get_id())
    inform(f'{request.remote_addr} has logged in as {input_username}')
    return response



# Sign-up
def handle_sign_up(server_account_manager: ServerAccountManager) -> Response:
    if request.method == "POST":
        input_username: str = request.form.get("username", "")
        input_password: str = request.form.get("password", "")
        return handle_post_sign_up(server_account_manager, input_username, input_password)
    elif request.method == "GET":
        return render_html(
            "sign_up.html",
            server_account_manager,
        )
    else:
        warn(f'{request.remote_addr} used invalid method')
        flash('This method does not exist', 'warning')
        return redirect('/sign-up')


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
    inform(f"{request.remote_addr}:{request.cookies.get('account-token')} has delogged")
    response.delete_cookie("account-token")
    return response


# Modify profile
def handle_modify_profile(server_account_manager: ServerAccountManager) -> Response:
    if request.method == "POST":
        return handle_post_modify_profile(server_account_manager)
    elif request.method == "GET":
        current_account_info: dict = server_account_manager.get_user_account_info()
        return render_html(
            "modify_user_profile.html",
            server_account_manager,
            username=current_account_info["username"],
            description=current_account_info["description"],
            profile_picture=current_account_info["profile_picture"],
            cheat_sheet=current_account_info["cheat_sheet"],
        )
    else:
        flash('This method does not exist', 'warning')
        warn(f'{request.remote_addr} used invalid method')
        return redirect('/')    


def handle_post_modify_profile(server_account_manager: ServerAccountManager) -> Response:
    new_image_input: str = request.form.get("new_image_input", "")
    description_input: str = request.form.get("description_input", "")
    username_input: str = request.form.get("username_input", "")
    if server_account_manager.has_account(server_account_manager.get_user_account()):
        server_account_manager.modify_profile(new_image_input, description_input, username_input)
        inform(f"{request.remote_addr}:{request.cookies.get('account-token')} modified {username_input}, with {new_image_input}, {description_input}")
        flash('Account has been successfully modified', 'success')
    else:
        warn(f'{request.remote_addr}:{server_account_manager.get_user_account()} tried to modify non existant account')
        flash('Account does not exist', 'warning') 
        abort(404)
    return redirect(f"/profile/{server_account_manager.get_user_account_hashed_token()}")




# Display profile
def handle_profile(server_account_manager: ServerAccountManager, hashed_token: str) -> Response:
    if request.method == "GET":
        account_info: dict = server_account_manager.get_account_info_from_hashed_token(hashed_token)
        does_account_exist: bool = account_info is not None
        if does_account_exist:
            user_account_info: dict = server_account_manager.get_user_account_info()
            #test if user logged in
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
                profile_picture=account_info["profile_picture"],
                is_user=is_user,
                cheat_sheet=server_account_manager.get_account_cheat_sheet_info(account_info["id"])
            ))
            return response
        flash('Account does not exist', 'warning')
        abort(404)

    
    elif request.method == "POST":
        form_data: dict = get_form_data()
        input_type: str = form_data["input_type"]
        if input_type == "delete_account_input":
            account: Account = server_account_manager.get_account_from_hashed_token(hashed_token)
            if account is None:
                flash("Account does not exist", "warning")
                abort(404)
            server_account_manager.delete_account(account)
            return redirect("/profile")



# Collections
def handle_collections(sam: ServerAccountManager, hashed_token: str) -> Response:
    target_account: Account = sam.get_account_from_hashed_token(hashed_token)
    debug(target_account)
    if target_account == None:
        collections = None
    else:
        collections: list = sam.get_collections(target_account.get_id())
    if collections is None:
        flash("Unexisting collections", "warning")
        abort(404)
    is_user: bool = hashed_token == sam.get_user_account_hashed_token()


    if request.method == "GET":
        return render_html(
            "collections.html",
            sam,
            username=target_account.get_username(),
            collections=collections,
            author_hashed_token=hashed_token,
            is_user=is_user,
        )
    

    elif request.method == "POST":
        form_data: dict = get_form_data()
        input_type: str = form_data.get("input_type")
        if input_type == "create_collection_input":
            collection_name: str = form_data["collection_name"]
            is_public: bool = bool(form_data.get("is_collection_public"))
            if sam.has_user_collection(collection_name):
                warn(f'{request.remote_addr}:{request.cookies.get("account-token")} tried to create already existing collection')
                flash('cCection already exists', 'warning')
                return render_html(
                    "collections.html",
                    sam,
                    username=target_account.get_username(),
                    collections=collections,
                    author_hashed_token=hashed_token,
                    is_user=is_user,
                )
            else:
                sam.add_new_collection_to_account(collection_name, target_account.get_id(), is_public)
                inform(f'{request.remote_addr}:{request.cookies.get("account-token")} created collection : {collection_name}, {target_account.id}, {is_public}')
                return redirect(f"/collections/{hashed_token}")
            

        elif input_type == "delete_collection_input":
            flash('Collection has been deleted', 'success')
            collection_name: str = form_data["collection_name"]
            sam.delete_collection(collection_name, target_account.get_id())
            inform(f'{request.remote_addr}:{request.cookies.get("account-token")} deleted collection {collection_name}')
            return redirect(f"/collections/{hashed_token}")
        

        elif input_type == "save_collection_input":
            flash('Collection has been saved', 'success')
            collection_name: str = form_data["collection_name"]
            cheat_sheet_token: str = form_data["cheat_sheet_token"]
            sam.save_to_collection(collection_name, cheat_sheet_token)
            inform(f'{request.remote_addr}:{request.cookies.get("account-token")} saved collection {collection_name}')
            return redirect(f"/cheat-sheet/{cheat_sheet_token}")
        

        elif input_type == "remove_cheat_sheet_input":
            flash('cheat-sheet removed','success')
            collection_name: str = form_data["collection_name"]
            cheat_sheet_token: str = form_data["cheat_sheet_token"]
            user_token: str = sam.get_user_account_token()
            sam.remove_cheat_sheet_from_collection(user_token, collection_name, cheat_sheet_token)
            inform(f'{request.remote_addr}:{request.cookies.get("account-token")} removed cheat-sheet: {cheat_sheet_token} from collection: {collection_name}')
            return redirect(f"/cheat-sheet/{cheat_sheet_token}")
        

    return "WIP, come back later! ^^"


def handle_collection(
    sam: ServerAccountManager,
    csm: CheatSheetManager,
    hashed_token: str,
    collection_name: str
) -> Response:
    
    author: Account = sam.get_account_from_hashed_token(hashed_token)
    is_user: bool = author.get_id() == sam.get_user_account_token()
    cheat_sheet_tokens: list = sam.get_cheat_sheet_token_from_collection(author.get_id(), collection_name)
    cheat_sheet_info = []
    if cheat_sheet_tokens is not None:
        for token in cheat_sheet_tokens:
            target_cheat_sheet_info: dict = csm.get_cheat_sheet_info(token)
            cheat_sheet_info.append(target_cheat_sheet_info)

    if request.method == "POST":
        form_data: dict = get_form_data()
        input_type: str = form_data.get("input_type")
        if input_type == "rename_collection_input":
            new_collection_name: str = form_data.get("collection_name")
            sam.rename_collection(author.get_id(), collection_name, new_collection_name)
            inform(f'{request.remote_addr}:{request.cookies.get("account-token")} renamed collection {collection_name}, to {new_collection_name}')
            flash('collection renamed','success')
            return redirect(f"/collections/{hashed_token}/{new_collection_name}")
        
        
        elif input_type == "publish_collection_input":
            sam.toggle_collection_visibility(author.get_id(), collection_name)
            flash('Visibility modified','success')
            inform(f'{request.remote_addr}:{request.cookies.get("account-token")} modified the visibility of {collection_name}')
            return redirect(f"/collections/{hashed_token}/{collection_name}")


        elif input_type == "remove_cheat_sheet_input":
            cheat_sheet_token: str = form_data["cheat_sheet_token"]
            user_token: str = sam.get_user_account_token()
            sam.remove_cheat_sheet_from_collection(user_token, collection_name, cheat_sheet_token)
            flash('Cheat-sheet has been removed', 'success')
            inform(f'{request.remote_addr}:{request.cookies.get("account-token")} removed cheat-sheet:{cheat_sheet_token} from collection {collection_name}')
            return redirect(f"/collections/{hashed_token}/{collection_name}")
        

    elif request.method == "GET":
        return render_html(
            "collection.html",
            sam,
            collection_name=collection_name,
            cheat_sheet=cheat_sheet_info,
            is_user=is_user,
            is_public=sam.is_collection_public(author.get_id(), collection_name),
        )
