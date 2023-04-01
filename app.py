import ics
from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Add your authentication code here
    if username == 'admin' and password == 'password':
        return redirect(url_for('upload'))
    else:
        return redirect(url_for('home'))

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/process', methods=['POST'])
def process():
    f = request.files['file']
    filename = f.filename
    f.save(os.path.join('uploads', filename))
    with open(os.path.join('uploads', filename), 'r') as file:
        calendar = ics.Calendar(file.read())
        for event in calendar.events:
            event.name = event.name[7:]
    with open(os.path.join('uploads', 'modified_' + filename), 'w') as file:
        file.write(str(calendar))
    return redirect(url_for('download', filename=filename))

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join('uploads', 'modified_' + filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
