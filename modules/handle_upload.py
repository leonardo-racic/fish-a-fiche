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

import os
from flask import Flask, Response, flash, request, redirect, render_template, abort
from werkzeug.utils import secure_filename
from werkzeug.datastructures.file_storage import FileStorage
import os.path
from .cheat_sheet_module import CheatSheet
from .server_account_manager import ServerAccountManager
from .cheat_sheet_manager import CheatSheetManager
import terminal_log
from environment_variable import upload_path


UPLOAD_FOLDER: str = upload_path
ALLOWED_EXTENSIONS: set = {'md','MD','txt', 'jpeg', 'png', 'jpg'}

app: Flask = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


csm: CheatSheetManager = CheatSheetManager()


def allowed_file(filename: str) -> bool:
    """
    This function checks if a file with the given name has a valid extension.

    :param filename: the name of the file to check
    :return: True if the file has a valid extension, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def handle_upload(server_account_manager: ServerAccountManager) -> Response:
    """
    This function handles the upload of a new cheatsheet.

    :param server_account_manager: the server account manager used to authenticate the user
    :return: redirect to the same page if upload unsuccesfull, or a page indicating that the
             upload was succesfull otherwise.
    """
    logged_in: bool = server_account_manager.is_user_logged_in()
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            terminal_log.warn('no files uploaded')
            return redirect(request.url)
        
        terminal_log.inform('requesting file')
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            terminal_log.warn('no filename')
            return redirect(request.url)
        
        terminal_log.inform('verifying filename')
        if file and allowed_file(file.filename):
            
            filename = secure_filename(request.form.get("title"))
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
            terminal_log.inform(f'{request.remote_addr}:{server_account_manager.get_user_account_token()} upload succesfull, redirecting')
            flash('upload succesfull','success')
            return render_template('upload.html',
                                   logged_in=logged_in,
                                   hashed_token=server_account_manager.get_user_account_hashed_token(),
                                   )

    return render_template(
        'upload.html',
        logged_in=logged_in,
        hashed_token=server_account_manager.get_user_account_hashed_token(),
    )


def create_cheat_sheet(server_account_manager: ServerAccountManager):
    """
    This function creates a new CheatSheet object from the uploaded file.

    :param server_account_manager: the server account manager used to authenticate the user
    :return: the new CheatSheet object
    """
    file = request.files['file']
    title = request.form.get("title")
    author_token = server_account_manager.get_user_account_token()
    content = read_md(UPLOAD_FOLDER+"/"+str(secure_filename(request.form.get("title"))))
    description = request.form.get("description")
    #keywords = request.form.get("keywords")
    #keywords = keywords.split()
    new_cs = CheatSheet(title, author_token, content, description)
    #new_cs.keywords = keywords

    return new_cs


def read_md(file):
    """
    This function reads the contents of a markdown file.

    :param file: the path to the markdown file
    :return: the contents of the markdown file
    """
    with open(file) as md:
        return md.read()


def get_extension(file_name: str) -> str:
    try:
        return file_name.split(".")[-1]
    except Exception:
        return ""

def handle_profile_picture_upload(new_image_input: FileStorage, sam: ServerAccountManager) -> str:
    if new_image_input.filename == "":
        return ""
    elif new_image_input and allowed_file(new_image_input.filename):
        hashed_user_id: str = sam.get_user_account_hashed_token()
        extension: str = get_extension(new_image_input.filename)
        file_name: str = secure_filename(f"{hashed_user_id}.{extension}")
        path: str = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
        new_image_input.save(path)
        return path
    return ""
