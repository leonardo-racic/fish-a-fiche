from flask import Response, request, flash, abort, redirect, make_response
from .account_module import Account
from .server_account_manager import ServerAccountManager
from .cheat_sheet_manager import CheatSheetManager
from singletons import render_html, get_form_data
from terminal_log import warn, inform



def handle_collections(sam: ServerAccountManager, hashed_token: str) -> Response:
    target_account: Account | None = sam.get_account_from_hashed_token(hashed_token)
    collections: list | None
    if target_account == None:
        collections = None
    else:
        collections = sam.get_collections(target_account.get_id())
    if collections is None:
        flash("Unexisting collections", "warning")
        abort(404)
    is_user: bool = hashed_token == sam.get_user_account_hashed_token()


    if request.method == "GET" and target_account is Account:
        return render_html(
            "collections.html",
            sam,
            username=target_account.get_username(),
            collections=collections,
            author_hashed_token=hashed_token,
            is_user=is_user,
        )
    

    elif request.method == "POST":
        form_data: dict = get_form_data()
        input_type: str | None = form_data.get("input_type")
        if input_type == "create_collection_input":
            collection_name: str = form_data["collection_name"]
            is_public: bool = bool(form_data.get("is_collection_public"))
            source: str | None = form_data.get("source")
            if sam.has_user_collection(collection_name):
                warn(f'{request.remote_addr}:{request.cookies.get("account-token")} tried to create already existing collection')
                flash('Collection already exists', 'warning')
                if source == "cheat-sheet":
                    return make_response(redirect(f"/cheat-sheet/{source}"))
                return render_html(
                    "collections.html",
                    sam,
                    username=target_account.get_username(),
                    collections=collections,
                    author_hashed_token=hashed_token,
                    is_user=is_user,
                )
            else:
                sam.add_new_collection_to_account(collection_name, target_account.get_id(), is_public)
                inform(f'{request.remote_addr}:{request.cookies.get("account-token")} created collection : {collection_name}, {target_account.id}, {is_public}')
                if source == "cheat-sheet":
                    return redirect(source)
                return redirect(f"/collections/{hashed_token}")
            

        elif input_type == "delete_collection_input":
            flash('Collection has been deleted', 'success')
            collection_name: str = form_data["collection_name"]
            sam.delete_collection(collection_name, target_account.get_id())
            inform(f'{request.remote_addr}:{request.cookies.get("account-token")} deleted collection {collection_name}')
            return redirect(f"/collections/{hashed_token}")
        

        elif input_type == "save_collection_input":
            flash('Collection has been saved', 'success')
            collection_name: str = form_data["collection_name"]
            cheat_sheet_token: str = form_data["cheat_sheet_token"]
            sam.save_to_collection(collection_name, cheat_sheet_token)
            inform(f'{request.remote_addr}:{request.cookies.get("account-token")} saved collection {collection_name}')
            return redirect(f"/cheat-sheet/{cheat_sheet_token}")
        

        elif input_type == "remove_cheat_sheet_input":
            flash('cheat-sheet removed','success')
            collection_name: str = form_data["collection_name"]
            cheat_sheet_token: str = form_data["cheat_sheet_token"]
            user_token: str = sam.get_user_account_token()
            sam.remove_cheat_sheet_from_collection(user_token, collection_name, cheat_sheet_token)
            inform(f'{request.remote_addr}:{request.cookies.get("account-token")} removed cheat-sheet: {cheat_sheet_token} from collection: {collection_name}')
            return redirect(f"/cheat-sheet/{cheat_sheet_token}")
        

    return "WIP, come back later! ^^"


def handle_collection(
    sam: ServerAccountManager,
    csm: CheatSheetManager,
    hashed_token: str,
    collection_name: str
) -> Response:
    
    author: Account = sam.get_account_from_hashed_token(hashed_token)
    is_user: bool = author.get_id() == sam.get_user_account_token()
    cheat_sheet_tokens: list = sam.get_cheat_sheet_token_from_collection(author.get_id(), collection_name)
    cheat_sheet_info = []
    if cheat_sheet_tokens is not None:
        for token in cheat_sheet_tokens:
            target_cheat_sheet_info: dict = csm.get_cheat_sheet_info(token)
            cheat_sheet_info.append(target_cheat_sheet_info)

    if request.method == "POST":
        form_data: dict = get_form_data()
        input_type: str = form_data.get("input_type")
        if input_type == "rename_collection_input":
            new_collection_name: str = form_data.get("collection_name")
            sam.rename_collection(author.get_id(), collection_name, new_collection_name)
            inform(f'{request.remote_addr}:{request.cookies.get("account-token")} renamed collection {collection_name}, to {new_collection_name}')
            flash('collection renamed','success')
            return redirect(f"/collections/{hashed_token}/{new_collection_name}")
        
        
        elif input_type == "publish_collection_input":
            sam.toggle_collection_visibility(author.get_id(), collection_name)
            flash('Visibility modified','success')
            inform(f'{request.remote_addr}:{request.cookies.get("account-token")} modified the visibility of {collection_name}')
            return redirect(f"/collections/{hashed_token}/{collection_name}")


        elif input_type == "remove_cheat_sheet_input":
            cheat_sheet_token: str = form_data["cheat_sheet_token"]
            user_token: str = sam.get_user_account_token()
            sam.remove_cheat_sheet_from_collection(user_token, collection_name, cheat_sheet_token)
            flash('Cheat-sheet has been removed', 'success')
            inform(f'{request.remote_addr}:{request.cookies.get("account-token")} removed cheat-sheet:{cheat_sheet_token} from collection {collection_name}')
            return redirect(f"/collections/{hashed_token}/{collection_name}")
        

    elif request.method == "GET":
        return render_html(
            "collection.html",
            sam,
            collection_name=collection_name,
            cheat_sheet=cheat_sheet_info,
            is_user=is_user,
            is_public=sam.is_collection_public(author.get_id(), collection_name),
        )
    

    else:
        return "Method not supported"
