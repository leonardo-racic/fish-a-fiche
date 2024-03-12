from flask import Response, render_template, request
from json import load, loads
from .server_account_manager import ServerAccountManager
from .cheat_sheet_manager import CheatSheetManager
from .cheat_sheet_module import CheatSheet


def handle_test(server_account_manager: ServerAccountManager) -> Response:
    with open("modules/cheat_sheet_test.json") as f:
        data = load(f)
    author_username: str = server_account_manager.get_current_username_from_token(data["author_token"])
    return render_template(
        "cheat_sheet.html",
        title=data["title"],
        author_username=author_username,
        is_logged_in=server_account_manager.is_user_logged_in(),
        context=data["context"],
        content=data["content"],
        date=data["date"],
        likes=data["likes"],
        dislikes=data["dislikes"],
        comments=data["comments"],
    )


def handle_cheat_sheet(
    cheat_sheet_manager: CheatSheetManager,
    server_account_manager: ServerAccountManager,
    token: str
) -> Response:
    cheat_sheet_info: dict = cheat_sheet_manager.get_cheat_sheet_info(token)
    author_token: str = cheat_sheet_info.get("author_token", "")
    author_username: str = server_account_manager.get_current_username_from_token(author_token)
    if cheat_sheet_info == {} or author_username == "":
        return Response("Well uhhhhh", status=404)


    return render_template(
        "cheat_sheet.html",
        title=cheat_sheet_info["title"],
        author_username=author_username,
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
) -> Response:
    cheat_sheet_data: dict = loads(request.data)
    print(cheat_sheet_data)
    cheat_sheet: CheatSheet = cheat_sheet_manager.create_new_cheat_sheet(cheat_sheet_data)
    return "RECEIVED"
    