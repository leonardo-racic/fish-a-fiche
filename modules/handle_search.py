from __future__ import annotations
from singletons import render_html, get_form_data
from flask import Response, request, redirect, make_response
from .sorting import sort_results_by_keywords, sort_results_by_likes
from .server_account_manager import ServerAccountManager
from .filtering import filter_context, filter_profiles, filter_title, get_profiles



def handle_search(sam: ServerAccountManager, search: str) -> Response:
    search_by: str | None
    if request.method == 'POST':
        form_data: dict[str, str] = get_form_data()
        title: str | None = form_data.get("title")
        search_by = form_data.get("search_by")
        return make_response(redirect(f'/search/{title}&{search_by}'))
    else:
        try:
            search_data: str = search[:search.rindex("&")]
        except ValueError:
            return make_response(redirect(f'/search/{search}&title'))
        
        
        search_by = search[search.rindex("&")+1:]
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
        return make_response("oops")


def handle_search_empty(sam: ServerAccountManager) -> Response:
    if request.method == 'POST':
        form_data: dict[str, str] = get_form_data()
        title: str | None = form_data.get("title")
        search_by: str | None = form_data.get("search_by")
        return make_response(redirect(f'/search/{title}&{search_by}'))
    else:
        return render_html(
            'search.html',
            sam,
            search_by="title",
            cheat_sheet=sort_results_by_likes(filter_title()),
            profiles=get_profiles(),
            search_title="",
        )

