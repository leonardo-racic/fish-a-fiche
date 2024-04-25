from flask import Response, request
from singletons import render_html
from .server_account_manager import ServerAccountManager
from .sorting import sort_results_by_likes
from .filtering import filter_context
import json


def remove_duplicates(array: list) -> list:
    cleaned: list = []
    for i in array:
        if i not in cleaned:
            cleaned.append(i)
    return cleaned


categories: list = [
    "maths",
    "physics",
    "chemistry",
    "geography",
    "foreign-languages",
    "history",
    "geopolitics",
    "sociology",
    "economy",
    "art/art-history",
    "recipe/cuisine/gastronomy",
    "technology/it",
]


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


def handle_faqs(sam: ServerAccountManager) -> Response:
    if request.method == "GET":
        return render_html("faqs.html", sam)


def handle_cheat_sheet_market(sam: ServerAccountManager) -> Response:
    if request.method == "GET":
        data: dict = {}
        for category in categories:
            keywords: list = category.split("/")
            data[category] = []
            for keyword in keywords:
                cs: list = filter_context(keyword)
                data[category] += cs
            data[category] = remove_duplicates(data[category])
            data[category] = sort_results_by_likes(data[category])
        data_values: list = list(data.values())
        return render_html("cheat_sheet_market.html", sam, data=data_values)