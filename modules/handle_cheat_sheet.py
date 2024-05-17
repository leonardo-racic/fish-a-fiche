from __future__ import annotations
from flask import Response, abort, redirect, flash, request, send_file, make_response
from singletons import render_html, get_form_data
from .server_account_manager import ServerAccountManager, get_hash
from .account_module import Account
from .cheat_sheet_manager import CheatSheetManager
from .cheat_sheet_module import CheatSheet
from environment_variable import reports_path, upload_path, cs_path
from terminal_log import inform, warn
from datetime import datetime
import json
import os


def get_current_date() -> str:
    now: datetime = datetime.now()
    date_str: str = now.strftime("%d/%m/%Y - %H:%M")
    return date_str


def get_comments(cheat_sheet_info: dict, sam: ServerAccountManager) -> list:
    comments = cheat_sheet_info["comments"]
    for i in range(len(comments)):
        current_comment: dict = comments[i]
        current_account: Account | None = sam.get_account_from_hashed_token(current_comment["token"])
        if isinstance(current_account, Account):
            comments[i]["username"] = current_account.username
        else:
            comments[i]["username"] = "DELETED_ACCOUNT;"
    return comments


def handle_cheat_sheet(
    cheat_sheet_manager: CheatSheetManager,
    server_account_manager: ServerAccountManager,
    token: str,
) -> Response:
    cheat_sheet_info: dict = cheat_sheet_manager.get_cheat_sheet_info(token)
    if request.method == "GET":
        if cheat_sheet_info == {}:
            flash("Cheat sheet info is not found", "danger")
            abort(404)
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


        user_token: str = server_account_manager.get_user_account_token()
        user_liked: bool = user_token in cheat_sheet_info["likes"]
        user_disliked: bool = user_token in cheat_sheet_info["dislikes"]


        return render_html(
            "cheat_sheet.html",
            server_account_manager,
            title=cheat_sheet_info["title"],
            is_author_dead=is_author_dead,
            cheat_sheet_token=token,
            author_username=author_username,
            author_hashed_token=author_hashed_token,
            user_liked=user_liked,
            is_user_author=is_user_author,
            context=cheat_sheet_info["context"],
            content=cheat_sheet_info["content"],
            date=cheat_sheet_info["date"],
            likes=len(cheat_sheet_info["likes"]),
            dislikes=len(cheat_sheet_info["dislikes"]),
            user_disliked=user_disliked,
            comments=comments,
            available_user_collections=available_user_collections,
            unavailable_user_collections=unavailable_user_collections,
        )
    

    elif request.method == "POST":
        form_data: dict = get_form_data()
        input_type: str = form_data["input_type"]
        if input_type == "comment_input":
            new_comment: dict = {
                "token": server_account_manager.get_user_account_hashed_token(),
                "content": form_data["comment"],
                "date": get_current_date(),
            }
            inform(f"New comment on CS {token}: {str(new_comment)}")
            cheat_sheet_manager.add_comment_to_cheat_sheet(token, new_comment)
        

        elif input_type == "delete_cheat_sheet_input":
            user_hashed_token: str = server_account_manager.get_user_account_hashed_token()
            user_token: str = server_account_manager.get_user_account_token()
            cheat_sheet_manager.delete_cheat_sheet(token)
            server_account_manager.delete_cheat_sheet(user_token, token)
            inform(f"CS ({token}) deleted")
            resp: Response = make_response(redirect(f"/profile/{user_hashed_token}"))
            return resp
        
        
        elif input_type == "delete_comment_input":
            comment_content: str = form_data["comment_content"]
            cheat_sheet_manager.remove_comment(token, comment_content)
            inform(f"Comment deleted with content: {comment_content}")


        elif input_type == "like_input":
            user_token: str = server_account_manager.get_user_account_token()
            liked: bool = user_token in cheat_sheet_info["likes"]
            cheat_sheet_token: str = cheat_sheet_info["token"]
            if user_token != "":
                if liked:
                    cheat_sheet_manager.remove_like(token, user_token)
                    inform(f"user({user_token}) unliked CS({cheat_sheet_token})")
                else:
                    cheat_sheet_manager.add_like(token, user_token)
                    cheat_sheet_manager.remove_dislike(token, user_token)
                    inform(f"user({user_token}) liked CS({cheat_sheet_token})")
            else:
                flash("You cannot like if you are not logged in", "error")


        elif input_type == "dislike_input":
            user_token: str = server_account_manager.get_user_account_token()
            cheat_sheet_token: str = cheat_sheet_info["token"]
            disliked: bool = user_token in cheat_sheet_info["dislikes"]
            if user_token != "":
                if disliked:
                    cheat_sheet_manager.remove_dislike(token, user_token)
                    inform(f"user({user_token}) undisliked CS({cheat_sheet_token})")
                else:
                    cheat_sheet_manager.add_dislike(token, user_token)
                    cheat_sheet_manager.remove_like(token, user_token)
                    inform(f"user({user_token}) disliked CS({cheat_sheet_token})")
            else:
                flash("You cannot dislike if you are not logged in", "error")
        

        elif input_type == "report_input":
            with open(reports_path) as f:
                reports_dict: dict = json.loads(f.read())
            reports: dict = reports_dict["reports"]
            if token not in reports["cheat_sheet"]:
                reports["cheat_sheet"].append(token)
                with open(reports_path, "w") as f:
                    f.write(json.dumps(reports_dict, indent=4))
                flash("Sucessfully reported!", "success")
                inform(f"CS({token}) has been reported")
            else:
                flash("It has already been reported", "warning")
                warn(f"CS({token}) has been reported once again")


        elif input_type == "download_input":
            with open(cs_path) as f:
                cs: dict = json.loads(f.read())["cheat_sheet"][token]
            content: str = cs["content"]
            title: str = form_data["title"]
            extension: str = "txt"
            file_path: str = os.path.join(upload_path, f"{token}.{extension}")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            resp: Response = make_response(
                send_file(file_path, as_attachment=True, download_name=f"{title}.{extension}") # type: ignore
            )
            return resp
            
        return make_response(redirect(f"/cheat-sheet/{token}"))
    else:
        return make_response("Method not supported")


