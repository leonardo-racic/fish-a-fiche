from flask import Response
from singletons import render_html
from .server_account_manager import ServerAccountManager
from werkzeug.exceptions import NotFound as Error404

def handle_404(sam: ServerAccountManager, error: Error404) -> Response:
    return render_html(
        "error_404.html",
        sam,
        error_description=error.description,
    )