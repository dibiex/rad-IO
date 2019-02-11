import os
from flask import Flask, request, redirect, url_for, render_template
from threading import Thread
from multiprocessing.pool import ThreadPool
import subprocess
from check_one import predict
from werkzeug.utils import secure_filename
uploaded = False
UPLOAD_FOLDER = './upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/results')
def results():
	if uploaded:
		return '''
			<!doctype html>
			<h1>Upload an image first</h1>'''
	else:	
		path = request.args.get('path')
		if path != "":
			ret=["not yet"]
			print(path)
			output = subprocess.check_output(['bash', '-c', 'python3 check_one.py ' + path])
			output = output.decode('utf-8')
			arr = output.split('\n')
			l1 = arr[0].split(' ')
			l2 = arr[1].split(' ')
			
			print(ret)
			return render_template('result.html', pat1=l1[0] , pat2=l2[0] ,scor1=l1[1] , scor2=l2[1] )

		return '''
		 		<!doctype html>
		 		<h1>UPLOADED BUT</h1>'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded = True
            return redirect(url_for('results', path=path))
    return render_template('index.html')
