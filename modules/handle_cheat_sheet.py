from flask import Response, redirect, flash, request
from singletons import render_html, get_form_data
from .server_account_manager import ServerAccountManager, get_hash
from .account_module import Account
from .cheat_sheet_manager import CheatSheetManager
from .cheat_sheet_module import CheatSheet
from terminal_log import inform
from datetime import datetime


def get_current_date() -> str:
    now: datetime = datetime.now()
    date_str: str = now.strftime("%d/%m/%Y - %H:%M")
    return date_str


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
        is_author_dead: bool = cheat_sheet_info == {} or author_username == ""
        comments: list = get_comments(cheat_sheet_info, server_account_manager)
        available_user_collections: list = []
        unavailable_user_collections: list = []
        if server_account_manager.is_user_logged_in():
            user_collections: list = server_account_manager.get_user_account_collections()
            for c in user_collections:
                if token in c["cheat_sheet"]:
                    unavailable_user_collections.append(c)
                else:
                    available_user_collections.append(c)
        author_hashed_token: str = get_hash(author_token)
        if not is_author_dead:
            is_user_author: bool = server_account_manager.get_user_account_token() == cheat_sheet_info["author_token"]
        else:
            is_user_author: bool = False


        return render_html(
            "cheat_sheet.html",
            server_account_manager,
            title=cheat_sheet_info["title"],
            is_author_dead=is_author_dead,
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
            available_user_collections=available_user_collections,
            unavailable_user_collections=unavailable_user_collections,
        )
    

    elif request.method == "POST":
        form_data: dict = get_form_data()
        if form_data["input_type"] == "comment_input":
            new_comment: dict = {
                "token": server_account_manager.get_user_account_hashed_token(),
                "content": form_data["comment"],
                "date": get_current_date(),
            }
            cheat_sheet_manager.add_comment_to_cheat_sheet(token, new_comment)
        

        elif form_data["input_type"] == "delete_cheat_sheet_input":
            user_hashed_token: str = server_account_manager.get_user_account_hashed_token()
            user_token: str = server_account_manager.get_user_account_token()
            cheat_sheet_manager.delete_cheat_sheet(token)
            server_account_manager.delete_cheat_sheet(user_token, token)
            return redirect(f"/profile/{user_hashed_token}")
        
        
        elif form_data["input_type"] == "delete_comment_input":
            comment_content: str = form_data["comment_content"]
            cheat_sheet_manager.remove_comment(token, comment_content)
        return redirect(f"/cheat-sheet/{token}")


def handle_create_cheat_sheet(
    cheat_sheet_manager: CheatSheetManager,
    server_account_manager: ServerAccountManager,
) -> Response:
    cheat_sheet_data: dict = get_form_data()
    if server_account_manager.is_user_logged_in():
        inform('creating cheat_sheet')
        cheat_sheet_data["author_token"] = server_account_manager.get_user_account_token()
        cheat_sheet: CheatSheet = cheat_sheet_manager.create_new_cheat_sheet(cheat_sheet_data)
        server_account_manager.add_cheat_sheet_to_user(cheat_sheet)
        inform('cheat-sheet created')
        flash('cheat-sheet created','success')
        return redirect(f"/cheat-sheet/{cheat_sheet.token}")
    else:
        flash('not logged in','warning')
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
        flash('cheat-sheet modified','success')
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
    flash('method not suported','warning')