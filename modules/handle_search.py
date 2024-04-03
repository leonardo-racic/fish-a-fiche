import json
from singletons import render_html
import os
from flask import Flask, flash, request, redirect, render_template
import os.path
from .cheat_sheet_module import CheatSheet
from .server_account_manager import ServerAccountManager
from .cheat_sheet_manager import CheatSheetManager
import terminal_log
from environment_variable import cs_path


def filter_title(name):
    #this shit is super confusing (at least to me) so let me explain to you:
    #open cheat_sheet.json
    with open(cs_path) as jsondata:
        #say that our dictionary data is what is inside of cheat_sheet basically but loaded whatever that means
        data: dict = json.loads(jsondata.read())["cheat_sheet"]
    #return a dictionnary verion of the filterd version of our items in data (but they are in a list). we use lambda as a filter because we could not figure out how to use a normal fuction so here cgoes a confusing syntax that say if title = name say True else say no.
    return list(dict(filter(lambda x:name in x[1]["title"], list(data.items()))).values())


def sort_results(cs, by):
    results = sorted(cs,reverse=True, key=lambda d: d[by])
    return results
def handle_search(sam,csm, name):
    if request.method == 'POST':
        return redirect(f'/search/{request.form.get("title")}')
    else:

        return render_template('search.html',
                                logged_in=sam.is_user_logged_in(),
                                hashed_token=sam.get_user_account_hashed_token(),
                                cheat_sheet=sort_results(filter_title(name),'likes'),
                                )

def handle_search_empty(sam,csm):
    #same thing but simple cause you havent shearched anything yet
    if request.method == 'POST':
        return redirect(f'/search/{request.form.get("title")}')
    else:
        return render_template('search.html',
                               logged_in=sam.is_user_logged_in(),
                               hashed_token=sam.get_user_account_hashed_token(),
                               cheat_sheet=None,
                               )
