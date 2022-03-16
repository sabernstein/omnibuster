import os
from crypt import methods
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from omnibuster import Omni_Parser

app = Flask(__name__)

directory = 'static/rendered_html/'

app.config['UPLOAD_FOLDER'] = '../xml_files'

@app.route("/", methods = ["GET", "POST"])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = str(f.filename)
        f.save(secure_filename(filename))
        parser = Omni_Parser(secure_filename(filename))
        parser.findExternalLinks()
        parser.create_Arrays()
        parser.createHTML()
        parser.createSectionHTML()
        parser.addButtons()
        # redirect
        return redirect('/static/rendered_html/index.html')
    
    
    for file in os.listdir(directory):
        if file.endswith(".html"):
            os.remove(directory + "/" + file)
            continue
        else:
            continue

    return render_template('home.html')