from singletons import render_html
from flask import Response, request, redirect
from .sorting import sort_results_by_keywords, sort_results_by_likes
from .server_account_manager import ServerAccountManager
from .filtering import filter_context, filter_profiles, filter_title, get_profiles



def handle_search(sam: ServerAccountManager, search: str) -> Response:
    if request.method == 'POST':
        title: str = request.form.get("title")
        search_by: str = request.form.get("search_by")
        return redirect(f'/search/{title}&{search_by}')
    else:
        try:
            search_data: str = search[:search.rindex("&")]
        except ValueError:
            return redirect(f'/search/{search}&title')
        
        
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

