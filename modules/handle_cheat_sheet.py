from flask import Response, abort, redirect, flash, request
from singletons import render_html, get_form_data
from .server_account_manager import ServerAccountManager, get_hash
from .account_module import Account
from .cheat_sheet_manager import CheatSheetManager
from .cheat_sheet_module import CheatSheet
from environment_variable import reports_path, upload_path
from terminal_log import inform
from datetime import datetime
from pdflatex import PDFLaTeX
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
        current_account: Account = sam.get_account_from_hashed_token(current_comment["token"])
        comments[i]["username"] = current_account.username
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
            cheat_sheet_manager.add_comment_to_cheat_sheet(token, new_comment)
        

        elif input_type == "delete_cheat_sheet_input":
            user_hashed_token: str = server_account_manager.get_user_account_hashed_token()
            user_token: str = server_account_manager.get_user_account_token()
            cheat_sheet_manager.delete_cheat_sheet(token)
            server_account_manager.delete_cheat_sheet(user_token, token)
            return redirect(f"/profile/{user_hashed_token}")
        
        
        elif input_type == "delete_comment_input":
            comment_content: str = form_data["comment_content"]
            cheat_sheet_manager.remove_comment(token, comment_content)
        

        elif input_type == "like_input":
            cheat_sheet_info: dict = cheat_sheet_manager.get_cheat_sheet_info(token)
            user_token: str = server_account_manager.get_user_account_token()
            liked: bool = user_token in cheat_sheet_info["likes"]
            
            if liked:
                cheat_sheet_manager.remove_like(token, user_token)
            else:
                cheat_sheet_manager.add_like(token, user_token)
                cheat_sheet_manager.remove_dislike(token, user_token)
        

        elif input_type == "dislike_input":
            cheat_sheet_info: dict = cheat_sheet_manager.get_cheat_sheet_info(token)
            user_token: str = server_account_manager.get_user_account_token()
            disliked: bool = user_token in cheat_sheet_info["dislikes"]
            
            if disliked:
                cheat_sheet_manager.remove_dislike(token, user_token)
            else:
                cheat_sheet_manager.add_dislike(token, user_token)
                cheat_sheet_manager.remove_like(token, user_token)
        

        elif input_type == "report_input":
            with open(reports_path) as f:
                reports_dict: dict = json.loads(f.read())
            reports: dict = reports_dict["reports"]
            if token not in reports["cheat_sheet"]:
                reports["cheat_sheet"].append(token)
                with open(reports_path, "w") as f:
                    f.write(json.dumps(reports_dict, indent=4))
                flash("Sucessfully reported!", "success")
            else:
                flash("It has already been reported", "warning")


        elif input_type == "download_input":
            title: str = cheat_sheet_info["title"]
            date: str = cheat_sheet_info["date"]
            author: str = server_account_manager.get_current_username_from_token(cheat_sheet_info["author_token"])
            content: str = cheat_sheet_info["content"]
            file_name: str = os.path.join(upload_path, f"{token}.tex")
            with open(file_name, "w") as file:
                print(type(file))
                file_content: str = f"\\documentclass\u007barticle\u007d\n" + \
                    f"\\title\u007b{title}\u007d\n\\date\u007b{date}\u007d\n\\author\u007b{author}\u007d\n" + \
                    f"\\begin\u007bdocument\u007d\n\\maketitle\n{content}\n\end\u007bdocument\u007d"
                file.write(file_content)
            #https://stackoverflow.com/questions/51711716/compile-latex-document-by-python
            #implement download
        return redirect(f"/cheat-sheet/{token}")


def handle_create_cheat_sheet(
    cheat_sheet_manager: CheatSheetManager,
    server_account_manager: ServerAccountManager,
) -> Response:
    user_logged_in: bool = server_account_manager.is_user_logged_in()
    if request.method == "GET":
        if not user_logged_in:
            flash("You have to log in first!", "warning")
            return redirect("/sign-up")
        return render_html(
            "create_cheat_sheet.html", 
            server_account_manager,
        )
    elif request.method == "POST":
        cheat_sheet_data: dict = get_form_data()
        if user_logged_in:
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