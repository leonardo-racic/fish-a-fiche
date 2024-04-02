import json
from singletons import render_html
import os
from flask import Flask, flash, request, redirect, render_template
import os.path
from .cheat_sheet_module import CheatSheet
from .server_account_manager import ServerAccountManager
from .cheat_sheet_manager import CheatSheetManager
import terminal_log


def check(name):
    return t[1]["title"] == name


def filter_title(name):
    with open('cheat_sheet.json') as jsondata:
        data: dict = json.loads(jsondata.read())["cheat_sheet"]

    return list(filter(lambda x:x[1]["title"] == name, list(data.items())))

def handle_search(server_account_manager,cheat_sheet_manager, name):

    return filter_title(name)

def handle_search_empty(sam,csm):

    if request.method == 'POST':
        terminal_log.inform(f'redirecting{request.form.get("title")}')
        return redirect(f'/search/{request.form.get("title")}')
    else:
        return render_html('search.html',sam)
