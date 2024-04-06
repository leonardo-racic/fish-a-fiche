import json
from singletons import render_html
from flask import Response, request, redirect
from .server_account_manager import ServerAccountManager, get_hash
from environment_variable import cs_path, account_path


def get_profiles() -> list:
    with open(account_path) as f:
        data: dict = json.loads(f.read())["accounts"]
    for id, info in list(data.items()):
        data[id]["id"] = get_hash(info["id"])
    data_values: list = list(data.values())
    return data_values


def filter_title(name: str) -> list:
    def filter_func(current_dict: dict) -> bool:
        current_title: str = current_dict["title"]
        condition: bool = name.casefold() in current_title.casefold()
        return condition
    

    with open(cs_path) as jsondata:
        data: dict = json.loads(jsondata.read())["cheat_sheet"]
    data_values: list = list(data.values())


    if name != "":
        result: list = list(filter(filter_func, data_values))
        return result
    return data_values


def filter_profiles(username: str) -> list:
    def filter_func(current_dict: dict) -> bool:
        current_username: str = current_dict["username"]
        condition: bool = username.casefold() in current_username
        return condition


    data_values: list = get_profiles()
    if username != "":
        result: list = list(filter(filter_func, data_values))
        return result
    return data_values


def sort_results(cs: list, by: str) -> list:
    def sort_func(current_cs: dict) -> int:
        return len(current_cs[by])
    results: list = sorted(cs, reverse=True, key=sort_func)
    return results


def handle_search(sam: ServerAccountManager, name: str) -> Response:
    if request.method == 'POST':
        return redirect(f'/search/{request.form.get("title")}')
    else:
        profiles: list = filter_profiles(name)
        return render_html(
            'search.html',
            sam,
            search_title=name,
            profiles=profiles,
            cheat_sheet=sort_results(filter_title(name),'likes'),
        )


def handle_search_empty(sam: ServerAccountManager) -> Response:
    if request.method == 'POST':
        return redirect(f'/search/{request.form.get("title")}')
    else:
        return render_html(
            'search.html',
            sam,
            cheat_sheet=sort_results(filter_title(''), 'likes'),
            profiles=get_profiles(),
            search_title="",
        )
