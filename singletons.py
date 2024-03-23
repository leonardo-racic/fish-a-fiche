from flask import render_template, Response, request
from modules.server_account_manager import ServerAccountManager


def get_form_data() -> dict:
    return dict(request.form)


def render_html(template_name: str, sam: ServerAccountManager, **kwargs) -> Response:
    return render_template(
        template_name,
        logged_in=sam.is_user_logged_in(),
        hashed_token=sam.get_user_account_hashed_token(),
        **kwargs
    )