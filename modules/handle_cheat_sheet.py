from flask import Response, render_template, redirect, request
from json import load
from .server_account_manager import ServerAccountManager
from .cheat_sheet_manager import CheatSheetManager
from .cheat_sheet_module import CheatSheet


def handle_cheat_sheet(
    cheat_sheet_manager: CheatSheetManager,
    server_account_manager: ServerAccountManager,
    token: str
) -> Response:
    cheat_sheet_info: dict = cheat_sheet_manager.get_cheat_sheet_info(token)
    author_token: str = server_account_manager.get_user_account_token()
    author_username: str = server_account_manager.get_current_username_from_token(author_token)
    if cheat_sheet_info == {} or author_username == "":
        return Response("Well uhhhhh", status=404)


    return render_template(
        "cheat_sheet.html",
        title=cheat_sheet_info["title"],
        cheat_sheet_token=token,
        author_username=author_username,
        hashed_token=server_account_manager.get_user_account_hashed_token(),
        is_logged_in=server_account_manager.is_user_logged_in(),
        context=cheat_sheet_info["context"],
        content=cheat_sheet_info["content"],
        date=cheat_sheet_info["date"],
        likes=cheat_sheet_info["likes"],
        dislikes=cheat_sheet_info["dislikes"],
        comments=cheat_sheet_info["comments"],
    )


def handle_create_cheat_sheet(
    cheat_sheet_manager: CheatSheetManager,
    server_account_manager: ServerAccountManager,
) -> Response:
    cheat_sheet_data: dict = dict(request.form)
    if server_account_manager.is_user_logged_in():
        cheat_sheet_data["author_token"] = server_account_manager.get_user_account_token()
        cheat_sheet: CheatSheet = cheat_sheet_manager.create_new_cheat_sheet(cheat_sheet_data)
        server_account_manager.add_cheat_sheet_to_user(cheat_sheet)
        return redirect("/")
    else:
        return render_template(
            "create_cheat_sheet.html",
            logged_in=False,
            hashed_token=server_account_manager.get_user_account_hashed_token(),
        )
    