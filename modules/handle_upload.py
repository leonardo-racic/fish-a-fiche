import os
from flask import Flask, flash, request, redirect, url_for , render_template
from werkzeug.utils import secure_filename
import os.path
from .cheat_sheet_module import CheatSheet
from .server_account_manager import ServerAccountManager



UPLOAD_FOLDER = 'sheets'
ALLOWED_EXTENSIONS = {'md','MD'}

app: Flask = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER





def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def handle_upload(server_account_manager: ServerAccountManager):

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):

            new_cs = create_cheat_sheet(server_account_manager)

            new_cs.store_to_index()


            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'upload succesfull'
    return render_template('upload.html')


def create_cheat_sheet(server_account_manager: ServerAccountManager):

    title = request.form.get("title")
    author_token = ServerAccountManager.get_user_account_token()
    content = request.form.get("file")
    description = request.form.get("description")
    keywords = request.form.get("keywords")
    keywords = keywords.split()
    new_cs = CheatSheet(title, author_token, content, description,)
    new_cs.keywords = keywords

    return new_cs