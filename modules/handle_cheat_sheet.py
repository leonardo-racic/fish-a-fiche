from flask import Response, render_template, redirect, url_for, request
from json import load
from .server_account_manager import ServerAccountManager, get_hash
from .cheat_sheet_manager import CheatSheetManager
from .cheat_sheet_module import CheatSheet
from .account_module import Account


def get_form_data() -> dict:
    return dict(request.form)


def handle_cheat_sheet(
    cheat_sheet_manager: CheatSheetManager,
    server_account_manager: ServerAccountManager,
    token: str
) -> Response:
    if request.method == "GET":
        cheat_sheet_info: dict = cheat_sheet_manager.get_cheat_sheet_info(token)
        author_token: str = cheat_sheet_info["author_token"]
        author_username: str = server_account_manager.get_current_username_from_token(author_token)
        if cheat_sheet_info == {} or author_username == "":
            return Response("Well uhhhhh", status=404)


        comments: list = cheat_sheet_info["comments"]
        for i in range(len(comments)):
            comments[i]["username"] = server_account_manager.get_account_info_by_token(comments[i]["id"])["username"]
        

        return render_template(
            "cheat_sheet.html",
            title=cheat_sheet_info["title"],
            author_username=author_username,
            author_hashed_token=get_hash(author_token),
            token=get_hash(server_account_manager.get_user_account_token()),
            cheat_sheet_token=token,
            is_user_author=server_account_manager.get_user_account_token() == cheat_sheet_info["author_token"],
            logged_in=server_account_manager.is_user_logged_in(),
            context=cheat_sheet_info["context"],
            content=cheat_sheet_info["content"],
            date=cheat_sheet_info["date"],
            likes=cheat_sheet_info["likes"],
            dislikes=cheat_sheet_info["dislikes"],
            comments=cheat_sheet_info["comments"],
        )
    

    elif request.method == "POST":
        form_data: dict = get_form_data()
        content: str = form_data.get("comment_input")
        user_account_id: str = server_account_manager.get_user_account_token()
        new_comment: dict = {
            "content": content,
            "id": user_account_id
        }
        cheat_sheet_manager.add_comment_to_cheat_sheet(token, new_comment)
        return redirect(f"/cheat-sheet/{token}")


    return "not done yet"


def handle_create_cheat_sheet(
    cheat_sheet_manager: CheatSheetManager,
    server_account_manager: ServerAccountManager,
) -> Response:
    cheat_sheet_data: dict = get_form_data()
    if server_account_manager.is_user_logged_in():
        cheat_sheet_data["author_token"] = server_account_manager.get_user_account_token()
        cheat_sheet: CheatSheet = cheat_sheet_manager.create_new_cheat_sheet(cheat_sheet_data)
        server_account_manager.add_cheat_sheet_to_user(cheat_sheet)
        return redirect(url_for("main"))
    else:
        return render_template("create_cheat_sheet.html", logged_in=False)


def handle_modify_cheat_sheet(
    cheat_sheet_manager: CheatSheetManager,
    server_account_manager: ServerAccountManager,
    token: str
) -> Response:
    cheat_sheet: CheatSheet = cheat_sheet_manager.get_cheat_sheet(token)
    if cheat_sheet is None:
        return Response(f"CheatSheet({token}) does not exist.", status=404)
    if request.method == "POST":
        new_cheat_sheet_info: dict = get_form_data()
        cheat_sheet_manager.modify_cheat_sheet(token, new_cheat_sheet_info)
        return redirect(url_for("main"))
    elif request.method == "GET":
        return render_template(
            "modify_cheat_sheet.html",
            logged_in=server_account_manager.is_user_logged_in(),
            token=server_account_manager.get_user_account_token(),
            old_cheat_sheet=cheat_sheet.get_info()
        )

    return "not done yet"