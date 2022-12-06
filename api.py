# app.py
from flask import Flask, render_template, send_file, Response, abort, jsonify, request, url_for, redirect
from sqlalchemy.sql import text
from werkzeug.utils import secure_filename
# Para a autenticação
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os
auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("ninda")
}



@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

app = Flask(__name__, template_folder="templates")
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.txt','.jpg']
app.config['UPLOAD_PATH'] = 'uploads/'

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/admin/upload')
@auth.login_required
def handleUpload():
    dir_name = os.path.join(app.config['UPLOAD_PATH'])
    files = []
    list_of_files = filter( lambda x: os.path.isfile(os.path.join(dir_name, x)), os.listdir(dir_name) )
    files_with_size = [ (file_name, os.stat(os.path.join(dir_name, file_name)).st_size) for file_name in list_of_files  ]
    for file_name, size in files_with_size:
        files.append( file_name + ' | ' + str(size) + ' bytes')
    return render_template('upload.html', files=files)

@app.route('/admin/upload', methods=['POST'])
@auth.login_required
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        arquivo = open(app.config['UPLOAD_PATH'] + filename, "rb")
    return redirect('upload')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9001 ,debug=True)