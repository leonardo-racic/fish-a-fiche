from flask import Response, request
from singletons import render_html
from .server_account_manager import ServerAccountManager


def handle_features(sam: ServerAccountManager) -> Response:
    if request.method == "GET":
        return render_html(
            "features.html",
            sam,
        )
    else:
        return "I didn't code this yet"


def handle_home_page(sam: ServerAccountManager) -> Response:
    if request.method == "GET":
        account_info: dict = sam.get_user_account_info()
        logged_in: bool = sam.is_user_logged_in()
        if logged_in:
            return render_html(
                "home_page.html",
                sam,
                username=account_info["username"],
            )
        else:
            return render_html(
                "home_page.html",
                sam,
            )


def handle_about(sam: ServerAccountManager) -> Response:
    if request.method == "GET":
        return render_html("about.html", sam)