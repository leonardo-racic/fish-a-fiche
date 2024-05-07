from flask import Response, make_response, redirect, url_for


def handle_favicon() -> Response:
    return make_response(redirect(url_for("static", filename="favicon.ico")))