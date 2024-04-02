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

    return dict(filter(lambda x:x[1]["title"] == name, list(data.items())))

def handle_search(sam,csm, name):
    if request.method == 'POST':
        terminal_log.debug(f'redirecting to /search/{request.form.get("title")}')
        return redirect(f'/search/{request.form.get("title")}')
    else:
        terminal_log.debug(filter_title(name))
        terminal_log.debug(type(filter_title(name)))
        list_of_data = list(filter_title(name).values())
        terminal_log.debug(type(list_of_data))
        terminal_log.debug(list_of_data)
        return render_template('search.html',
                                logged_in=sam.is_user_logged_in(),
                                hashed_token=sam.get_user_account_hashed_token(),
                                cheat_sheet=list_of_data,
                                )

def handle_search_empty(sam,csm):

    if request.method == 'POST':
        terminal_log.debug(f'redirecting to /search/{request.form.get("title")}')
        return redirect(f'/search/{request.form.get("title")}')
    else:
        return render_template('search.html',
                               logged_in=sam.is_user_logged_in(),
                               hashed_token=sam.get_user_account_hashed_token(),
                               cheat_sheet=[],
                               )