def handle_create_cheat_sheet(
    cheat_sheet_manager: CheatSheetManager,
    server_account_manager: ServerAccountManager,
) -> Response:
    user_logged_in: bool = server_account_manager.is_user_logged_in()
    if request.method == "GET":
        if not user_logged_in:
            flash("You have to log in first!", "warning")
            return make_response(redirect("/sign-up"))
        return render_html(
            "create_cheat_sheet.html", 
            server_account_manager,
        )
    elif request.method == "POST":
        cheat_sheet_data: dict = get_form_data()
        if user_logged_in:
            cheat_sheet_data["author_token"] = server_account_manager.get_user_account_token()
            cheat_sheet: CheatSheet = cheat_sheet_manager.create_new_cheat_sheet(cheat_sheet_data)
            server_account_manager.add_cheat_sheet_to_user(cheat_sheet)
            flash('cheat-sheet created','success')
            inform(f"CS({cheat_sheet.token}) has been created")
            return make_response(redirect(f"/cheat-sheet/{cheat_sheet.token}"))
        else:
            flash('not logged in','warning')
            return render_html(
                "create_cheat_sheet.html",
                server_account_manager,
            )
    else:
        return make_response("Method not supported")


def handle_modify_cheat_sheet(
    cheat_sheet_manager: CheatSheetManager,
    server_account_manager: ServerAccountManager,
    token: str
) -> Response:
    if request.method == "POST":
        new_cheat_sheet_info: dict = get_form_data()
        cheat_sheet_manager.modify_cheat_sheet(token, new_cheat_sheet_info)
        flash('cheat-sheet modified','success')
        return make_response(redirect(f"/cheat-sheet/{token}"))
    elif request.method == "GET":
        cheat_sheet: CheatSheet | None = cheat_sheet_manager.get_cheat_sheet(token)
        if cheat_sheet is None:
            return Response(f"CheatSheet({token}) does not exist (is None).", status=404)
        cheat_sheet_info: dict = cheat_sheet.get_info()
        print(cheat_sheet_info)
        return render_html(
            "modify_cheat_sheet.html",
            server_account_manager,
            old_cheat_sheet=cheat_sheet_info,
        )
    else:
        return make_response("Method not supported")
