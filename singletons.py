from __future__ import annotations
from werkzeug.datastructures import ImmutableMultiDict, FileStorage
from flask import render_template, make_response, Response, request
import modules
import modules.server_account_manager
import environment_variable


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

    logged_in = sam.is_user_logged_in()
    if logged_in:
        profile_picture = sam.get_user_pfp_path()
    else:
        profile_picture = ""
    return make_response(
        render_template(
            template_name,
            logged_in=logged_in,
            user_profile_picture=profile_picture,
            hashed_token=sam.get_user_account_hashed_token(),
            **kwargs
        )
    )


def is_user_verified(
    hashed_token: str,
) -> bool:
    with open(environment_variable.verified_path) as f:
        hashed_tokens: list[str] = f.read().split("\n")
    print(hashed_token in hashed_tokens, hashed_token, hashed_tokens)
    return hashed_token in hashed_tokens