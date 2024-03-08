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
            

            print("handle upload starting")
            new_cs = create_cheat_sheet(server_account_manager)
            print("handle_upload ok")
            new_cs.store_to_index()


            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'upload succesfull'
        
    
    logged_in: bool = server_account_manager.is_user_logged_in()
    print(logged_in)
    return render_template('upload.html',logged_in=logged_in)


def create_cheat_sheet(server_account_manager: ServerAccountManager):

    title = request.form.get("title")
    print("create cs starting")
    author_token = server_account_manager.get_user_account_token()
    print("create cs ok")
    content = request.form.get("file")
    description = request.form.get("description")
    keywords = request.form.get("keywords")
    keywords = keywords.split()
    new_cs = CheatSheet(title, author_token, content, description,)
    new_cs.keywords = keywords

    return new_cs