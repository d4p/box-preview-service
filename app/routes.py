from app import app
from flask import send_file, request
import subprocess
import os.path

@app.route('/')
@app.route('/index.html')
def index():
    #openscad -o test.png --imgsize=4096,4096  --colorscheme DeepOcean box_rounded.scad
    openscad_file = os.path.join(app.root_path,'..', 'openscad', 'box_rounded.scad')
    cache_file = os.path.join(app.root_path,'..', 'cache', 'box_rounded.png')
    status = subprocess.run(["openscad","-o",cache_file, "--imgsize=1024,1024", "--colorscheme", "DeepOcean", openscad_file], capture_output=True, text=True)
    return 'Hello, World!' + status.stdout + status.stderr

@app.route('/get_preview')
def get_preview():
    if request.args.get('type') == '1':
        filename = 'sample_file.png'
        imagetype = 'image/png'
    else:
        filename = '../resources/error.jpg'
        imagetype = 'image/jpg'
    return send_file(filename, mimetype=imagetype)
