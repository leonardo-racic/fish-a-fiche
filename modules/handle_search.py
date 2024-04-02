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
    #this shit is super confusing (at least to me) so let me explain to you:
    #open cheat_sheet.json
    with open('cheat_sheet.json') as jsondata:
        #say that our dictionary data is what is inside of cheat_sheet basically but loaded whatever that means
        data: dict = json.loads(jsondata.read())["cheat_sheet"]
    #return a dictionnary verion of the filterd version of our items in data (but they are in a list). we use lambda as a filter because we could not figure out how to use a normal fuction so here cgoes a confusing syntax that say if title = name say True else say no.
    return dict(filter(lambda x:x[1]["title"] == name, list(data.items())))

def handle_search(sam,csm, name):
    if request.method == 'POST':
        terminal_log.debug(f'redirecting to /search/{request.form.get("title")}')
        return redirect(f'/search/{request.form.get("title")}')
    else:
        #this is debug shit to undestand what to code don't bother'
        terminal_log.debug(filter_title(name))
        terminal_log.debug(type(filter_title(name)))
        #new list : list_of_data which is a list of the values of our filtered items which are dictionnaries that contain cheat sheet information
        list_of_data = list(filter_title(name).values())
        terminal_log.debug(type(list_of_data))
        terminal_log.debug(list_of_data)
        #we then render our template with the stupidly complicated cheat_sheet format and others info like logged_inness or the hashed token
        return render_template('search.html',
                                logged_in=sam.is_user_logged_in(),
                                hashed_token=sam.get_user_account_hashed_token(),
                                cheat_sheet=list_of_data,
                                )

def handle_search_empty(sam,csm):
    #same thing but simple cause you havent shearched anything yet
    if request.method == 'POST':
        terminal_log.debug(f'redirecting to /search/{request.form.get("title")}')
        return redirect(f'/search/{request.form.get("title")}')
    else:
        return render_template('search.html',
                               logged_in=sam.is_user_logged_in(),
                               hashed_token=sam.get_user_account_hashed_token(),
                               cheat_sheet=None,
                               )
