from flask import Response, redirect, request
from singletons import render_html, get_form_data
from .server_account_manager import ServerAccountManager, get_hash
from .account_module import Account
from .cheat_sheet_manager import CheatSheetManager
from .cheat_sheet_module import CheatSheet


def get_comments(cheat_sheet_info: dict, sam: ServerAccountManager) -> list:
    comments = cheat_sheet_info["comments"]
    for i in range(len(comments)):
        current_comment: dict = comments[i]
        current_account: Account = sam.get_account_from_hashed_token(current_comment["token"])
        comments[i]["username"] = current_account.username
    return comments


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
        
        is_user_author: bool = server_account_manager.get_user_account_token() == cheat_sheet_info["author_token"]
        comments: list = get_comments(cheat_sheet_info, server_account_manager)
        author_hashed_token: str = get_hash(author_token)        

        return render_html(
            "cheat_sheet.html",
            server_account_manager,
            title=cheat_sheet_info["title"],
            cheat_sheet_token=token,
            author_username=author_username,
            author_hashed_token=author_hashed_token,
            is_user_author=is_user_author,
            context=cheat_sheet_info["context"],
            content=cheat_sheet_info["content"],
            date=cheat_sheet_info["date"],
            likes=cheat_sheet_info["likes"],
            dislikes=cheat_sheet_info["dislikes"],
            comments=comments,
        )
    

    elif request.method == "POST":
        form_data: dict = get_form_data()
        if form_data["input_type"] == "comment_input":
            new_comment: dict = {
                "token": server_account_manager.get_user_account_hashed_token(),
                "content": form_data["comment"]
            }
            cheat_sheet_manager.add_comment_to_cheat_sheet(token, new_comment)
        return redirect(f"/cheat-sheet/{token}")


def handle_create_cheat_sheet(
    cheat_sheet_manager: CheatSheetManager,
    server_account_manager: ServerAccountManager,
) -> Response:
    cheat_sheet_data: dict = get_form_data()
    if server_account_manager.is_user_logged_in():
        cheat_sheet_data["author_token"] = server_account_manager.get_user_account_token()
        cheat_sheet: CheatSheet = cheat_sheet_manager.create_new_cheat_sheet(cheat_sheet_data)
        server_account_manager.add_cheat_sheet_to_user(cheat_sheet)
        return redirect(f"/cheat-sheet/{cheat_sheet.token}")
    else:
        return render_html(
            "create_cheat_sheet.html",
            server_account_manager,
        )


def handle_modify_cheat_sheet(
    cheat_sheet_manager: CheatSheetManager,
    server_account_manager: ServerAccountManager,
    token: str
) -> Response:
    if request.method == "POST":
        new_cheat_sheet_info: dict = get_form_data()
        cheat_sheet_manager.modify_cheat_sheet(token, new_cheat_sheet_info)
        return redirect(f"/cheat-sheet/{token}")
    elif request.method == "GET":
        cheat_sheet: CheatSheet = cheat_sheet_manager.get_cheat_sheet(token)
        if cheat_sheet is None:
            return Response(f"CheatSheet({token}) does not exist (is None).", status=404)
        cheat_sheet_info: dict = cheat_sheet.get_info()
        return render_html(
            "modify_cheat_sheet.html",
            server_account_manager,
            old_cheat_sheet=cheat_sheet_info,
        )

    return "not done yet"