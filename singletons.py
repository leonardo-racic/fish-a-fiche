from __future__ import annotations
from werkzeug.datastructures import ImmutableMultiDict, FileStorage
from typing import Any
from flask import render_template, Response, request
import modules
import modules.server_account_manager


def get_form_data() -> dict[str, str]:
    form: ImmutableMultiDict = ImmutableMultiDict(request.form)
    try:
        return dict(form)
    except Exception:
        return {}


def get_form_files() -> dict[str, FileStorage]:
    files: ImmutableMultiDict = ImmutableMultiDict(request.files)
    try:
        return dict(files)
    except Exception:
        return {}


def get_form_file(name: str) -> FileStorage | None:
    return get_form_files().get(name)


def get_cookies() -> dict[str, str]:
    cookies: ImmutableMultiDict = ImmutableMultiDict(request.cookies)
    try:
        return dict(cookies)
    except Exception:
        return {}


def get_cookie(name: str) -> str:
    return get_cookies().get(name, "")


def render_html(
    template_name: str,
    sam: modules.server_account_manager.ServerAccountManager,
    **kwargs
) -> Response:
    return render_template(
        template_name,
        logged_in=sam.is_user_logged_in(),
        hashed_token=sam.get_user_account_hashed_token(),
        **kwargs
    )