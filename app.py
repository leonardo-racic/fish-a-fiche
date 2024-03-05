from flask import Flask, Response, render_template, request
from server_account_manager import ServerAccountManager
from handle_account_management import handle_login, handle_sign_up, handle_sign_out, handle_modify_profile, handle_profile
from terminal_log import run_logging
from handle_upload import handle_upload


app: Flask = Flask(__name__)
server_account_manager: ServerAccountManager = ServerAccountManager()



@app.route("/")
def main() -> Response:
    account_info: dict = server_account_manager.get_user_account_info()
    logged_in: bool = server_account_manager.is_user_logged_in()
    if logged_in:
        return render_template("home_page.html", logged_in=logged_in, username=account_info["username"])
    else:
        return render_template("home_page.html")


@app.route("/login", methods=["POST", "GET"])
def login() -> Response:
    return handle_login(server_account_manager)


@app.route("/sign-up", methods=["POST", "GET"])
def sign_up() -> Response:
    return handle_sign_up(server_account_manager)


@app.route("/profile/<string:username>", methods=["GET"])
def profile(username: str) -> Response:
    return handle_profile(server_account_manager, username)


@app.route("/modify-profile", methods=["POST", "GET"])
def modify_profile() -> Response:
    return handle_modify_profile(server_account_manager)


@app.route("/sign-out")
def sign_out() -> Response:
    return handle_sign_out()


@app.route("/upload", methods=["POST", "GET"])
def search() -> Response:
    return handle_upload()

if __name__ == "__main__":
    run_logging()