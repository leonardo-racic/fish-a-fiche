"""
This module contains the code for the cheatsheet uploader.

The main classes are:
- CheatSheet: represents a single cheatsheet
- CheatSheetManager: manages a list of cheatsheets
- ServerAccountManager: manages the user's authentication with the server

The main functions are:
- handle_upload: handles the upload of a new cheatsheet
- create_cheat_sheet: creates a new CheatSheet from the uploaded file
- read_md: reads the contents of a markdown file

The main routes are:
- /upload: handles the upload form

The main templates are:
- upload.html: the upload form

The main static files are part of the bootstrap library.

The main dependencies are:
- flask: the web framework used
- werkzeug: utilities for working with Flask
- markdown: for parsing markdown files
- bootstrap

Note: this docstring is a modified version of the Google Python Style Guide.
"""

from __future__ import annotations
import os
from flask import Flask, Response, request, flash, redirect, make_response
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os.path
from .cheat_sheet_module import CheatSheet
from .server_account_manager import ServerAccountManager
from .cheat_sheet_manager import CheatSheetManager
import terminal_log
from environment_variable import upload_path
from singletons import render_html, get_form_file, get_form_data


UPLOAD_FOLDER: str = upload_path
ALLOWED_EXTENSIONS: set = {'md','MD','txt', 'jpeg', 'png', 'jpg'}

app: Flask = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


csm: CheatSheetManager = CheatSheetManager()


def allowed_file(filename: str | None) -> bool:
    """
    This function checks if a file with the given name has a valid extension.

    :param filename: the name of the file to check
    :return: True if the file has a valid extension, False otherwise
    """
    if filename is None:
        return False
    extension: str = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and extension in ALLOWED_EXTENSIONS


def handle_upload(server_account_manager: ServerAccountManager) -> Response:
    """
    This function handles the upload of a new cheatsheet.

    :param server_account_manager: the server account manager used to authenticate the user
    :return: redirect to the same page if upload unsuccesfull, or a page indicating that the
             upload was succesfull otherwise.
    """
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            terminal_log.warn('no files uploaded')
            return make_response(redirect(request.url))
        
        terminal_log.inform('requesting file')
        file: FileStorage | None = get_form_file("file")
        if file is None:
            terminal_log.warn('no file uploaded')
            return make_response(redirect(request.url))

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            terminal_log.warn('no filename')
            return make_response(redirect(request.url))
        
        terminal_log.inform('verifying filename')
        if file and allowed_file(file.filename):
            filename: str = secure_filename(f"{get_form_data.get('title')}.txt")
            terminal_log.inform(f'filename secured FILENAME:{filename}')
            terminal_log.inform('saving file')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            terminal_log.inform('file saved')

            terminal_log.inform('creating cheat-sheet')
            new_cs = create_cheat_sheet(server_account_manager)
            terminal_log.inform(f'cheat_sheet created cs_token: {new_cs.token} author_token: {new_cs.author_token}')

            terminal_log.inform('storing to index')
            csm.add_cheat_sheet(new_cs)
            terminal_log.inform('stored to index')
            terminal_log.inform(
                f'{request.remote_addr}:{server_account_manager.get_user_account_token()} upload succesfull, redirecting'
            )
            flash('upload succesfull','success')


    return render_html(
        'upload.html',
        server_account_manager,
    )


def create_cheat_sheet(server_account_manager: ServerAccountManager):
    """
    This function creates a new CheatSheet object from the uploaded file.

    :param server_account_manager: the server account manager used to authenticate the user
    :return: the new CheatSheet object
    """
    form_data: dict[str, str] = get_form_data()
    title: str | None = form_data.get("title")
    author_token: str = server_account_manager.get_user_account_token()
    content: str = read_md(
        UPLOAD_FOLDER + "/" + secure_filename(str(title)) + ".txt"
    )
    description: str | None = form_data.get("description")
    new_cs = CheatSheet(str(title), author_token, content, str(description))
    server_account_manager.add_cheat_sheet_to_user(new_cs)
    return new_cs


def read_md(file: str) -> str:
    """
    This function reads the contents of a markdown file.

    :param file: the path to the markdown file
    :return: the contents of the markdown file
    """
    with open(file) as md:
        return md.read()


def get_extension(file_name: str | None) -> str:
    if file_name is None:
        return ""
    try:
        return file_name.split(".")[-1]
    except Exception:
        return ""


def handle_profile_picture_upload(new_image_input: FileStorage | None, sam: ServerAccountManager) -> str:
    if new_image_input is None:
        return ""
    elif new_image_input.filename == "":
        return ""
    elif new_image_input and allowed_file(new_image_input.filename):
        hashed_user_id: str = sam.get_user_account_hashed_token()
        extension: str = get_extension(new_image_input.filename)
        file_name: str = secure_filename(f"{hashed_user_id}.{extension}")
        path: str = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
        new_image_input.save(path)
        flask_path: str = os.path.join("upload", file_name)
        return flask_path
    return ""
