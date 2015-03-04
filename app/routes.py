from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import os, difflib

app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'log', 'cfg'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
  
@app.route('/')
def home():
  return render_template('home.html')
  
@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/uploadhtml')
def uploadhtml():
  return render_template('upload.html')

@app.route('/comptwo')
def comptwo():
  return render_template('comptwo.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded files
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to the upload
            # folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Save the filename into a list, we'll use it later
            filenames.append(filename)
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
    # Load an html page with a link to each uploaded file
    return render_template('uploaded.html', filenames=filenames)

# Route that will process the file comptwo
@app.route('/compdiff', methods=['POST'])
def compdiff():
    # Get the name of the uploaded files
    text1 = request.form.get("text1")
    text2 = request.form.get("text2")
    text1_lines = text1.splitlines()
    text2_lines = text2.splitlines()
    diff = difflib.HtmlDiff().make_table(text1_lines, text2_lines, context=True,
                                            numlines=4)
    return render_template('diff.html', diff=diff)

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
  app.run(debug=True)