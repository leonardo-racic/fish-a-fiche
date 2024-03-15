from flask import Flask, Response, render_template, request
from modules.server_account_manager import ServerAccountManager, get_hash
from modules.cheat_sheet_manager import CheatSheetManager
from modules.handle_account_management import handle_login, handle_sign_up, handle_sign_out, handle_modify_profile, handle_profile
from modules.handle_cheat_sheet import handle_cheat_sheet, handle_create_cheat_sheet
from modules.terminal_log import run_logging
from modules.handle_upload import handle_upload


app: Flask = Flask(__name__)
server_account_manager: ServerAccountManager = ServerAccountManager()
cheat_sheet_manager: CheatSheetManager = CheatSheetManager()


def sep() -> None:
    print("-" * 20)


@app.route("/")
def main() -> Response:
    account_info: dict = server_account_manager.get_user_account_info()
    logged_in: bool = server_account_manager.is_user_logged_in()
    if logged_in:
        hashed_token: str = get_hash(account_info["id"])
        return render_template(
            "home_page.html",
            logged_in=logged_in,
            username=account_info["username"],
            hashed_token=hashed_token,
        )
    else:
        return render_template("home_page.html")


@app.route("/login", methods=["POST", "GET"])
def login() -> Response:
    return handle_login(server_account_manager)


@app.route("/sign-up", methods=["POST", "GET"])
def sign_up() -> Response:
    return handle_sign_up(server_account_manager)


@app.route("/profile/<string:hashed_token>", methods=["GET"])
def profile(hashed_token: str) -> Response:
    resp: Response = handle_profile(server_account_manager, hashed_token)
    return resp


@app.route("/modify-profile", methods=["POST", "GET"])
def modify_profile() -> Response:
    return handle_modify_profile(server_account_manager)


@app.route("/sign-out")
def sign_out() -> Response:
    return handle_sign_out()


@app.route("/upload", methods=["POST", "GET"])
def upload() -> Response:
    print("upload starting")
    return handle_upload(server_account_manager)


@app.route("/create-cheat-sheet", methods=["GET", "POST"])
def create_cheat_sheet() -> Response:
    if request.method == "GET":
        return render_template(
            "create_cheat_sheet.html", 
            logged_in=server_account_manager.is_user_logged_in(),
            token=server_account_manager.get_user_account_token(),
        )
    elif request.method == "POST":
        return handle_create_cheat_sheet(cheat_sheet_manager, server_account_manager)
    return "METHOD UNKNOWN"



@app.route("/cheat-sheet/<string:token>")
def cheat_sheet(token: str) -> Response:
    return handle_cheat_sheet(cheat_sheet_manager, server_account_manager, token)


if __name__ == "__main__":
    app.run(debug=True)
    run_logging()
