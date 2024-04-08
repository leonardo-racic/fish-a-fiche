import json
from singletons import render_html
from flask import Response, request, redirect, abort
from .server_account_manager import ServerAccountManager, get_hash
from environment_variable import cs_path, account_path


def get_profiles() -> list:
    with open(account_path) as f:
        data: dict = json.loads(f.read())["accounts"]
    for id, info in list(data.items()):
        data[id]["id"] = get_hash(info["id"])
    data_values: list = list(data.values())
    return data_values


def filter_title(name: str = "") -> list:
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


def filter_context(context: str = "") -> list:
    def filter_func(current_dict: dict) -> bool:
        current_context: str = current_dict["context"]
        condition: bool = False
        for keyword in context.split():
            if keyword in current_context.split():
                condition = True
                break
        return condition 

    with open(cs_path) as jsondata:
        data: dict = json.loads(jsondata.read())["cheat_sheet"]
    data_values: list = list(data.values())

    if context != "":
        result: list = list(filter(filter_func, data_values))
        return result
    return data_values


def filter_profiles(username: str = "") -> list:
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


def sort_results_by_likes(cs: list) -> list:
    def sort_func(current_cs: dict) -> int:
        dislikes: int = len(current_cs["dislikes"])
        likes: int = len(current_cs["likes"])
        difference: int = likes - dislikes
        return difference
    results: list = sorted(cs, key=sort_func, reverse=True)
    return results


def sort_results_by_keywords(cs: list, keywords: str = "") -> list:
    if keywords == "":
        return cs
    

    def sort_func(current_cs: dict) -> tuple:
        current_context: str = current_cs["context"]
        index = 0
        for k in keywords.split():
            if k in current_context.split():
                index += 1
        dislikes: int = len(current_cs["dislikes"])
        likes: int = len(current_cs["likes"])
        difference: int = likes - dislikes
        return index, difference
    results: list = sorted(cs, key=sort_func, reverse=True)
    return results


def handle_search(sam: ServerAccountManager, search: str) -> Response:
    if request.method == 'POST':
        title: str = request.form.get("title")
        search_by: str = request.form.get("search_by")
        return redirect(f'/search/{title}&{search_by}')
    else:
        try:
            search_data: str = search[:search.rindex("&")]
        except Exception:
            abort(404)
        search_by: str = search[search.rindex("&")+1:]
        profiles: list = filter_profiles(search_data)
        if search_by == "title":
            return render_html(
                'search.html',
                sam,
                search_title=search_data,
                profiles=profiles,
                search_by=search_by,
                cheat_sheet=sort_results_by_likes(filter_title(search_data)),
            )
        elif search_by == "context":
            return render_html(
                "search.html",
                sam,
                search_title=search_data,
                search_by=search_by,
                profiles=profiles,
                cheat_sheet=sort_results_by_keywords(filter_context(search_data), search_data),
            )
        return "oops"


def handle_search_empty(sam: ServerAccountManager) -> Response:
    if request.method == 'POST':
        title: str = request.form.get("title")
        search_by: str = request.form.get("search_by")
        return redirect(f'/search/{title}&{search_by}')
    else:
        return render_html(
            'search.html',
            sam,
            search_by="title",
            cheat_sheet=sort_results_by_likes(filter_title()),
            profiles=get_profiles(),
            search_title="",
        )

