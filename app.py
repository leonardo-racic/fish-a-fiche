from flask import Flask, Response


from modules.server_account_manager import ServerAccountManager
from modules.cheat_sheet_manager import CheatSheetManager


from modules.handle_pages import handle_features, handle_home_page, handle_about, handle_faqs
from modules.handle_account_management import handle_login, handle_sign_up, handle_sign_out, handle_modify_profile, handle_profile
from modules.handle_search import handle_search , handle_search_empty
from modules.handle_cheat_sheet import handle_cheat_sheet, handle_create_cheat_sheet, handle_modify_cheat_sheet
from modules.handle_upload import handle_upload
from modules.handle_collections import handle_collections, handle_collection
from modules.handle_errors import handle_404


from terminal_log import run_logging
from werkzeug.exceptions import NotFound as Error404




run_logging()


app: Flask = Flask(__name__)
app.secret_key = "Sachin"
server_account_manager: ServerAccountManager = ServerAccountManager()
cheat_sheet_manager: CheatSheetManager = CheatSheetManager()


@app.route("/")
def main() -> Response:
    return handle_home_page(server_account_manager)


@app.route("/login", methods=["POST", "GET"])
def login() -> Response:
    return handle_login(server_account_manager)


@app.route("/sign-up", methods=["POST", "GET"])
def sign_up() -> Response:
    return handle_sign_up(server_account_manager)


@app.route("/profile/<string:hashed_token>", methods=["GET", "POST"])
def profile(hashed_token: str) -> Response:
    return handle_profile(server_account_manager, hashed_token)


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
    return handle_create_cheat_sheet(cheat_sheet_manager, server_account_manager)


@app.route("/cheat-sheet/<string:token>", methods=["GET", "POST"])
def cheat_sheet(token: str) -> Response:
    return handle_cheat_sheet(cheat_sheet_manager, server_account_manager, token)


@app.route("/modify-cheat-sheet/<string:token>", methods=["GET", "POST"])
def modify_cheat_sheet(token: str) -> Response:
    return handle_modify_cheat_sheet(cheat_sheet_manager, server_account_manager, token)


@app.route("/collections/<string:hashed_token>", methods=["GET", "POST"])
def collections(hashed_token: str) -> Response:
    return handle_collections(server_account_manager, hashed_token)


@app.route("/collections/<string:hashed_token>/<string:collection_name>", methods=["GET", "POST"])
def collection(hashed_token: str, collection_name: str) -> Response:
    return handle_collection(server_account_manager, cheat_sheet_manager, hashed_token, collection_name)


@app.route("/search/<string:name>", methods=["GET","POST"])
def search(name :str) -> Response:
    return handle_search(server_account_manager, name)


@app.route("/search/", methods=["GET",'POST'])
def search_empty() -> Response:
    return handle_search_empty(server_account_manager)


@app.errorhandler(404)
def error404(error: Error404) -> Response:
    return handle_404(server_account_manager, error), 404


@app.route("/features", methods=["GET"])
def features() -> Response:
    return handle_features(server_account_manager)


@app.route("/about")
def about() -> Response:
    return handle_about(server_account_manager)


@app.route("/faqs")
def faqs() -> Response:
    return handle_faqs(server_account_manager)


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
