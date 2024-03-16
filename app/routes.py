from app import app
from flask import send_file, request


@app.route('/')
@app.route('/index.html')
def index():
    return 'Hello, World!'

@app.route('/get_preview')
def get_preview():
    if request.args.get('type') == '1':
        filename = 'sample_file.png'
        imagetype = 'image/png'
    else:
        filename = '../resources/error.jpg'
        imagetype = 'image/jpg'
    return send_file(filename, mimetype=imagetype)
