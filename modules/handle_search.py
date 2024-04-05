import json
from singletons import render_html
import os
from flask import Flask, Response, flash, request, redirect, render_template
import os.path
from .cheat_sheet_module import CheatSheet
from .server_account_manager import ServerAccountManager
from .cheat_sheet_manager import CheatSheetManager
import terminal_log
from environment_variable import cs_path


def filter_title(name: str) -> list:
    def filter_func(current_dict) -> list:
        current_title: str = current_dict["title"]
        condition: bool = name.casefold() in current_title
        return condition
    

    with open(cs_path) as jsondata:
        data: dict = json.loads(jsondata.read())["cheat_sheet"]
    data_values: list = list(data.values())
    if name != "":
        result: list = list(filter(filter_func, data_values))
        return result
    else:
        return data_values


def sort_results(cs, by):
    results = sorted(cs,reverse=True, key=lambda d: d[by])
    return results


def handle_search(sam: ServerAccountManager, csm: CheatSheetManager, name: str) -> Response:
    if request.method == 'POST':
        return redirect(f'/search/{request.form.get("title")}')
    else:
        return render_html(
            'search.html',
            sam,
            cheat_sheet=sort_results(filter_title(name),'likes'),
        )


def handle_search_empty(sam: ServerAccountManager, csm: CheatSheetManager) -> Response:
    #same thing but simple cause you havent shearched anything yet
    if request.method == 'POST':
        return redirect(f'/search/{request.form.get("title")}')
    else:
        return render_html(
            'search.html',
            sam,
            cheat_sheet=sort_results(filter_title(''),'likes'),
        )
