import os
from crypt import methods
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from omnibuster import Omni_Parser
import sys

app = Flask(__name__)

directory = 'static/rendered_html/'

app.config['UPLOAD_FOLDER'] = '../xml_files'

@app.route("/", methods = ["GET", "POST"])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']

        # print(f, file=sys.stderr, flush=True)

        filename = str(f.filename)
        f.save(secure_filename(filename))
        parser = Omni_Parser(secure_filename(filename))
        parser.findExternalLinks()
        parser.getShortTitle()
        parser.create_Arrays()
        parser.createHTML()
        parser.createSectionHTML()
        parser.addDefiniions()
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


@app.route('/submit', methods = ["GET", "POST"])
def downloadFile():
    print("here", file=sys.stderr, flush=True)

    if request.method == 'POST':
        ftext = request.form['getDocResults']

        tmp_file = open("temp.xml", "r+")
        tmp_file.write(ftext)
        # print(tmp_file.read(), file=sys.stderr, flush=True)
        tmp_file.close()

        with open('temp.xml', 'rb') as fp:
            f = FileStorage(fp)

        filename = str(f.filename)
        f.save(secure_filename(filename))
        parser = Omni_Parser(f)
        parser.findExternalLinks()
        parser.getShortTitle()
        parser.create_Arrays()
        parser.createHTML()
        parser.createSectionHTML()
        parser.addDefiniions()
        parser.addButtons()
    #     # redirect
        return redirect('/static/rendered_html/index.html')
    
    
    
    # for file in os.listdir(directory):
    #     if file.endswith(".html"):
    #         os.remove(directory + "/" + file)
    #         continue
    #     else:
    #         continue

    # return render_template('home.html')